import re
import sqlite3
from sqlite3 import Error

courseList = []


def main():

	database = '/Users/nathanjenkins/Dropbox/Programming/Course_Map/Course_Map/course.sqlite3'

	conn = createConnection(database)

	deleteAll(conn)
	stringParser(conn)

	conn.commit()

	return


def deleteAll(conn):
	with conn:
		c = conn.cursor()
		c.execute("DELETE FROM UVICMap_course")
		c.execute("DELETE FROM UVICMap_operations")
		c.execute("DELETE FROM UVICMap_precombinationcourses")


def createConnection(db_file):
	try:
		conn = sqlite3.connect(db_file)
		return conn
	except Error as e:
		print(e)
		return None

def findCidRowId(conn, cid):
	with conn:
		sql = "SELECT id FROM UVICMap_course WHERE cid = ?"
		c = conn.cursor()
		c.execute(sql, cid)
		row = c.fetchone()
		if (row):
			return row[0]
		return -1


def createCourse(conn, cid):
	with conn:
		sql = "INSERT INTO UVICMap_course VALUES (NULL, ?)"
		c = conn.cursor()
		c.execute(sql, cid)
		return c.lastrowid


def createOperation(conn, operation):
	with conn:
		try:
			sql = "INSERT INTO UVICMap_operations VALUES (NULL, ?, ?)"
			c = conn.cursor()
			c.execute(sql, operation)
			return c.lastrowid
		except sqlite3.IntegrityError:
			return -1


def createPreCombinationCourses(conn, combination):
	with conn:
		sql = "INSERT INTO UVICMap_precombinationcourses VALUES (NULL, ?, ?)"
		c = conn.cursor()
		c.execute(sql, combination)
		return c.lastrowid


courseString = r"[A-Z\-]{2,4}\s[0-9]{3}[A-Z]?"
courseID = re.compile(courseString)

def processCourse(conn, course):

	cid = courseID.search(course).group(0)

	# add course to the course table
	courseTuple = (cid,)
	courseTupleID = findCidRowId(conn, courseTuple)
	if ( courseTupleID == -1):
		courseTupleID = createCourse(conn, courseTuple)
	return courseTupleID

def processPrereq(conn, line, courseTupleID):
	line = line[8:].rstrip('.\n')

	# if there are courses after prereq
	if not (re.search(r'(None)', line)):

		for s in re.split('; ', line):

			operation = parseSubsetOperation(s)
			if (operation == "ERR"):
				break

			# add operations to operation table
			opTuple = (operation, courseTupleID)
			operationTableID = createOperation(conn, opTuple)			
			
			addCombinationCourse(conn, operationTableID,  courseID.findall(s))
	return

def stringParser(conn):

	courseStringWith = r"[A-Z\-]{2,4}\s[0-9]{3}[A-Z]? with.*(?=[\,,;,.])"
	courseIDWith = re.compile(courseStringWith)

	# file = open('./CSCCourses.txt')
	file = open('./CSCCourses.txt')

	while True:

		course = file.readline()
		prereq = file.readline() 
		coreq = file.readline() 
		precoreq = file.readline()
		file.readline()

		if (course.strip() == "" or course == None):
			break

		courseTupleID = processCourse(conn, course)	
		processPrereq(conn, prereq, courseTupleID)
			
	file.close


def parseSubsetOperation(s):
	courseString = r"[A-Z\-]{2,4}\s[0-9]{3}[A-Z]?"
	courseID = re.compile(courseString)

	if (len(courseID.findall(s)) == 1):
		operation = 'Single'

	elif (re.search(r'[E,e]ither ', s)):
		operation = 'Either'

	elif (re.search(courseString + r'.*or ' + courseString, s)):
		operation = 'Or'

	elif (re.search(r', [O,o]r ', s)):
		operation = 'Or'

	elif (re.search(r'[O,o]ne of ', s)):
		operation = 'One of'

	elif (re.search(r'[T,t]wo of ', s)):
		operation = 'Two of'

	elif (re.search(r'[A,a]nd ', s)):
		operation = 'Single'

	else:
		operation = 'ERR'

	return operation


def addCombinationCourse(conn, operationID, courses):

	for cid in courses:
		# find the cid of the course
		courseTuple = (cid,)
		courseTupleID = findCidRowId(conn, courseTuple)

		# if one of the courses has not already been added to the course table
		if (courseTupleID == -1):
			courseTupleID = createCourse(conn, courseTuple)

		combination = (courseTupleID, operationID)
		createPreCombinationCourses(conn, combination)


if __name__ == "__main__":
	main()
