from django import forms
from LMS.models import *

class TaskAdd(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "description", "status"]

    widgets = {
            'course': forms.HiddenInput()
        }
    
class LessonAdd(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ["name", "content"]

    widgets = {
            'course': forms.HiddenInput()
        }

#class CommentForm(forms.ModelForm):
#    class Meta:
#        model = Comment
#        fields = ["content",]
        #widgets = {
        #    "media": forms.FileInput()
#
        #}