from django import forms
from LMS.models import *

class TaskAdd(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "description", "staus", "priority", "start_date", "dead_line"]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content",]
        #widgets = {
        #    "media": forms.FileInput()
#
        #}