# django
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse

# custom
from .rebuild import delete_all, process_course, process_prereq
from .webScraper import create_dict
from .forms import CourseForm	
from .query import find_req

# python
import json
import os


# Create your views here.
def index(request):

	return render(request, 'uvic/index.html', {'form' : CourseForm})

def get_prereq(request):
	cid = request.GET.get('cid', '')
	d = find_req(cid)
	return JsonResponse(d)

@staff_member_required
def hood(request):
	return render(request, 'uvic/hood.html')

@staff_member_required
def rebuild(request):
	debug = False

	# delete all values in the models
	delete_all()

	# get the course_dict from the text file so that it is faster than reloading each time
	if (debug):
		current_directory = os.path.dirname(os.path.abspath(__file__))
		filename = os.path.join(current_directory, 'courses.txt')
		with open(filename) as json_file:
			course_dict = json.load(json_file)
	# create the course dict live from scrapping the website
	else: 
		course_dict = create_dict()

	# rebuild
	for course, value in course_dict.items():
		prereq = value['prereq']
		course, created = process_course(course)
		
		if (not created):
			messages.error(request, 'Course not created')

		process_prereq(course, prereq)

   

	return render(request, 'uvic/hood.html')
