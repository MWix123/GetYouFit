import psycopg2


dbName = "dcjdhd0n3ngqo0"
dbHost = "ec2-54-225-173-42.compute-1.amazonaws.com"
dbUser = "asfmhdygmsibfb"
dbPassword = "d57768a0ac5b6f7313d2173a9b8179443465c3515448f2b6b11d806a7a11047b"

def loginUser(info):
	print("Login Function")
	info = info.split(";")
	username = info[0]
	password = info[1]

	returnString = "Not logged in"

	try:
		conn = psycopg2.connect(database=dbName, password = dbPassword, user=dbUser, host=dbHost)

		cursor = conn.cursor()
	
		
		cursor.execute("SELECT * FROM users WHERE username = '" + username + "' AND pword = '" + password + "'")
		rows = cursor.fetchall()
		
		if cursor.rowcount > 0:
			returnString = "logged in"
		else:
			returnString += " username: " + username + " password: " + password
		
	except Exception as ex:
		returnString += ": " + type(ex).__name__
		print("Not connected: " + type(ex).__name__)

	return returnString


def createUser(info):

	returnString = "Error, unable to create new user"
	isValid = False
	
	try:
		conn = psycopg2.connect(database=dbName, password = dbPassword, user=dbUser, host=dbHost)

		cursor = conn.cursor()
		

		age = 0
		if info['age'] != None:
			age = info['age']

		height = 0
		if info['height1'] != None and info['height2'] != None:
			height = info['height1']*12 + info['height2']

		weight = 0
		if info['weight'] != None:
			weight = info['weight']
		
		gender = info['gender']
		
		cursor.execute("INSERT INTO users(username, pword, age, height, weight, gender) VALUES('" + info['username'] + "', '" + info['password1'] + "', " + str(age) + ", " + str(height) + ", " + str(weight) + ", '" + gender + "')")
		cursor.execute("INSERT INTO PreferenceList(username) VALUES('" + info['username'] + "')")
		
		conn.commit()

		returnString = "New user sucessfully created"
		isValid = True
	except Exception as ex:
		print("Not connected: " + type(ex).__name__)
		if type(ex).__name__ == "UniqueViolation":
			returnString = "Username already taken"

	return [isValid, returnString]
