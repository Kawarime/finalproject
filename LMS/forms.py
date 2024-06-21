from django import forms
from LMS.models import *

class TaskAdd(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "course", "description", "status", "priority", "start_date", "dead_line"]

class LessonAdd(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ["name", "content", "creator", "course"]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content",]
        #widgets = {
        #    "media": forms.FileInput()
#
        #}