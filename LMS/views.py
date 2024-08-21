from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from LMS.models import *
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, View
from LMS.forms import CommentForm, TaskAdd
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from LMS.mixins import UserIsOwnerMixin
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth import login as auth_login

from django.urls import reverse_lazy
from django.views.generic.base import RedirectView

from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.contrib.auth.models import User
from LMS.models import CustomUser
from django.db import IntegrityError

from django.urls import path, reverse_lazy
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import authenticate, login
from .models import CustomUser

def base_view(request):
    return render(request, 'base.html')



# views.py
from django.shortcuts import render, redirect
from .forms import RegisterForm

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lms:main')  
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(reverse_lazy("lms:main"))
            else:
                error_message = "Ваш аккаунт не активований."
        else:
            error_message = "Неправильне ім'я користувача або пароль. Будь ласка, спробуйте ще раз."
    return render(request, 'login.html', {'error_message': error_message})


def logout_view(request):
    logout(request)
    return redirect(reverse_lazy("lms:main"))


@login_required
def profile_view(request):
    return render(request, 'profile.html')

@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        
        user = request.user
        user.username = username
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.save()
    
        return redirect('lms:profile')

    return render(request, 'edit_profile.html')


class CourseView(ListView):
    model = Course
    context_object_name = "courses"
    template_name = "LMS/main.html"
    paginate_by = 7
    
class TaskView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "LMS/tasks_list.html"
    context_object_name = "task"
    paginate_by = 6
    
    def get_queryset(self):
        course_pk = self.kwargs.get('pk')
        course = get_object_or_404(Course, pk=course_pk)
        tasks = Task.objects.filter(course=course)
        return tasks

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = get_object_or_404(Course, pk=self.kwargs.get('pk'))
        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "LMS/task_detail.html"
    context_object_name = "task"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()  
        return context
    
    

    def post(self, request, *args, **kwargs):
        task = self.get_object()  
        comment_form = CommentForm(request.POST, request.FILES)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.creator = request.user
            comment.task = task  
            comment.post = task  
            comment.save()
            return redirect('lms:task_detail', pk=comment.task.pk)
        
class TaskAddView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = "LMS/task_add.html"
    form_class = TaskAdd
    success_url = reverse_lazy("lms:main")

    def form_valid(self, form):
        course_pk = self.request.GET.get('course')
        course = get_object_or_404(Course, pk=course_pk)
        form.instance.course = course
        form.instance.creator = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('lms:main')
        

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = "LMS/task_update.html"
    form_class = TaskAdd
    success_url = reverse_lazy("lms:main")

class TaskDeleteView(LoginRequiredMixin,  DeleteView):
    model = Task
    template_name = "LMS/task_delete.html"
    success_url = reverse_lazy("lms:main")


class CommentAddView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = "LMS/comment_add.html"
    form_class = CommentForm
    success_url = reverse_lazy("lms:course_list")


class CommentLikeToggle(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        comment_id = kwargs.get('comment_id')
        comment = Comment.objects.get(pk=comment_id)
        user = request.user
        like, created = Like.objects.get_or_create(comment=comment, user=user)
        if not created:
           
            like.delete()

       
        return redirect('lms:task_detail', pk=comment.task.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ["comments"] = Comment.objects.filter(task=self.get_object())
        return context


    


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = "LMS/comment_delete.html"
    success_url = reverse_lazy("lms:main")

    def get_object(self, queryset=None):
        object = super().get_object(queryset)
        print(object)
        return object

    def get_success_url(self):
        if self.object:
            return self.success_url
        else:
            return reverse_lazy("lms:main")



