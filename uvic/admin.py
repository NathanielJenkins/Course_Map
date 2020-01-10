from django.contrib import admin
from .models import Course, Operation, PreCombinationCourse

admin.site.register(Course)
admin.site.register(Operation)
admin.site.register(PreCombinationCourse)