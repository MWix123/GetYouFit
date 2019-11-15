import psycopg2

dbName = "GetYouFit"
dbUser = "getyoufit"
dbPassword = "test123"
dbHost = "localhost"
#dbPort = "5432"

try:
	conn = psycopg2.connect(database=dbName, password = dbPassword, user=dbUser, host=dbHost)
	print("Connected")

	cursor = conn.cursor()

	cursor.execute("SELECT * FROM users;")
	rows = cursor.fetchall()
	for row in rows:
		print(row)
except Exception as ex:
	print("Not connected: " + type(ex).__name__)
