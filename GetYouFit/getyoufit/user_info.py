import psycopg2
from math import floor


dbName = "dcjdhd0n3ngqo0"
dbHost = "ec2-54-225-173-42.compute-1.amazonaws.com"
dbUser = "asfmhdygmsibfb"
dbPassword = "d57768a0ac5b6f7313d2173a9b8179443465c3515448f2b6b11d806a7a11047b"

def get_profile_info(username):
	data = {'username': username}
	try:
		conn = psycopg2.connect(database=dbName, password = dbPassword, user=dbUser, host=dbHost)

		cursor = conn.cursor()
	
		cursor.execute("SELECT * FROM users WHERE username = '" + username + "'")
		rows = cursor.fetchall()
		
		if cursor.rowcount == 1:
			data['password'] = rows[0][1]
			data['age'] = rows[0][2]
			data['height1'] = floor(rows[0][3]/12)
			data['height2'] = int(rows[0][3]%12)
			data['weight'] = rows[0][4]
			data['gender'] = rows[0][5]
			
	except Exception as ex:
		print("Not connected: " + type(ex).__name__)

	
	return data

def update_profile_info(data):
	
	message = "Unable to update user profile"
	isValid = False

	try:
		conn = psycopg2.connect(database=dbName, password = dbPassword, user=dbUser, host=dbHost)

		cursor = conn.cursor()

		height = data['height1']*12 + data['height2']
			
		
		cursor.execute("UPDATE users SET pword=%s, age=%s, height=%s, weight=%s, gender=%s WHERE username = %s", (data['password'], str(data['age']), str(height), str(data['weight']), data['gender'], data['username']))
		
		conn.commit()

		message = "User profile successfully updated"
		isValid = True

	except Exception as ex:
		print("Not connected: ", ex)
		print("Not connected: " + type(ex).__name__)

	return [isValid, message]
