import psycopg2


dbName = "GetYouFit"
dbHost = "localhost"
dbUser = "getyoufit"
dbPassword = "test123"

def login(info):
	info = info.split(";")
	username = info[0]
	password = info[1]

	returnString = "Not logged in"
	
	try:
		conn = psycopg2.connect(database=dbName, password = dbPassword, user=dbUser, host=dbHost)
		#print("Connected")

		cursor = conn.cursor()

		cursor.execute("SELECT * FROM users WHERE username = '" + username + "'")
		rows = cursor.fetchall()
		#print(cursor.rowcount)	
		if cursor.rowcount > 0:
			returnString = "logged in"
	except Exception as ex:
		print("Not connected: " + type(ex).__name__)

	return returnString
