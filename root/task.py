from celery import task
# other imports

@task()
def patient1(request):

	#geolocator = Nominatim()
	#location = geolocator.geocode("Dupage hospital")
	api_key = 'AIzaSyB--XNP_v_U26cBpVbE8T3rm_HTe0PKxvU'
	#gmaps = GoogleMaps(api_key)
	#print(location.address)

	
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
	# 	key = name
	# 	data = cache.get(key)
	# 	print(name)
	# 	if data is None:

	# 		cmd = ['/usr/local/Cellar/casperjs/1.1-beta3/libexec/bin/casperjs', 'procedureCost.js',name]
	# 		cmdName = ['/usr/local/Cellar/casperjs/1.1-beta3/libexec/bin/casperjs', 'hospName.js',name]
	# 		try:
	# 			response = subprocess.check_output(cmd)
	# 			name = subprocess.check_output(cmdName)
	# 			Procedures = True
	# 		except:
	# 			hospNotFound = True
	# 			#return render(request,'patient.html',locals())
	# 		try:
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
	# 		except:
	# 			hi = 0
	

	if(requestType == "Search"):
		hospitalName = str(request.POST.get('hospInput',''))
		combined = cache.get(hospitalName)

	# elif(requestType == "Find"):
	# 	lowestCosts = []
	# 	zipCode = str(request.POST.get('inputZip',''))
	# 	procedure = str(request.POST.get('procSelect',''))
	# 	if(len(zipCode) != 5):
	# 		validZip = False
	# 		render(request,'patient.html',locals())

	# 	cmd = ['/usr/local/Cellar/casperjs/1.1-beta3/libexec/bin/casperjs', 'closestHospitals.js', zipCode]

	# 	try:
	# 		response = subprocess.check_output(cmd)

	# 	except:
	# 		validZip = False
	# 		return render(request,'patient.html',locals())

	# 	response = str(response)
	# 	response = re.sub('- Details', '', response)
	# 	response = re.sub('-','',response)
	# 	validHosps = []
	# 	closestNamesList = [y for y in (x.strip() for x in response.splitlines()) if y]
	# 	cmd = ['/usr/local/Cellar/casperjs/1.1-beta3/libexec/bin/casperjs', 'lowestCost.js']
	# 	finalProc = procedure
	# 	procedure = procedure.replace(" ", "")
	# 	procedure = procedure.replace("/", "")
	# 	print(procedure)
	# 	procedure = ' a[href = "/glossaries/index/#MedianCharges' + procedure + '"] span' 
	# 	#procedure = "' a[href = " + '"/glossaries/index/#MedianCharges' + procedure + '"]' + " span'"
	# 	#' a[href = "/glossaries/index/#MedianChargesArthroscopy"] span'
	# 	print(procedure)
	# 	print(closestNamesList)
	# 	blacklist = ["N/A", "too few cases", "too cases"]
	# 	for name in closestNamesList:
	# 		cmd = ['/usr/local/Cellar/casperjs/1.1-beta3/libexec/bin/casperjs', 'lowestCost.js',name,procedure]
	# 		try:
	# 			lowestCosts.append(subprocess.check_output(cmd))
	# 			#lowestCosts[name] = ["$" + k for k in ((subprocess.check_output(cmd))).split('$') if not k == ""]
	# 			# for i in blacklist:
	# 			# 	tmp_arr = []
	# 			# 	for k in lowestCosts[name]:
	# 			# 		if(not i in k):
	# 			# 			tmp_arr.append(k)
	# 			# 		else:
	# 			# 			tmp_arr.append(k[0:k.index(i)])
	# 			# 			tmp_arr.append(i)
	# 			# 	lowestCosts[name] = tmp_arr
	# 			# 	print 'e'

	# 			validHosps.append(name)
	# 			print(lowestCosts)
	# 		except subprocess.CalledProcessError as e:
	# 			#print e.output
	# 			hi = 0
	# 	for x in range(0,len(lowestCosts)):
	# 		if(lowestCosts[x] == "N/A\n" or lowestCosts[x] == 'N/AN/A\n' or lowestCosts[x] == 'too few cases\n' or lowestCosts[x] == "oo few cases" or lowestCosts[x] == 'too few\n'):
	# 			lowestCosts[x] = "1000000000"
	# 		else:
	# 			lowestCosts[x] = lowestCosts[x][1:]
	# 			lowestCosts[x] = lowestCosts[x].replace(",", "")
	# 		#lowestCosts[x] = lowestCosts[x][:-3]
	# 		print(lowestCosts[x])
	# 	index = 0
	# 	smallestVal = float(lowestCosts[0])
	# 	for x in range(0,len(lowestCosts)):
	# 		if(smallestVal > float(lowestCosts[x])):
	# 			smallestVal = float(lowestCosts[x])
	# 	print(smallestVal)
	# 	for x in range(0,len(lowestCosts)):
	# 		if(float(lowestCosts[x]) == smallestVal):
	# 			index = x
	# 	bestHospital = validHosps[index]
	# 	foundBest = True

	# 	if( all(i == "1000000000" for i in lowestCosts)):
	# 		bestHospital = "Not enough data"
	# 		smallestVal = "Not enough data"