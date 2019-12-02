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
		print("--Start---")
		cursor.execute("SELECT * FROM users WHERE username = '" + username+ "'")
		rows = cursor.fetchall()
		
		print("--After---")
		if cursor.rowcount == 1:
			data['password'] = rows[0][1]
			data['age'] = rows[0][2]
			data['height1'] = floor(rows[0][3]/12)
			data['height2'] = int(rows[0][3]%12)
			data['weight'] = rows[0][4]
			data['gender'] = rows[0][5]
		
		print("--Start 2---")
		cursor.execute("SELECT * FROM PreferenceList WHERE username = '" + username +"'")
		rows = cursor.fetchall()
		print("--After 2---")
		
		if cursor.rowcount == 1:
			data['skillLevel'] = rows[0][1]
			data['caloriegoal'] = rows[0][2]

	except Exception as ex:
		print("Not connected: ", ex)
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
		
		cursor.execute("UPDATE PreferenceList SET skilllevel=%s, caloriegoal=%s WHERE username = %s", (data['skillLevel'], str(data['calorieGoal']), data['username']))
		conn.commit()

		message = "User profile successfully updated"
		isValid = True

	except Exception as ex:
		print("Not connected: ", ex)
		print("Not connected: " + type(ex).__name__)

	return [isValid, message]

def retrieveCalorieInfo(username):

	message = ""

	try:
		conn = psycopg2.connect(database=dbName, password = dbPassword, user=dbUser, host=dbHost)

		cursor = conn.cursor()
		cursor.execute("SELECT SUM(calories) FROM DietEntry WHERE username = '" + username + "'")
		
		consumed = cursor.fetchall()[0][0]
		print("consumed:",consumed)

		cursor.execute("SELECT SUM(caloriesburned) FROM WorkoutEntry WHERE username = '" + username + "'")

		burned = cursor.fetchall()[0][0]
		print("burned:",burned)
		
		cursor.execute("SELECT * FROM PreferenceList WHERE username = '" + username +"'")
		goal = cursor.fetchall()[0][2]

		difference = consumed - burned
		
		net = "<span class='bad'>+" + str(difference) +"</span>"
		status = "<span class='bad'>You have not met your goal yet. You still need to burn " + str(goal+difference) + " calories</span>"

		if difference <= 0:
			net = "<span class='good'>" + str(difference) +"</span>"

		if (goal + difference) <= 0:
			status = "<span class='good'>You have met your goal! You have burned " + str((goal + difference)*(-1)) + " calories past your desired goal.</span>"

		message = "<div class='calorie-message'><p><strong>Current calorie goal:</strong> " + str(goal) + "</p><p><strong>Total calories consumed:</strong> " + str(consumed) + "</p><p><strong>Total calories burned:</strong> " + str(burned) +"</p><p><strong>Net calorie gain/loss:</strong> " + net + "</p></div><p class='message' style='font-size:1.2em;'>" + status + "</p>"

	except Exception as ex:
		print("Not connected: ", ex)
		print("Not connected: " + type(ex).__name__)

	
	return message
