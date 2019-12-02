import psycopg2
import datetime

dbName = "dcjdhd0n3ngqo0"
dbHost = "ec2-54-225-173-42.compute-1.amazonaws.com"
dbUser = "asfmhdygmsibfb"
dbPassword = "d57768a0ac5b6f7313d2173a9b8179443465c3515448f2b6b11d806a7a11047b"

def retrieveWorkoutEntries(info, username):
	startDate = info['startDate']
	endDate = info['endDate']
	
	message = "<p>No entries found</p>"
	total = ""
	

	if not info['showAll']:
		if type(startDate).__name__ == "NoneType":
			return ["<p class='message'>Error: missing start date</p>", ""]
	
		if type(endDate).__name__ == "NoneType":
			return ["<p class='message'>Error: missing end date</p>", ""]
		if startDate.year > endDate.year or (startDate.year == endDate.year and startDate.month > endDate.month) or (startDate.year == endDate.year and startDate.month == endDate.month and startDate.day > endDate.day):
			return "<p class='message'>Error: the start date must be before the end date</p>"


	try:
		conn = psycopg2.connect(database=dbName, password = dbPassword, user=dbUser, host=dbHost)

		cursor = conn.cursor()
		
		if info['showAll']:
			cursor.execute("SELECT * FROM LogEntry LEFT JOIN WorkoutEntry ON LogEntry.logdate = WorkoutEntry.logdate LEFT JOIN StrengthExercise ON WorkoutEntry.exerciseid = StrengthExercise.exerciseid LEFT JOIN RunningExercise ON WorkoutEntry.exerciseid = RunningExercise.exerciseid WHERE LogEntry.username = '" + username + "' AND WorkoutEntry.exerciseid IS NOT NULL ORDER BY LogEntry.logdate")
		else:
			cursor.execute("SELECT * FROM LogEntry LEFT JOIN WorkoutEntry ON LogEntry.logdate = WorkoutEntry.logdate LEFT JOIN StrengthExercise ON WorkoutEntry.exerciseid = StrengthExercise.exerciseid LEFT JOIN RunningExercise ON WorkoutEntry.exerciseid = RunningExercise.exerciseid WHERE LogEntry.username = %s AND LogEntry.logdate BETWEEN %s AND %s AND WorkoutEntry.exerciseid IS NOT NULL ORDER BY LogEntry.logdate", (username, info['startDate'].strftime('%Y-%m-%d'), info['endDate'].strftime('%Y-%m-%d')))


		rows = cursor.fetchall()
		
		prevDate = rows[0][0]
		
		message = "<div class='Diet-Entry'><div class='close-button'>X</div><h3>Date: " + prevDate.strftime("%m/%d/%Y") + "</h3>"
		dayTotal = 0
		overallTotal = 0
		for row in rows:
			print("Row:",row)
			currentDate = row[0]
			if prevDate != currentDate:
				message += "<p class='Diet-Final-Tally'>Total calories: " + str(dayTotal)+ "</p></div><div class='Diet-Entry'><div class='close-button'>X</div><h3>Date: " + currentDate.strftime("%m/%d/%Y") + "</h3>"
				overallTotal += dayTotal
				dayTotal = 0
				prevDate = currentDate
			
			if type(row[2]).__name__ == "int":
				message += "<div class='Diet-Sub-Entry'><div class='close-button'>X</div><div class='edit-button'>+</div><p>Exercise: <span class='editable'>" + row[3] + "</span></p><p>Calories burned: <span class='editable'>" + str(row[4]) + "</span></p>"
				dayTotal += row[4]

				print("Row 7:",row[7],":",type(row[7]).__name__)
				if type(row[7]).__name__ == "int":
					message += "<p>Muscle: <span class='editable'>" + row[8]+ "</span></p><p>Weight: <span class='editable'>" + str(row[9])+ "</span></p><p>Repetitions: <span class='editable'>" + str(row[10]) + "</span></p><p class='hidden'>" + str(row[7]) + "</p>"
				else:
					print("Row 12:",row[12])
					message += "<p>Duration: <span class='editable'>" + row[12].strftime('%H:%M:%S')+ "</span></p><p>Distance: <span class='editable'>" + str(row[13]) + "</span></p><p class='hidden'>" + str(row[11]) + "</p>"

				message += "</div>"
		
		# finished
		message += "<p class='Diet-Final-Tally'>Total Calories: " + str(dayTotal)+ "</p></div>"
		overallTotal += dayTotal
		total = "<p class='message' style='font-size:1.2em; font-weight:bold;'> The total number of calories burned in the given time period is " + str(overallTotal) + " calories</p>"

	except Exception as ex:
		print("Not connected: ", ex)
		print("Not connected: " + type(ex).__name__)
		message = "<p>No entries found</p>"


	return [message, total]

def createWorkoutEntry(info, username):
	
	message = "Unable to create a new entry"

	try:
		conn = psycopg2.connect(database=dbName, password = dbPassword, user=dbUser, host=dbHost)

		cursor = conn.cursor()
		
		# check to see if an entry for the entered date already exists
		cursor.execute("SELECT * FROM LogEntry WHERE username = %s AND logdate = %s", (username, info['date']))
		rows = cursor.fetchall()

		if cursor.rowcount == 0:
			cursor.execute("INSERT INTO LogEntry(logdate, username) VALUES(%s, %s)", (info['date'], username))
		
		cursor.execute("INSERT INTO WorkoutEntry(exercisename, caloriesburned, logdate, username) VALUES(%s, %s, %s, %s)", (info['exerciseName'], str(info['calories']), info['date'], username))
		cursor.execute("SELECT * FROM WorkoutEntry WHERE username = %s AND logdate = %s ORDER BY exerciseid DESC", (username, info['date']))
		exerciseId = cursor.fetchone()[0]

		if info['typeForm'] == 'Strength':
			cursor.execute("INSERT INTO StrengthExercise(exerciseid, muscle, weight, repetitions) VALUES(%s, %s, %s, %s)", (exerciseId, info['muscle'], str(info['weight']), str(info['repetitions'])))
		else:
			cursor.execute("INSERT INTO RunningExercise(exerciseid, duration, distance) VALUES(%s, %s, %s)", (exerciseId, info['duration'], str(info['distance'])))

		
		conn.commit()
		message = "New entry successfully created"
	except Exception as ex:
		print("Not connected: ", ex)
		print("Not connected: " + type(ex).__name__)

	return message

def editWorkoutEntry(info, username):
	
	message = "<p>No entries found</p>"

	try:
		conn = psycopg2.connect(database=dbName, password = dbPassword, user=dbUser, host=dbHost)

		cursor = conn.cursor()

		print("exercise id:", info['exerciseId'], "username:",username,"date:", info['date'])

		cursor.execute("UPDATE WorkoutEntry SET exercisename = %s, caloriesburned = %s WHERE WorkoutEntry.username = %s AND WorkoutEntry.logdate = %s AND WorkoutEntry.exerciseid = %s", (info['exerciseName'], info['calories'], username, info['date'], info['exerciseId']))
		
		if info['typeForm'] == 'Strength':
			cursor.execute("UPDATE StrengthExercise SET muscle = %s, weight = %s, repetitions = %s WHERE StrengthExercise.exerciseid = %s", (info['muscle'], info['weight'], info['repetitions'], info['exerciseId']))
		else:
			cursor.execute("UPDATE RunningExercise SET duration = %s, distance = %s WHERE RunningExercise.exerciseid = %s", (info['duration'], info['distance'], info['exerciseId']))
			

		conn.commit()
		message = "<p class='message'>Entry successfully updated</p>"

	except Exception as ex:
		print("Not connected: ", ex)
		print("Not connected: " + type(ex).__name__)
		message = "<p>No entries found</p>"


	return message

def deleteWorkoutEntry(info, username):
	
	message = "<p>No entries found</p>"

	try:
		conn = psycopg2.connect(database=dbName, password = dbPassword, user=dbUser, host=dbHost)

		cursor = conn.cursor()
		
		print("exercise id:", info['exerciseId'])
		
		if info['single'] == "day":
			print("u:",username)
			cursor.execute("DELETE FROM WorkoutEntry WHERE WorkoutEntry.username = %s AND WorkoutEntry.logdate = %s", (username, info['date']))
		else:
			cursor.execute("DELETE FROM WorkoutEntry WHERE WorkoutEntry.username = %s AND WorkoutEntry.logdate = %s AND WorkoutEntry.exerciseid = %s", (username, info['date'], str(info['exerciseId'])))

		if info['exerciseId'] != 0:
			print("Shouold not be here")
			cursor.execute("DELETE FROM StrengthExercise WHERE StrengthExercise.exerciseid = %s", (str(info['exerciseId'])))
			cursor.execute("DELETE FROM RunningExercise WHERE RunningExercise.exerciseid = %s", (str(info['exerciseId'])))
			

		conn.commit()
		message = "<p class='message'>Entry successfully updated</p>"

	except Exception as ex:
		print("Not connected: ", ex)
		print("Not connected: " + type(ex).__name__)
		message = "<p>No entries found</p>"


	return message
