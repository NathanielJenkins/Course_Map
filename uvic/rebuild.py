# custom
from .models import Course, Operation, PreCombinationCourse

# python
import re

def delete_all():
	Course.objects.all().delete()
	Operation.objects.all().delete()
	PreCombinationCourse.objects.all().delete()

courseString = r"[A-Z\-]{2,4}\s[0-9]{3}[A-Z]?"
courseID = re.compile(courseString)

def process_course(course):
	# get the cid by regex
	cid = courseID.search(course).group(0)

	# add the course to the course table
	course, created = Course.objects.get_or_create(cid=cid)
	return course, created

def process_prereq(course, prereq):

	if prereq is None: 		
		return

	error_messages = [] 
	for s in re.split('; ', prereq):

			operation = parse_operation(s)
			
			if (operation == "ERR"):
				error_messages.append("operation ERR")
				return
			
			# add operations to operation table
			operation_obj = Operation(course=course, operation=operation)
			operation_obj.save()

			combination_error_messages = add_combination_course(operation_obj, courseID.findall(s))	
			error_messages.append(combination_error_messages)
	
	return error_messages


def parse_operation(s):

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

def add_combination_course(operation_obj, courses):
	error_messages = []
	for cid in courses: 
		
		# find the cid of the course
		course, created = Course.objects.get_or_create(cid=cid)

		# temps 
		if not created : 
			error_messages.append("combination error message")

		combination = PreCombinationCourse(operation=operation_obj, course=course,)
		combination.save()
	
	return error_messages