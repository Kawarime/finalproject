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

class TaskDoneForm(forms.ModelForm):
    class Meta:
        model = Task_Done
        fields = ["content"]
    
    widgets = {
            'task': forms.HiddenInput(),
            'media': forms.FileInput(),
        }

#class CommentForm(forms.ModelForm):
#    class Meta:
#        model = Comment
#        fields = ["content",]
        #widgets = {
        #    "media": forms.FileInput()
#
        #}