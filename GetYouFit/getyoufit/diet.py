import psycopg2
import datetime

dbName = "dcjdhd0n3ngqo0"
dbHost = "ec2-54-225-173-42.compute-1.amazonaws.com"
dbUser = "asfmhdygmsibfb"
dbPassword = "d57768a0ac5b6f7313d2173a9b8179443465c3515448f2b6b11d806a7a11047b"

def retrieveDietEntries(info, username, index):
	startDate = info['startDate']
	endDate = info['endDate']
	
	message = "<p>No entries found</p>"
	total = ""
	
	print("heyad")


	if not index:
		print("no-------------------------------------")
		if not info['showAll']:
			if type(startDate).__name__ == "NoneType":
				return ["<p class='message'>Error: missing start date</p>", ""]
	
			if type(endDate).__name__ == "NoneType":
				return ["<p class='message'>Error: missing end date</p>", ""]
			if startDate.year > endDate.year or (startDate.year == endDate.year and startDate.month > endDate.month) or (startDate.year == endDate.year and startDate.month == endDate.month and startDate.day > endDate.day):
				return ["<p class='message'>Error: the start date must be before the end date</p>", ""]


	try:
		conn = psycopg2.connect(database=dbName, password = dbPassword, user=dbUser, host=dbHost)

		cursor = conn.cursor()
	
		print("All status:", info['showAll'])
		if not index:
			print("no2-------------------------------------")
			if info['showAll']:
				cursor.execute("SELECT * FROM LogEntry INNER JOIN DietEntry ON LogEntry.logdate = DietEntry.logdate WHERE LogEntry.username = %s AND DietEntry.username = %s ORDER BY LogEntry.logdate", (username, username))
			else:
				cursor.execute("SELECT * FROM LogEntry INNER JOIN DietEntry ON LogEntry.logdate = DietEntry.logdate WHERE LogEntry.username = %s AND DietEntry.username = %s AND LogEntry.logdate BETWEEN %s AND %s ORDER BY LogEntry.logdate", (username, username, info['startDate'].strftime('%Y-%m-%d'), info['endDate'].strftime('%Y-%m-%d')))
		else:
			cursor.execute("SELECT * FROM LogEntry INNER JOIN DietEntry ON LogEntry.logdate = DietEntry.logdate WHERE LogEntry.username = %s AND DietEntry.username = %s AND LogEntry.logdate BETWEEN %s AND %s ORDER BY LogEntry.logdate", (username, username, info['startDate'].strftime('%Y-%m-%d'), info['endDate'].strftime('%Y-%m-%d')))
		
		rows = cursor.fetchall()
		print(info['startDate'])
		print(cursor.rowcount)
		
		prevDate = rows[0][0]
		message = "<div class='Diet-Entry'><div class='close-button'>X</div><h3>Date: " + prevDate.strftime("%m/%d/%Y") + "</h3>"
		dayTotal = 0
		overallTotal = 0
		for row in rows:
			currentDate = row[0]
			if prevDate != currentDate:
				message += "<p class='Diet-Final-Tally'>Total calories: " + str(dayTotal)+ "</p></div><div class='Diet-Entry'><div class='close-button'>X</div><h3>Date: " + currentDate.strftime("%m/%d/%Y") + "</h3>"
				overallTotal += dayTotal
				dayTotal = 0
				prevDate = currentDate
			message += "<div class='Diet-Sub-Entry'><div class='close-button'>X</div><div class='edit-button'>+</div><p>Food: <span class='editable'>" + row[2]+ "</span></p><p>Calories: <span class='editable'>" + str(row[3]) + "</span></p></div>"
			dayTotal += row[3]
		message += "<p class='Diet-Final-Tally'>Total Calories: " + str(dayTotal)+ "</p></div>"
		overallTotal += dayTotal
		total = "<p class='message' style='font-size:1.2em; font-weight:bold;'> The total number of calories consumed in the given time period is " + str(overallTotal) + " calories</p>"

	except Exception as ex:
		print("Not connected: ", ex)
		print("Not connected: " + type(ex).__name__)
		message = "<p>No entries found</p>"


	#print("message:",message)
	return [message, total]

def createDietEntry(info, username):
	
	message = "<p>Unable to create entry</p>"

	try:
		conn = psycopg2.connect(database=dbName, password = dbPassword, user=dbUser, host=dbHost)

		cursor = conn.cursor()
		
		# check to see if an entry for the entered date already exists
		cursor.execute("SELECT * FROM LogEntry WHERE username = %s AND logdate = %s", (username, info['date']))
		rows = cursor.fetchall()

		if cursor.rowcount == 0:
			cursor.execute("INSERT INTO LogEntry(logdate, username) VALUES(%s, %s)", (info['date'], username))
		
		cursor.execute("INSERT INTO DietEntry(food, calories, logdate, username) VALUES(%s, %s, %s, %s)", (info['food'], info['calories'], info['date'], username))

		conn.commit()
		message = "New entry successfully created"
	except Exception as ex:
		print("Not connected: ", ex)
		print("Not connected: " + type(ex).__name__)
		message = "<p>No entries found</p>"

	return message

def updateDietEntry(info, username):
	
	message = "<p class='message'>No entries found</p>"
	total = ""
	

	try:
		conn = psycopg2.connect(database=dbName, password = dbPassword, user=dbUser, host=dbHost)

		cursor = conn.cursor()
		
		#print("editing...........................")
		#print("food:", info['food'], "calories:", info['calories'], "username:", username, "date:", info['date'], " old food:", oldInfo['food'], "old calories:", oldInfo['calories'])

		cursor.execute("UPDATE DietEntry SET food=%s, calories=%s WHERE username = %s AND logdate = %s AND food = %s AND calories = %s", (info['food'], info['calories'], username, info['date'], info['oldFood'], info['oldCalories']))
	
		conn.commit()
		message = "<p class='message'>Entry successfully updated</p>"

	except Exception as ex:
		print("Not connected: ", ex)
		print("Not connected: " + type(ex).__name__)
		message = "<p>No entries found</p>"

	return message

def deleteDietEntry(info, username):
	
	message = "<p class='message'>Unable to delete entry</p>"
	total = ""
	

	try:
		conn = psycopg2.connect(database=dbName, password = dbPassword, user=dbUser, host=dbHost)

		cursor = conn.cursor()
		
		print("value:",info['single'])
		if info['single'] == 'day':
			cursor.execute("DELETE FROM DietEntry WHERE username = %s AND logdate = %s AND food = %s AND calories = %s", (username, info['date'], info['food'], info['calories']))
		else:
			cursor.execute("DELETE FROM DietEntry WHERE username = %s AND logdate = %s", (username, info['date']))
		
	
		conn.commit()
		message = "<p class='message'>Entry successfully deleted</p>"

	except Exception as ex:
		print("Not connected: ", ex)
		print("Not connected: " + type(ex).__name__)

	return message
