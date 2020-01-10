import uuid
from django.db import models


class Course (models.Model):
	cid = models.CharField(max_length=10, default="", unique=True)

	def __str__(self):
		return "cid: {}".format(self.cid,)


class Operation (models.Model):
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	operation = models.CharField(max_length=10, default="")

	# def __str__(self):
	# 	return "course_id: {}, operation: {}".format(self.course, self.operation)


class PreCombinationCourse (models.Model):
	operation = models.ForeignKey(Operation, on_delete=models.CASCADE)
	course = models.ForeignKey(Course, on_delete=models.CASCADE)

	# def __str__(self):
	# 	return "operation_id: {}, course_id: {}".format(self.operation, self.course)
