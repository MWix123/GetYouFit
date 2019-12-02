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

	if startDate.year > endDate.year or (startDate.year == endDate.year and startDate.month > endDate.month) or (startDate.year == endDate.year and startDate.month == endDate.month and startDate.day > endDate.day):
		return "<p class='message'>Error: the start date must be before the end date</p>"


	try:
		conn = psycopg2.connect(database=dbName, password = dbPassword, user=dbUser, host=dbHost)

		cursor = conn.cursor()
		
		cursor.execute("SELECT * FROM LogEntry LEFT JOIN WorkoutEntry ON LogEntry.logdate = WorkoutEntry.logdate LEFT JOIN StrengthExercise ON WorkoutEntry.exerciseid = StrengthExercise.exerciseid LEFT JOIN RunningExercise ON WorkoutEntry.exerciseid = RunningExercise.exerciseid WHERE LogEntry.username = %s AND LogEntry.logdate BETWEEN %s AND %s AND WorkoutEntry.exerciseid IS NOT NULL ORDER BY LogEntry.logdate", (username, info['startDate'].strftime('%Y-%m-%d'), info['endDate'].strftime('%Y-%m-%d')))


		rows = cursor.fetchall()
		
		prevDate = rows[0][0]
		print(prevDate)
		message = "<div class='Diet-Entry'><h3>Date: " + prevDate.strftime("%m/%d/%Y") + "</h3>"
		print("after")
		dayTotal = 0
		overallTotal = 0
		for row in rows:
			print(row)
			currentDate = row[0]
			if prevDate != currentDate:
				message += "<p class='Diet-Final-Tally'>Total calories: " + str(dayTotal)+ "</p></div><div class='Diet-Entry'><h3>Date: " + currentDate.strftime("%m/%d/%Y") + "</h3>"
				overallTotal += dayTotal
				dayTotal = 0
				prevDate = currentDate
			
			if type(row[2]).__name__ == "int":
				message += "<div class='Diet-Sub-Entry'><p>Exercise: " + row[3] + "</p><p>Calories burned: " + str(row[4]) + "</p>"
				dayTotal += row[4]

				print(row[7],":",type(row[7]).__name__)
				if type(row[7]).__name__ == "int":
					message += "<p>Muscle: " + row[8]+ "</p><p>Weight: " + str(row[9])+ "</p><p>Repetitions: " + str(row[10]) + "</p>"
				else:
					print(row[12])
					message += "<p>Duration: " + row[12].strftime('%H:%M:%S')+ "</p><p>Distance: " + str(row[13]) + "</p>"

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
		cursor.execute("SELECT * FROM WorkoutEntry WHERE username = %s AND logdate = %s", (username, info['date']))
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
