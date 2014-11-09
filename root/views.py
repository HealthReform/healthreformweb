from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.db import connection
from django.db import IntegrityError

# Create your views here.

def home(request):

	IDTaken = False
	notInt = False
	match = True

	isPOSTRequest = (request.method == "POST")
	requestType = request.POST['action'] if isPOSTRequest else None
	cursor = connection.cursor()


	if isPOSTRequest:
		if(requestType == "Login"):

			hospID = request.POST.get('username','')
			password = request.POST.get('password','')

			cursor.execute('SELECT ID FROM User WHERE ID = %s AND Password = %s ', [hospID,password])
			output = cursor.fetchone()

			if(output != None):
				request.session['member_id'] = output[0]
				return redirect('main')
			else:
				match = False
				return render(request,"index.html",locals())

		if(requestType == "Register"):

			hospname = request.POST.get('hospName','')
			hospid = request.POST.get('hospID','')
			password = request.POST.get('password','')

			#Check first if ID is a valid number, continue if so , otherwise return page with warning
			if(hospid.isdigit() == False):
				notInt = True
				return render(request,"index.html",locals())

			#Convert to SQL command based on inputs from login form
			raw_sql = "INSERT INTO User (Id, Name, Email, Password) VALUES ("
			sql_vals = [int(float(hospid)), '\"'+hospname+'\"', '\"'+''+'\"', '\"'+password+'\"']
			raw_sql += "%d, " %sql_vals[0]
			for i in range(1, len(sql_vals)):
				raw_sql = raw_sql + str(sql_vals[i])
				if (i < len(sql_vals) - 1):
				 raw_sql = raw_sql + ", "
			raw_sql = raw_sql + ");"

			#cursor.execute("INSERT INTO User (Id, Name, Email, Password) VALUES (2,'name','email','password')")
			#Execute SQL code and if ID is not unique then reload page with warning
			try:
				cursor.execute(raw_sql)
			except IntegrityError as e:
				IDTaken = True
				return render(request,"index.html",locals())

			request.session['member_id'] = hospid
			return redirect('main')
		

	return render(request,'index.html',locals())

def main(request):

	isPOSTRequest = (request.method == "POST")
	requestType = request.POST['action'] if isPOSTRequest else None	

	if(requestType == "Logout"):
		del request.session['member_id']
		return redirect('home')

	hospName = ''
	cursor = connection.cursor()
	hospID = request.session['member_id']
	cursor.execute('SELECT Name FROM User WHERE ID = %s', [hospID])
	print hospID
	hospName = cursor.fetchone()[0]
	hospName = (hospName + " Hospital").title()
	return render(request,'home.html',locals())

def account(request):

	cursor = connection.cursor()
	hospID = request.session['member_id']


	fieldsComplete = True
	success = False
	IDTaken = False
	notInt = False

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
				cursor.execute("UPDATE User SET Name = %s, Password = %s, ID = %s, Email = %s WHERE ID = %s", [name,passw,id,email,hospID])
				del request.session['member_id']
				request.session['member_id'] = id
				hospID = request.session['member_id']
				success = True
			except IntegrityError as e:
				IDTaken = True
				return render(request,'account.html',locals())
			


	elif(requestType == "Delete Account"):
		cursor.execute('DELETE FROM User Where ID = %s', [hospID])
		del request.session['member_id']
		return redirect('home')

	elif(requestType == "Log out"):
		del request.session['member_id']
		return redirect('home')

	cursor.execute('SELECT * FROM User WHERE ID = %s', [hospID])

	allInfo = cursor.fetchone()
	ID = allInfo[0]
	Name = allInfo[1]
	Email = allInfo[2]
	Password = allInfo[3]

	

	return render(request,'account.html',locals())