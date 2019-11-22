import psycopg2


dbName = "dcjdhd0n3ngqo0"
dbHost = "ec2-54-225-173-42.compute-1.amazonaws.com"
dbUser = "asfmhdygmsibfb"
dbPassword = "d57768a0ac5b6f7313d2173a9b8179443465c3515448f2b6b11d806a7a11047b"

def login(info):
	info = info.split(";")
	username = info[0]
	password = info[1]

	returnString = "Not logged in"
	
	try:
		conn = psycopg2.connect(database=dbName, password = dbPassword, user=dbUser, host=dbHost)
		#print("Connected")

		cursor = conn.cursor()
	
		#cursor.execute("CREATE TABLE users (username VARCHAR(50) PRIMARY KEY, pword VARCHAR(100) NOT NULL, age INT, height FLOAT, weight FLOAT, gender CHAR(1))")
		#returnString= "Table created"
		
		#cursor.execute("INSERT INTO users(username, pword) VALUES('" + username + "', '" + password + "')")
		#returnString = "User: " + username + " entered successfully"
		
		cursor.execute("SELECT * FROM users WHERE username = '" + username + "'")
		rows = cursor.fetchall()
		#print(cursor.rowcount)	
		if cursor.rowcount > 0:
			returnString = "logged in"
		else:
			returnString += " username: " + username + " password: " + password
		
	except Exception as ex:
		returnString += ": " + type(ex).__name__
		print("Not connected: " + type(ex).__name__)

	return returnString
