from django import forms
from LMS.models import *
from .models import CustomUser


class TaskAdd(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "description", "dead_line"]

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


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirmation = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, widget=forms.Select)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'role')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')

        if password and password_confirmation and password != password_confirmation:
            raise forms.ValidationError('Пароли не совпадают')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user