from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.db import connection,connections
from django.db import IntegrityError
from chartit import DataPool, Chart
from django.db import models
from collections import defaultdict
from random import randint
from django.template.defaulttags import register
from Naked.toolshed.shell import execute_js
import subprocess
from geopy.geocoders import Nominatim
import re
from subprocess import CalledProcessError, check_output
from xlrd import open_workbook
import math
from django.core.cache import cache



# Create your views here.


def home(request):

	IDTaken = False
	notInt = False
	match = True
	validHosp = True

	isPOSTRequest = (request.method == "POST")
	requestType = request.POST['action'] if isPOSTRequest else None
	

	#excelToDatabase(request,"2010","Data_2010.xls")


	if isPOSTRequest:
		if(requestType == "Login"):

			match = login(request)

		if(requestType == "Register"):

			IDTaken = register(request)
	
	currMember = None
	try:
		currMember = request.session['member_id']
	except KeyError:
		currMember = None

	print currMember
	if(currMember == None):
		return render(request,'index.html',locals())
	else:
		if(requestType == "Logout"):
			logout(request)
			return redirect("home")
		hospName,validHosp = getUserName(request)
		if(validHosp == True):
			return render(request,'home.html',locals())
		else:
			return render(request,'index.html',locals())

def main(request):

	isPOSTRequest = (request.method == "POST")
	requestType = request.POST['action'] if isPOSTRequest else None	

	if(requestType == "Logout"):
		del request.session['member_id']
		return redirect('home')

	
	hospName = getUserName(request)
	return render(request,'home.html',locals())

def account(request):

	cursor = connections['user'].cursor()
	hospID = request.session['member_id']


	fieldsComplete = True
	success = False
	IDTaken = False
	notInt = False

	name = ''
	passw = ''
	id = ''
	email = ''

	isPOSTRequest = (request.method == "POST")
	requestType = request.POST['action'] if isPOSTRequest else None
	if(requestType == "change"):

		name = request.POST.get('name','')
		passw = request.POST.get('hospass','')
		id = request.POST.get('hospid','')
		email = request.POST.get('email','')

		print name
		print passw
		print id

		if(id.isdigit() == False):
				notInt = True
				


		elif(name == "" or passw == "" or id == ""):
			fieldsComplete = False
			

		else:
		
			try:
				cursor.execute("UPDATE Users SET UserName = %s, Password = %s, UserID = %s, Email = %s WHERE UserID = %s", [name,passw,id,email,hospID])
				del request.session['member_id']
				request.session['member_id'] = id
				hospID = request.session['member_id']
				success = True
			except IntegrityError as e:
				IDTaken = True
				return render(request,'account.html',locals())
			


	elif(requestType == "Delete Account"):
		cursor.execute('DELETE FROM Users Where UserID = %s', [hospID])
		del request.session['member_id']
		return redirect('home')

	elif(requestType == "Log out"):
		logout(request)
		return redirect('home')

	elif(requestType == "cancel"):
		cursor.execute('SELECT * FROM Users WHERE UserID = %s', [hospID])
		allInfo = cursor.fetchone()
		ID = allInfo[0]
		Name = allInfo[1]
		Email = allInfo[2]
		Password = allInfo[3]


	cursor.execute('SELECT * FROM Users WHERE UserID = %s', [hospID])

	allInfo = cursor.fetchone()
	ID = allInfo[0]
	Name = allInfo[1]
	Email = allInfo[2]
	Password = allInfo[3]

	hospName = getUserName(request)[0]
	return render(request,'account.html',locals())


def form(request):
	return render(request,'form.html',locals())

def getUserName(request):
	cursor = connection.cursor()
	validHosp = True
	hospID = request.session['member_id']
	hospName = ''
	print("This is your hospid:" + str(hospID))
	cursor.execute('SELECT Name FROM Information WHERE ID = %s', [hospID])
	try:
		hospName = cursor.fetchone()[0]
	except:
		validHosp = False
	#hospName = (hospName + " Hospital").title()
	return hospName,validHosp

def login(request):


	cursor = connections['user'].cursor()

	hospID = request.POST.get('username','')
	password = request.POST.get('password','')
	match = True

	cursor.execute('SELECT UserID FROM Users WHERE UserID = %s AND Password = %s ', [hospID,password])
	output = cursor.fetchone()
	if(output != None):
		request.session['member_id'] = output[0]
		match = True
	else:
		match = False
		
	return match

def register(request):

	cursor = connections['user'].cursor()
	IDTaken = False

	hospname = request.POST.get('hospName','')
	hospid = request.POST.get('hospID','')
	password = request.POST.get('password','')
	email = request.POST.get('email','')

	#Check first if ID is a valid number, continue if so , otherwise return page with warning
	if(hospid.isdigit() == False):
		notInt = True
		return render(request,"index.html",locals())

	#Convert to SQL command based on inputs from login form

	raw_sql = "INSERT INTO Users(UserID, UserName, Email, Password) VALUES ("
	sql_vals = [int(float(hospid)), '\"'+hospname+'\"', '\"'+email+'\"', '\"'+password+'\"']
	raw_sql += "%d, " %sql_vals[0]
	for i in range(1, len(sql_vals)):
		raw_sql = raw_sql + str(sql_vals[i])
		if (i < len(sql_vals) - 1):
		 raw_sql = raw_sql + ", "
	raw_sql = raw_sql + ");"

	#cursor.execute("INSERT INTO User (Id, Name, Email, Password) VALUES (2,'name','email','password')")
	#Execute SQL code and if ID is not unique then reload page with warning

	#cursor.execute(raw_sql)
	try:
		cursor.execute(raw_sql)
		request.session['member_id'] = hospid
	except IntegrityError as e:
		IDTaken = True
		
	return IDTaken

def logout(request):
	del request.session['member_id']
	return redirect('home')

def dashboard(request):
	
	hospName = getUserName(request)[0]
	startYear = 2013;
	startYear2 = 2013;
	medicareInRev,medicaidInRev,otherPublicInRev,privateInRev,totalInRev,\
	medicareOutRev,medicaidOutRev,otherPublicOutRev,privateOutRev,totalOutRev = revenueComparison(request,str(startYear))

	isPOSTRequest = (request.method == "POST")
	if(isPOSTRequest):
		year = request.POST.get('hiddeninput','')
		if(year != "video34"):
			startYear = year
		year2 = request.POST.get('hiddenout','')
		if(year != "video34"):
			startYear2 = year2
		print(year)
		medicareInRev,medicaidInRev,otherPublicInRev,privateInRev,totalInRev,\
		medicareOutRev,medicaidOutRev,otherPublicOutRev,privateOutRev,totalOutRev = revenueComparison(request,str(startYear))


	return render(request,'dashboard.html',locals())


def revenueComparison(request,startYear):
	
	currUserId = request.session['member_id']
	if(startYear != '2013'):
		cursor = connections[startYear].cursor() 
	else:
		cursor = connection.cursor()

	hospID = request.session['member_id']
	cursor.execute('SELECT Inpatient_Medicaid FROM Revenue WHERE ID = %s', [hospID])
	medicaidInRev = cursor.fetchone()[0]
	cursor.execute('SELECT Inpatient_Medicare FROM Revenue WHERE ID = %s', [hospID])
	medicareInRev = cursor.fetchone()[0]
	cursor.execute('SELECT Inpatient_Other_Public_Payment FROM Revenue WHERE ID = %s', [hospID])
	otherPublicInRev = cursor.fetchone()[0]
	cursor.execute('SELECT Inpatient_Private_Insurance FROM Revenue WHERE ID = %s', [hospID])
	privateInRev = cursor.fetchone()[0]
	
	
	cursor.execute('SELECT Outpatient_Medicaid FROM Revenue WHERE ID = %s', [hospID])
	medicaidOutRev = cursor.fetchone()[0]
	cursor.execute('SELECT Outpatient_Medicare FROM Revenue WHERE ID = %s', [hospID])
	medicareOutRev = cursor.fetchone()[0]
	cursor.execute('SELECT Outpatient_Other_Public_Payment FROM Revenue WHERE ID = %s', [hospID])
	otherPublicOutRev = cursor.fetchone()[0]
	cursor.execute('SELECT Outpatient_Private_Insurance FROM Revenue WHERE ID = %s', [hospID])
	privateOutRev = cursor.fetchone()[0]

	totalInRev = 0
	totalOutRev = 0
	

	return medicareInRev,medicaidInRev,otherPublicInRev,privateInRev,\
	totalInRev,medicareOutRev,medicaidOutRev,otherPublicOutRev,privateOutRev,totalOutRev

def surgery(request):

	hospName = getUserName(request)[0]
	surgeryData = defaultdict(dict)
	years = [2013,2012,2011,2010,2009]
	hospID = request.session['member_id']
	surgeryTypes = ['General_Inpatient_Cases','Ophthalmology_Inpatient_Cases','Cardiovascular_Inpatient_Cases','Dermatology_SurgeryInpatient_Cases',
	'Gastroenterology_Inpatient_Cases','Neurology_Inpatient_Cases','Obstetric_Gynecology_Inpatient_Cases','Oral_Maxillofacia_Inpatient_Cases','Orthopedic_Inpatient_Cases',
	'Otolaryngology_Inpatient_Cases','Plastic_Inpatient_Cases','Podiatry_Inpatient_Cases','Thoracic_Inpatient_Cases','Urology_Inpatient_Cases']
	

	for x in surgeryTypes:
		for y in years:

			if(y != 2013):
				cursor = connections[str(y)].cursor()
			else:
				cursor = connection.cursor()

			sqlQuery = "SELECT " + x + " FROM Surgery WHERE ID = " + str(hospID)
			cursor.execute(sqlQuery)
			surgeryData[x][y] = cursor.fetchone()[0]
			
			
	for k,a_dict in surgeryData.items():
		print (k)
		for k2,v in a_dict.items():
			print(v)



	return render(request,'surgery.html',locals())

def outpatient(request):
	hospName = getUserName(request)[0]
	startYear = 2013;
	medicareInRev,medicaidInRev,otherPublicInRev,privateInRev,totalInRev,\
	medicareOutRev,medicaidOutRev,otherPublicOutRev,privateOutRev,totalOutRev = revenueComparison(request,str(startYear))

	isPOSTRequest = (request.method == "POST")
	if(isPOSTRequest):
		year = request.POST.get('hiddeninput','')
		if(year != "video34"):
			startYear = year
		print(year)
		medicareInRev,medicaidInRev,otherPublicInRev,privateInRev,totalInRev,\
		medicareOutRev,medicaidOutRev,otherPublicOutRev,privateOutRev,totalOutRev = revenueComparison(request,str(startYear))

	return render(request,'outpatient.html',locals())

def patient(request):

	#geolocator = Nominatim()
	#location = geolocator.geocode("Dupage hospital")
	api_key = 'AIzaSyB--XNP_v_U26cBpVbE8T3rm_HTe0PKxvU'
	#gmaps = GoogleMaps(api_key)
	#print(location.address)

	isPOSTRequest = (request.method == "POST")
	requestType = request.POST['action'] if isPOSTRequest else None
	hospNotFound = False
	Procedures = False
	validZip = True
	foundBest = False
	procedure = ''
	bestHospital = ''
	finalProc = ''
	listOfProcedures = ['Alcohol/Drug Abuse','Appendectomy','Bronchitis and Asthma','Cellulitis','Caesarian Section','Cesarean with Multiple Complications','Chest Pain','Chronic Obstructive Pulmonary Disease','Diabetes','Digestive Disorders','Heart Failure','Heart Failure with Complications','Heart Failure with Multiple Complications','Major Joint Replacement','Urinary Tract Infections','Gallbladder Removal By Laparoscope','Normal Newborn','Neonate with Other Significant Problems','Metabolic Disorders','Pneumonia','Psychoses','Rehabilitation Multiple Complications','Septicemia with Multiple Complications','Uterine Procedures for Nonmalignancy without Multiple Complications','Vaginal Birth','Bronchitis and Asthma Pediatric','Psychoses Pediatric','Vaginal Birth Pediatric','Arthroscopy','Bunionectomy','Cardiac Catheterization','Colonoscopy','Diagnostic procedures, male genital','Knee Cartilage Excision','Lesion Excision','Insertion of catheter or spinal stimulator and inj','Inguinal Hernia Repair','Laproscopic Cholecystectomy','Lens Procedures','Lumpectomy','Other non-OR therapeutic procedures, male genital','PTCA','Tonsillectomy','Upper GI Endoscopy','Decompression Peripheral Nerve','Other Therapeutic Procedures on Muscles and Tendons','Myringotomy Pediatric','Tonsillectomy Pediatric']
	cursor = connection.cursor()
	cursor.execute('SELECT Name FROM Information')	
	output = cursor.fetchall()
	combined1 = ''
	combined = ''
	index = 0

	# for x in output:
	# 	name = x[0]
	# 	for proc in listOfProcedures:
	# 		key = (name,x)
	# 		data = cache.get(key)
	# 		if data is None:
	# 			cmd = ['/usr/local/Cellar/casperjs/1.1-beta3/libexec/bin/casperjs', 'procedureCost.js',name]
	# 			cmdName = ['/usr/local/Cellar/casperjs/1.1-beta3/libexec/bin/casperjs', 'hospName.js',name]
	# 			try:
	# 				response = subprocess.check_output(cmd)
	# 				name = subprocess.check_output(cmdName)
	# 				Procedures = True
	# 			except:
	# 				hospNotFound = True
	# 				return render(request,'patient.html',locals())

	# 			response = subprocess.check_output(cmd)
	# 			response = response.replace("\xc2\xa0", " ")
	# 			costOfProcedure = response.split()
	# 			try:
	# 				while(1):
	# 					costOfProcedure.remove('few')
	# 			except:
	# 				hi = 0
				
	# 			try:
	# 				while(1):
	# 					costOfProcedure.remove('cases')
	# 			except:
	# 				hi = 0

	# 			for x in range(0,len(costOfProcedure)):
	# 				if(costOfProcedure[x] == "too"):
	# 					costOfProcedure[x] = "N/A"

	# 			print(costOfProcedure) 
	# 			combined1 = zip(costOfProcedure,listOfProcedures)
	# 			cache.set(key,combined1)
	

	if(requestType == "Search"):
		hospitalName = str(request.POST.get('hospInput',''))
		cmd = ['/usr/local/Cellar/casperjs/1.1-beta3/libexec/bin/casperjs', 'procedureCost.js',hospitalName]
		cmdName = ['/usr/local/Cellar/casperjs/1.1-beta3/libexec/bin/casperjs', 'hospName.js',hospitalName]
		try:
			response = subprocess.check_output(cmd)
			name = subprocess.check_output(cmdName)
			Procedures = True
		except:
			hospNotFound = True
			return render(request,'patient.html',locals())

		response = subprocess.check_output(cmd)
		response = response.replace("\xc2\xa0", " ")
		costOfProcedure = response.split()
		try:
			while(1):
				costOfProcedure.remove('few')
		except:
			hi = 0
		
		try:
			while(1):
				costOfProcedure.remove('cases')
		except:
			hi = 0

		for x in range(0,len(costOfProcedure)):
			if(costOfProcedure[x] == "too"):
				costOfProcedure[x] = "N/A"

		print(costOfProcedure) 
		combined = zip(costOfProcedure,listOfProcedures)

	elif(requestType == "Find"):
		lowestCosts = []
		zipCode = str(request.POST.get('inputZip',''))
		procedure = str(request.POST.get('procSelect',''))
		if(len(zipCode) != 5):
			validZip = False
			render(request,'patient.html',locals())

		cmd = ['/usr/local/Cellar/casperjs/1.1-beta3/libexec/bin/casperjs', 'closestHospitals.js', zipCode]

		try:
			response = subprocess.check_output(cmd)

		except:
			validZip = False
			return render(request,'patient.html',locals())

		response = str(response)
		response = re.sub('- Details', '', response)
		response = re.sub('-','',response)
		validHosps = []
		closestNamesList = [y for y in (x.strip() for x in response.splitlines()) if y]
		cmd = ['/usr/local/Cellar/casperjs/1.1-beta3/libexec/bin/casperjs', 'lowestCost.js']
		finalProc = procedure
		procedure = procedure.replace(" ", "")
		procedure = procedure.replace("/", "")
		print(procedure)
		procedure = ' a[href = "/glossaries/index/#MedianCharges' + procedure + '"] span' 
		#procedure = "' a[href = " + '"/glossaries/index/#MedianCharges' + procedure + '"]' + " span'"
		#' a[href = "/glossaries/index/#MedianChargesArthroscopy"] span'
		print(procedure)
		print(closestNamesList)
		blacklist = ["N/A", "too few cases", "too cases"]
		for name in closestNamesList:
			cmd = ['/usr/local/Cellar/casperjs/1.1-beta3/libexec/bin/casperjs', 'lowestCost.js',name,procedure]
			try:
				lowestCosts.append(subprocess.check_output(cmd))
				#lowestCosts[name] = ["$" + k for k in ((subprocess.check_output(cmd))).split('$') if not k == ""]
				# for i in blacklist:
				# 	tmp_arr = []
				# 	for k in lowestCosts[name]:
				# 		if(not i in k):
				# 			tmp_arr.append(k)
				# 		else:
				# 			tmp_arr.append(k[0:k.index(i)])
				# 			tmp_arr.append(i)
				# 	lowestCosts[name] = tmp_arr
				# 	print 'e'

				validHosps.append(name)
				print(lowestCosts)
			except subprocess.CalledProcessError as e:
				#print e.output
				hi = 0
		for x in range(0,len(lowestCosts)):
			if(lowestCosts[x] == "N/A\n" or lowestCosts[x] == 'N/AN/A\n' or lowestCosts[x] == 'too few cases\n' or lowestCosts[x] == "oo few cases" or lowestCosts[x] == 'too few\n'):
				lowestCosts[x] = "1000000000"
			else:
				lowestCosts[x] = lowestCosts[x][1:]
				lowestCosts[x] = lowestCosts[x].replace(",", "")
			#lowestCosts[x] = lowestCosts[x][:-3]
			print(lowestCosts[x])
		index = 0
		smallestVal = float(lowestCosts[0])
		for x in range(0,len(lowestCosts)):
			if(smallestVal > float(lowestCosts[x])):
				smallestVal = float(lowestCosts[x])
		print(smallestVal)
		for x in range(0,len(lowestCosts)):
			if(float(lowestCosts[x]) == smallestVal):
				index = x
		bestHospital = validHosps[index]
		foundBest = True

		if( all(i == "1000000000" for i in lowestCosts)):
			bestHospital = "Not enough data"
			smallestVal = "Not enough data"


		


	return render(request,'patient.html',locals())

def rank(request):
	
	years = ["2013","2012","2011","2010","2009"]
	year = "2013"
	isPOSTRequest = (request.method == "POST")
	
	if(isPOSTRequest):
		year = str((request.POST.get('yearSelect','')))
		print(year)

	if(year != "2013"):
		cursor = connections[year].cursor()
	else:
		cursor = connection.cursor()

	cursor.execute("SELECT Revenue.ID, Revenue.Name, sum(Revenue.Inpatient_Medicaid + Revenue.Inpatient_Medicare + Revenue.Inpatient_Other_Public_Payment + Revenue.Inpatient_Private_Insurance + Revenue.Inpatient_Private_Payment + Revenue.Outpatient_Medicaid + Revenue.Outpatient_Medicare + Revenue.Outpatient_Other_Public_Payment + Revenue.Outpatient_Private_Insurance + Revenue.Outpatient_Private_Payment ) AS Total_Revenue FROM Revenue GROUP BY Revenue.ID, Revenue.Name, Revenue.Inpatient_Medicaid ORDER BY Total_Revenue DESC;")
	output = cursor.fetchall()

	hospName = getUserName(request)[0]
	print(hospName)
	hospID = request.session["member_id"]
	hospNames = []
	hospRevenues = []
	for hospsOrdered in output:
		hospNames.append(hospsOrdered[1])
		if(hospsOrdered[2] != 0):
			hospRevenues.append("${:,.2f}".format(hospsOrdered[2]))
		else:
			hospRevenues.append("N/A")
	print(hospNames)
	print(hospRevenues)
	combined = zip(hospNames,hospRevenues)



	return render(request,'rank.html',locals())
def calcRank(request,year):
	
	if(year != "2013"):
		cursor = connections[year].cursor()
	else:
		cursor = connection.cursor()

	cursor.execute("SELECT Revenue.ID, Revenue.Name, sum(Revenue.Inpatient_Medicaid + Revenue.Inpatient_Medicare + Revenue.Inpatient_Other_Public_Payment + Revenue.Inpatient_Private_Insurance + Revenue.Inpatient_Private_Payment + Revenue.Outpatient_Medicaid + Revenue.Outpatient_Medicare + Revenue.Outpatient_Other_Public_Payment + Revenue.Outpatient_Private_Insurance + Revenue.Outpatient_Private_Payment ) AS Total_Revenue FROM Revenue GROUP BY Revenue.ID, Revenue.Name, Revenue.Inpatient_Medicaid ORDER BY Total_Revenue DESC;")
	output = cursor.fetchall()

	hospName = getUserName(request)[0]
	
	hospID = request.session["member_id"]
	hospNames = []
	hospRevenues = []
	for hospsOrdered in output:
		hospNames.append(hospsOrdered[1])
		if(hospsOrdered[2] != 0):
			hospRevenues.append("${:,.2f}".format(hospsOrdered[2]))
		else:
			hospRevenues.append("N/A")
	for x in range(0,len(hospRevenues)):
		if(hospNames[x] == hospName):
			return x+1


def correlation(request):
	typesOfPayments = ["Outpatient Medicaid Patients","Outpatient Medicare Patients","Outpatient Private insurance Patients","Outpatient Private Payment Patients","Outpatient Other Payments Patients","Inpatient Medicaid Patients","Inpatient Medicare Patients","Inpatient Private Insurance","Inpatient Private Payment Patients","Inpatient Other Payment Patients"]
	hospName = getUserName(request)[0]
	allX = [10,100,400,500]
	allY = [200,0,100,0]

	avgX = 0
	avgY = 0

	
	years = ["2013","2012","2011","2010","2009"]
	#avgList = ["inMedicareAvg","inMedicaid","inPublic",""]
	cursor = connections["2012"].cursor()
	cursor.execute("select * from Data_2012.Avg_Patients_All_Source")
	output = cursor.fetchall()
	
	avgNums = {}
	for x in range(0,10):
		avgNums[typesOfPayments[x]] = output[0][x]

	
	cursor.execute("select * from Data_2012.Avg_Payment_All_Source")
	output = cursor.fetchall()

	avgRevs = {}
	for x in range(0,10):
		avgRevs[typesOfPayments[x]] = output[0][x]

	print(avgNums)
	print(avgRevs)
	hospID = request.session['member_id']

	idx = 0

	patientNums = {}
	patientRevenue = {}

	for x in years:
		if(x == "2013"):
			cursor = connection.cursor()
		else:
			cursor = connections[x].cursor()
		cursor.execute("""SELECT 
    Patient_By_Payment_Source.Name,
    Patient_By_Payment_Source.ID,
    Patient_By_Payment_Source.Outpatient_Medicaid as Out_Medicaid_Patients,
    Patient_By_Payment_Source.Outpatient_Medicare as Out_Medicare_Patients,
    Patient_By_Payment_Source.Outpatient_Private_Insurance as Out_Private_Insurance_Patients,
    Patient_By_Payment_Source.Outpatient_Private_Payment as Out_Private_Payment_Patients,
    Patient_By_Payment_Source.Outpatient_Other_Public_Payments as Out_Other_Payments_Patients,
    Patient_By_Payment_Source.Inpatient_Medicaid as In_Medicaid_Patients,
    Patient_By_Payment_Source.Inpatient_Medicare as In_Medicare_Patients,
    Patient_By_Payment_Source.Inpatient_Private_Insurance as In_Private_Insurance_Patients,
    Patient_By_Payment_Source.Inpatient_Private_Payment as In_Private_Payment_Patients,
    Patient_By_Payment_Source.Inpatient_Other_Public_Payment as In_Other_Payment_Patients
    
FROM
    Patient_By_Payment_Source
WHERE
	ID = %s """, [hospID])
		nums = cursor.fetchall()
		patientNums[x] = nums[0]
	
		cursor.execute("""SELECT 
    Revenue.Name,
    Revenue.ID,
    Revenue.Outpatient_Medicaid,
    Revenue.Outpatient_Medicare,
    Revenue.Outpatient_Private_Insurance,
    Revenue.Outpatient_Private_Payment,
    Revenue.Outpatient_Other_Public_Payment,
    Revenue.Inpatient_Medicaid,
    Revenue.Inpatient_Medicare,
    Revenue.Inpatient_Private_Insurance,
    Revenue.Inpatient_Private_Payment,
    Revenue.Inpatient_Other_Public_Payment
FROM
    Revenue
WHERE
	ID = %s """, [hospID])
		revs = cursor.fetchall()
		patientRevenue[x] = revs[0]
	
	#print(patientNums)
	#print(patientRevenue)

	
	typeRevs = {}
	typeNums = {}

	for typeP in typesOfPayments:
		typeRevs[typeP] = []
		typeNums[typeP] = []

	for y in years:
		for x in range(2,12):
			typeRevs[typesOfPayments[x-2]].append(patientRevenue[y][x])
			typeNums[typesOfPayments[x-2]].append(patientNums[y][x])
	
	# print(typeRevs)
	# print(typeNums)
	rxy = {}
	for typeP in typesOfPayments:
		avgR = 0
		avgN = 0
		for x in typeNums[typeP]:
			avgN = avgN + x
		for x in typeRevs[typeP]:
			avgR = avgR + x
		avgR = avgR/5
		avgN = avgN/5
		rxy[typeP] = corrCoef(request,float(avgN),float(avgR) ,typeNums[typeP],typeRevs[typeP],5)

	print(rxy)
	
	corrStatus = " "
	maxpaymentName = max(rxy, key=rxy.get)
	maxpaymentName = maxpaymentName.replace("_"," " )
	minpaymentName = min(rxy, key=rxy.get)
	minpaymentName = minpaymentName.replace("_"," " )


	initRank = str(calcRank(request,"2009"))
	finalRank = str(calcRank(request,"2013"))
	rankChange = "From " + initRank + " to " + finalRank

	isPOSTRequest = (request.method == "POST")
	dataOut = []

	paymentSelect = "Outpatient Medicaid Patients"
	if(isPOSTRequest):
		paymentSelect = str((request.POST.get('procSelect','')))
	
	
	firstNum = typeNums[paymentSelect][0]
	firstRev = typeRevs[paymentSelect][0]
	secondNum = typeNums[paymentSelect][1]
	secondRev = typeRevs[paymentSelect][1]
	thirdNum = typeNums[paymentSelect][2]
	thirdRev = typeRevs[paymentSelect][2]
	fourthNum = typeNums[paymentSelect][3]
	fourthRev = typeRevs[paymentSelect][3]
	fifthNum = typeNums[paymentSelect][4]
	fifthRev = typeRevs[paymentSelect][4]

	typeNums = [firstNum,secondNum,thirdNum,fourthNum,fifthNum]
	typeRevs = [firstRev,secondRev,thirdRev,fourthRev,fifthRev]

	avgNums = (firstNum + secondNum + thirdNum + fourthNum + fifthNum)/5
	avgRevs = (firstRev + secondRev + thirdRev + fourthRev+ fifthRev)/5
	print(typeNums)
	print(typeRevs)

	test = corrCoef(request,float(avgNums),float(avgRevs) ,typeNums,typeRevs,5)
	print("This is your coeff:" + str(test))

	title = paymentSelect + " Correlation"
	return render(request,'performance.html',locals())

def corrCoef(request,avgX,avgY,allX,allY,size):
	sX = 0
	sY = 0
	covXY = covariance(request,avgX,avgY,allX,allY,size)
	print("covXY: " + str(covXY))

	topX = 0
	topY = 0
	rxy = 0

	for x in range(0,len(allX)):
		topX = topX + math.pow(allX[x] - avgX,2)
	topX = topX / (size - 1)
	sX = math.sqrt(topX)

	for x in range(0,len(allY)):
		topY = topY + math.pow(allY[x] - avgY,2)
	topY = topY / (size - 1)
	sY = math.sqrt(topY)

	print('SX:' + str(sX))
	print('SY:' + str(sY))

	rxy = (covXY/(sX * sY))
	return rxy

def covariance(request,avgX,avgY,allX,allY, size):

	topCov = 0
	for x in range(0,size):
		topCov = topCov + ((allX[x] - avgX) * (allY[x] - avgY))
	print("topCov: " + str(topCov))
	covXY = topCov / (size -1)
	return covXY



def excelToDatabase(request,databaseName,filename):

	
	book = open_workbook(filename)

	#Sheet 0
	sheet0 = book.sheet_by_index(0)

	d_Hospital_Information = {}
	listID_0 = [str(s) for s in sheet0.col_values(0,3)]
	listID_0 = [float(s) for s in listID_0]
	    
	for row in range(len(listID_0)):
	    d_Hospital_Information[listID_0[row]] = [str(s) for s in sheet0.row_values(row+3,0)]

	for s in range(len(d_Hospital_Information)):
	    tmp_arr = []
	    for j in d_Hospital_Information[listID_0[s]]:
	        try:
	            str(tmp_arr.append(int(float(j))))
	        except:
	            tmp_arr.append(j)
	    d_Hospital_Information[listID_0[s]] = tmp_arr

	for j in range(len(listID_0)):
		tmp_arr2 = [k for k in d_Hospital_Information[listID_0[j]] if not k == ""]
		number = 9 - len(tmp_arr2)
		while(number>0):
			tmp_arr2.append("No Information")
			number = number - 1
		d_Hospital_Information[listID_0[j]] = tmp_arr2

	if(databaseName != '2013'):
		cursor = connections[databaseName].cursor()
	else:
		cursor = connection.cursor()

	for key in d_Hospital_Information.keys():
		try:
			cursor.execute("""INSERT INTO Information (ID, Name, Address, City, ZipCode, County, Ownership_Type,
	Specialized_Hospital_Characteristics, Hospital_Classification) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""", d_Hospital_Information[key])
			print("Inserted first " + d_Hospital_Information[key])
		except:
			hi = 0

	#Sheet 1
	sheet0 = book.sheet_by_index(1)

	d_Hospital_Information = {}
	listID_0 = [str(s) for s in sheet0.col_values(0,3)]
	listID_0 = [float(s) for s in listID_0]
	    
	for row in range(len(listID_0)):
	    d_Hospital_Information[listID_0[row]] = [str(s) for s in sheet0.row_values(row+3,0)]

	for s in range(len(d_Hospital_Information)):
	    tmp_arr = []
	    for j in d_Hospital_Information[listID_0[s]]:
	        try:
	            str(tmp_arr.append(int(float(j))))
	        except:
	            tmp_arr.append(j)
	    d_Hospital_Information[listID_0[s]] = tmp_arr

	for j in range(len(listID_0)):
	    tmp_arr2 = [k for k in d_Hospital_Information[listID_0[j]] if not k == ""]
	    number = 22 - len(tmp_arr2)
	    while(number>0):
	    	tmp_arr2.append("No Information")
	    	number = number - 1

	    d_Hospital_Information[listID_0[j]] = tmp_arr2


	if(databaseName != '2013'):
		cursor = connections[databaseName].cursor()
	else:
		cursor = connection.cursor()

	for key in d_Hospital_Information.keys():
		#print d_Hospital_Information[key]
		try:
			cursor.execute("""INSERT INTO Utilization (ID, Name, Medical_Surgical, Intensive_Care, Pediatric , Obstetrics_Gynecology ,
Long_Term_Care, Neonatal_ICU, Rehabilitation, Acute_Mental_Illness, Long_Term_Acute_Care, Authorized_Beds, _0_to_14_Admission,
_15_to_44_Admission, _45_to_64_Admission, _65_to_74_Admission, _75_Plus_Admission, _0_to_14_PDays, _15_to_44_PDays,	_45_to_64_PDays,
_65_to_74_PDays, _75_Plus_PDays) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", d_Hospital_Information[key][0:22])
			print("Inserted second " + d_Hospital_Information[key])
		except:
			hi = 0

			#Sheet 2
	sheet2 = book.sheet_by_index(2)

	d_Patient_By_Payment_Source = {}
	listID_2 = [str(s) for s in sheet2.col_values(0,3)]
	listID_2 = [float(s) for s in listID_2]

	for row in range(len(listID_2)):
	    d_Patient_By_Payment_Source[listID_2[row]] = [str(s) for s in sheet2.row_values(row+3,0)]

	for s in range(len(d_Patient_By_Payment_Source)):
	    tmp_arr = []
	    for j in d_Patient_By_Payment_Source[listID_2[s]]:
	        try:
	            tmp_arr.append(int(float(j)))        
	        except:
	            tmp_arr.append(j)
	    d_Patient_By_Payment_Source[listID_2[s]] = tmp_arr

	for j in range(len(listID_2)):
	    tmp_arr2 = [k for k in d_Patient_By_Payment_Source[listID_2[j]] if not k == ""]
	    d_Patient_By_Payment_Source[listID_2[j]] = tmp_arr2

	if(databaseName != '2013'):
		cursor = connections[databaseName].cursor()
	else:
		cursor = connection.cursor()

	for key in d_Patient_By_Payment_Source:
		try:
			cursor.execute("""INSERT INTO Patient_By_Payment_Source (
		ID, Name, Inpatient_Medicare , Inpatient_Medicaid ,	Inpatient_Other_Public_Payment , Inpatient_Private_Insurance , Inpatient_Private_Payment , Inpatient_Charity_Care ,	Outpatient_Medicare , Outpatient_Medicaid , Outpatient_Other_Public_Pyaments , Outpatient_Private_Insurance ,
		Outpatient_Private_Payment , Outpatient_Charity_Care) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", d_Patient_By_Payment_Source[key][0:14])
		except:
			hi = 0

#Sheet 0
	sheet0 = book.sheet_by_index(4)

	d_Hospital_Information = {}
	listID_0 = [str(s) for s in sheet0.col_values(0,3)]
	listID_0 = [float(s) for s in listID_0]
	    
	for row in range(len(listID_0)):
	    d_Hospital_Information[listID_0[row]] = [str(s) for s in sheet0.row_values(row+3,0)]

	for s in range(len(d_Hospital_Information)):
	    tmp_arr = []
	    for j in d_Hospital_Information[listID_0[s]]:
	        try:
	            str(tmp_arr.append(int(float(j))))
	        except:
	            tmp_arr.append(j)
	    d_Hospital_Information[listID_0[s]] = tmp_arr

	for j in range(len(listID_0)):
	    tmp_arr2 = [k for k in d_Hospital_Information[listID_0[j]] if not k == ""]
	    number = 125 - len(tmp_arr2)
	    while(number>0):
	    	tmp_arr2.append("No Information")
	    	number = number - 1

	    d_Hospital_Information[listID_0[j]] = tmp_arr2


	if(databaseName != '2013'):
		cursor = connections[databaseName].cursor()
	else:
		cursor = connection.cursor()

	for key in d_Hospital_Information.keys():
		try:
			cursor.execute("""INSERT INTO Surgery (ID, Name, General_Inpatient_OR , General_Outpatient_OR , General_Inpatient_Cases, General_Outpatient_Cases,
General_Inpatient_Surgery_Hours, General_Outpatient_Surgery_Hours, Ophthalmology_Inpatient_OR, Ophthalmology_Outpatient_OR, Ophthalmology_Inpatient_Cases,
Ophthalmology_Outpatient_Cases,	Ophthalmology_Inpatient_Surgery_Hours,	Ophthalmology_Outpatient_Surgery_Hours,	Cardiovascular_Inpatient_OR,
Cardiovascular_Outpatient_OR, Cardiovascular_Inpatient_Cases, Cardiovascular_Outpatient_Cases, Cardiovascular_Inpatient_Surgery_Hours,
Cardiovascular_Outpatient_Surgery_Hours, Dermatology_SurgeryInpatient_OR, Dermatology_SurgeryOutpatient_OR, Dermatology_SurgeryInpatient_Cases ,
Dermatology_SurgeryOutpatient_Cases, Dermatology_SurgeryInpatient_Surgery_Hours, Dermatology_SurgeryOutpatient_Surgery_Hours ,
Gastroenterology_Inpatient_OR ,	Gastroenterology_Outpatient_OR , Gastroenterology_Inpatient_Cases , Gastroenterology_Outpatient_Cases ,
Gastroenterology_Inpatient_Surgery_Hours ,  Gastroenterology_Outpatient_Surgery_Hours ,	Neurology_Inpatient_OR , Neurology_Outpatient_OR , Neurology_Inpatient_Cases ,
Neurology_Outpatient_Cases , Neurology_Inpatient_Surgery_Hours , Neurology_Outpatient_Surgery_Hours , Obstetric_Gynecology_Inpatient_OR ,
Obstetric_Gynecology_Outpatient_OR , Obstetric_Gynecology_Inpatient_Cases , Obstetric_Gynecology_Outpatient_Cases , Obstetric_Gynecology_Inpatient_Surgery_Hours ,
Obstetric_Gynecology_Outpatient_Surgery_Hours ,	Oral_Maxillofacia_Inpatient_OR , Oral_Maxillofacia_Outpatient_OR ,  Oral_Maxillofacia_Inpatient_Cases ,
Oral_Maxillofacia_Outpatient_Cases , Oral_Maxillofacia_Inpatient_Surgery_Hours , Oral_Maxillofacia_Outpatient_Surgery_Hours , Orthopedic_Inpatient_OR ,
Orthopedic_Outpatient_OR ,  Orthopedic_Inpatient_Cases , Orthopedic_Outpatient_Cases ,	Orthopedic_Inpatient_Surgery_Hours ,
Orthopedic_Outpatient_Surgery_Hours , Otolaryngology_Inpatient_OR , Otolaryngology_Outpatient_OR ,  Otolaryngology_Inpatient_Cases ,
Otolaryngology_Outpatient_Cases , Otolaryngology_Inpatient_Surgery_Hours ,  Otolaryngology_Outpatient_Surgery_Hours ,
Plastic_Inpatient_OR ,	Plastic_Outpatient_OR ,	Plastic_Inpatient_Cases , Plastic_Outpatient_Cases , Plastic_Inpatient_Surgery_Hours ,
Plastic_Outpatient_Surgery_Hours ,  Podiatry_Inpatient_OR , Podiatry_Outpatient_OR ,Podiatry_Inpatient_Cases ,	Podiatry_Outpatient_Cases ,
Podiatry_Inpatient_Surgery_Hours ,  Podiatry_Outpatient_Surgery_Hours ,	Thoracic_Inpatient_OR ,	Thoracic_Outpatient_OR ,
Thoracic_Inpatient_Cases ,  Thoracic_Outpatient_Cases ,	Thoracic_Inpatient_Surgery_Hours ,  Thoracic_Outpatient_Surgery_Hours ,	Urology_Inpatient_OR ,
Urology_Outpatient_OR ,	Urology_Inpatient_Cases , Urology_Outpatient_Cases ,	Urology_Inpatient_Surgery_Hours , Urology_Outpatient_Surgery_Hours)
VALUE (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )""",d_Hospital_Information[key][0:86])
			print("Inserted third " + d_Hospital_Information[key])
		except:
			hi = 0



	#Sheet 0
	sheet0 = book.sheet_by_index(5)

	d_Hospital_Information = {}
	listID_0 = [str(s) for s in sheet0.col_values(0,3)]
	listID_0 = [float(s) for s in listID_0]
	    
	for row in range(len(listID_0)):
	    d_Hospital_Information[listID_0[row]] = [str(s) for s in sheet0.row_values(row+3,0)]

	for s in range(len(d_Hospital_Information)):
	    tmp_arr = []
	    for j in d_Hospital_Information[listID_0[s]]:
	        try:
	            str(tmp_arr.append(int(float(j))))
	        except:
	            tmp_arr.append(j)
	    d_Hospital_Information[listID_0[s]] = tmp_arr

	for j in range(len(listID_0)):
	    tmp_arr2 = [k for k in d_Hospital_Information[listID_0[j]] if not k == ""]
	    number = 14 - len(tmp_arr2)
	    while(number>0):
	    	tmp_arr2.append("No Information")
	    	number = number - 1

	    d_Hospital_Information[listID_0[j]] = tmp_arr2


	if(databaseName != '2013'):
		cursor = connections[databaseName].cursor()
	else:
		cursor = connection.cursor()

	for key in d_Hospital_Information.keys():
		try:
			cursor.execute("""INSERT INTO Revenue (ID , Name, Inpatient_Medicaid ,  Inpatient_Medicare , Inpatient_Other_Public_Payment ,
Inpatient_Private_Insurance , Inpatient_Private_Payment , Inpatient_Charity_Care_Cost , Outpatient_Medicaid , Outpatient_Medicare ,
Outpatient_Other_Public_Payment , Outpatient_Private_Insurance , Outpatient_Private_Payment , Outpatient_Charity_Care_Cost)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", d_Hospital_Information[key][0:14])
			print("Inserted fourth " + d_Hospital_Information[key])
		except:
			hi = 0


		
		







