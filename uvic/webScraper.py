#a trash, super inefficient webparser built with beautiful soup


import requests
import urllib.parse
import json

from bs4 import BeautifulSoup

# custom
from .rebuild import delete_all, process_course, process_prereq

debug = 1

def create_dict(ret = True, live = False):
	# --------------------- #
	courseObectList = []
	# ----------------------#

	url = urllib.parse.urlparse('https://web.uvic.ca/calendar2018-09/courses/')

	page = requests.get (url.geturl())
	soup = BeautifulSoup(page.content, 'html.parser')

	courseDict = {}

	# Loops through all the faculuties on the uvic page 
	visitedFacList = [] 
	#comment back in when you want all the courses in all fac
	# for link in soup.find('section', class_='CoIn').find_all('a'): 
	if 1==1: 
		link = soup.find('a', text ="Computer Science")
		#print (link)
		l = urllib.parse.urljoin(url.geturl(), link.get('href'))
		
		if (link.get('href') and link.get('href')[:6] == '../CDs' and l not in visitedFacList):
			visitedFacList.append(l)

			page2 = requests.get(l)
			soup2 = BeautifulSoup(page2.content, 'html.parser')

			visitedCourseList = []

			#Loops through all the courses in the faculty page
			#for crs in soup2.find_all('section', class_='crs-list'):		#comment back in if you want to consider graduate courses aswell
			crs = soup2.find('section', class_='crs-list')				
			if crs is not None:
				for link2 in crs.find_all('a'):

					l2 = urllib.parse.urljoin (l, link2.get('href'))

					#l2 contains the full url for each of the individual courses at uvic
					if (link2.get('href') and link2.get('href')[:2].isdigit()) and l2 not in visitedCourseList:
						visitedCourseList.append(l2)

						page3 = requests.get(l2)
						soup3 = BeautifulSoup(page3.content, 'html.parser')

						cid=soup3.title.get_text().rstrip()
						prereq = soup3.find('ul', class_='prereq')
						coreq = soup3.find('ul', class_='coreq')
						precoreq = soup3.find('ul', class_='precoreq')
						
						if prereq: 
							prereq = prereq.get_text().replace("\n", " ")
						
						if coreq:
							coreq = coreq.get_text().replace("\n", " ")				

						if precoreq: 
							precoreq = precoreq.get_text().replace("\n", " ")	

						courseDict[cid] = {
							"prereq" : prereq,
							"coreq" : coreq,
							"precoreq" : precoreq
						}
						print (cid,courseDict[cid])

						if (live):
							course, created = process_course(cid)
						
							if (not created):
								messages.error(request, 'Course not created')

							process_prereq(course, prereq)

	
	if (ret):
		return courseDict
	else:
		print ('creating new courses.txt')
		with open('courses.txt', 'w') as outfile:
			json.dump(courseDict, outfile)

if __name__ == "__main__":
	create_dict()