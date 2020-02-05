# Course_Map

live demo: https://coursemap.herokuapp.com/

## Description

This web app gives you a tree of the prerequisite required to take a given course at UVIC

## Usage
#### Type a course into the search box at the top, an example could be "CSC 361"
Holding on a course will search for that course, single click on a course will highlight all instances of the course
![Demo Gif](CourseMapDemo.gif)

## Development

This website was created by scrapping the uvic course site with beautiful and creating a database of dependencies. There are three tables in the database, course, operations and precombinations. Courses may have many types of operations and operations may have many of different courses. For example, the course CSC 361 has two direct operations. Single course with SENG 265 and One of CSC 230, CENG 255 ECE 255. Each of these course have one or many operations, who have one or many precombination courses

This tree is stored in the database, and is retrieved by a breath first search. The website is writen in Django
