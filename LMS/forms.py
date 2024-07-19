from django import forms
from LMS.models import *

class TaskAdd(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "description", "status", "start_date", "dead_line"]

    widgets = {
            'course': forms.HiddenInput()
        }
    


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content",]
        widgets = {
           "course": forms.FileInput()

        }
