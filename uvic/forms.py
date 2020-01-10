from django import forms
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit


class CourseForm(forms.Form):
    cid = forms.CharField(label='course', max_length=10)
