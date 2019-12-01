import psycopg2
import datetime

dbName = "dcjdhd0n3ngqo0"
dbHost = "ec2-54-225-173-42.compute-1.amazonaws.com"
dbUser = "asfmhdygmsibfb"
dbPassword = "d57768a0ac5b6f7313d2173a9b8179443465c3515448f2b6b11d806a7a11047b"

def retrieveDietEntries(info, username):
	startDate = info['startDate']
	endDate = info['endDate']
	
	message = "<p>No entries found</p>"
	total = ""

	if startDate.year > endDate.year or (startDate.year == endDate.year and startDate.month > endDate.month) or (startDate.year == endDate.year and startDate.month == endDate.month and startDate.day > endDate.day):
		return "<p class='message'>Error: the start date must be before the end date</p>"


	try:
		conn = psycopg2.connect(database=dbName, password = dbPassword, user=dbUser, host=dbHost)

		cursor = conn.cursor()
	
		cursor.execute("SELECT * FROM LogEntry INNER JOIN DietEntry ON LogEntry.logdate = DietEntry.logdate WHERE LogEntry.username = %s AND LogEntry.logdate BETWEEN %s AND %s ORDER BY LogEntry.logdate", (username, info['startDate'], info['endDate']))
		rows = cursor.fetchall()
		
		prevDate = rows[0][0]
		message = "<div class='Diet-Entry'><h3>Date: " + prevDate.strftime("%m/%d/%Y") + "</h3>"
		dayTotal = 0
		overallTotal = 0
		for row in rows:
			currentDate = row[0]
			if prevDate != currentDate:
				message += "<p class='Diet-Final-Tally'>Total calories: " + str(dayTotal)+ "</p></div><div class='Diet-Entry'><h3>Date: " + currentDate.strftime("%m/%d/%Y") + "</h3>"
				dayTotal = 0
				prevDate = currentDate
			message += "<div class='Diet-Sub-Entry'><p>Food: " + row[2]+ "</p>Calories: " + str(row[3]) + "<p></p></div>"
			dayTotal += row[3]
			overallTotal += dayTotal
		message += "<p class='Diet-Final-Tally'>Total Calories: " + str(dayTotal)+ "</p></div>"
		total = "<p class='message' style='font-size:1.2em; font-weight:bold;'> The total number of calories consumed in the given time period is " + str(overallTotal) + " calories</p>"

	except Exception as ex:
		print("Not connected: ", ex)
		print("Not connected: " + type(ex).__name__)
		message = "<p>No entries found</p>"



	return [message, total]

def createDietEntry(info, username):
	
	message = "<p>No entries found</p>"

	print("----------Start-------------")
	try:
		conn = psycopg2.connect(database=dbName, password = dbPassword, user=dbUser, host=dbHost)

		cursor = conn.cursor()
		
		print("----------we-------------")
		# check to see if an entry for the entered date already exists
		cursor.execute("SELECT * FROM LogEntry WHERE username = %s AND logdate = %s", (username, info['date']))
		#rows = cursor.fetchall()

		print("----------here-------------")
		if cursor.rowcount == 0:
			cursor.execute("INSERT INTO LogEntry(logdate, username) VALUES(%s, %s)", (info['date'], username))
		
		cursor.execute("INSERT INTO DietEntry(food, calories, logdate) VALUES(%s, %s, %s)", (info['food'], info['calories'], info['date']))

		conn.commit()
		message = "New entry successfully created"
	except Exception as ex:
		print("Not connected: ", ex)
		print("Not connected: " + type(ex).__name__)
		message = "<p>No entries found</p>"

	return message
