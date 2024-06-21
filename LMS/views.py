from django.shortcuts import render, redirect, get_object_or_404
from LMS.models import *
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, View
from LMS.forms import TaskAdd, CommentForm, LessonAdd
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

def base_view(request):
    return render(request, 'base.html')

# Register --- Login --- Logout #

def register_view(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        if password1 == password2:
            try:
                user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
                login(request, user)  # Вхід користувача в систему після реєстрації
                return redirect('main_page')
            except IntegrityError:
                error_message = "Ім'я користувача вже існує. Будь ласка, виберіть інше ім'я користувача."
                return render(request, 'register.html', {'error_message': error_message})
        else:
            error_message = "Паролі не співпадають."
            return render(request, 'register.html', {'error_message': error_message})
    return render(request, 'register.html')

def login_view(request):
    error_message = None
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('main_page')
        else:
            error_message = "Неправильне ім'я користувача або пароль. Будь ласка, спробуйте ще раз."
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form, 'error_message': error_message})

def logout_view(request):
    logout(request)
    return redirect(reverse_lazy('main_page'))


# --- Profile --- #
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
        
        return redirect('profile')
    
    return render(request, 'edit_profile.html')
#конец регистрации

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
        tasks = Course.objects.filter(course=course)
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
        comment_form = CommentForm(request.POST, request.FILES)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.creator = request.user
            comment.task = self.get_object()
            comment.save()
            return redirect('LMS:task_detail', pk=comment.task.pk)
        
class TaskAddView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = "LMS/task_add.html"
    form_class = TaskAdd
    success_url = reverse_lazy("LMS:courses_list")

    def get_initial(self):
        initial = super().get_initial()
        course_pk = self.request.GET.get('course')
        initial['course'] = get_object_or_404(Course, pk=course_pk)
        return initial

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('LMS:course_list', kwargs={'pk': self.object.course.pk})
        

class TaskUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = Task
    template_name = "LMS/task_update.html"
    form_class = TaskAdd
    success_url = reverse_lazy("LMS:course_list")

class TaskDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = Task
    template_name = "LMS/task_delete.html"
    success_url = reverse_lazy("LMS:course_list")

class LessonView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "LMS/lesson_list.html"
    context_object_name = "lesson"
    paginate_by = 6
    
    def get_queryset(self):
        course_pk = self.kwargs.get('pk')
        course = get_object_or_404(Course, pk=course_pk)
        lessons = Course.objects.filter(course=course)
        return lessons

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = get_object_or_404(Course, pk=self.kwargs.get('pk'))
        return context

class LessonDetailView(LoginRequiredMixin, DetailView):
    model = Lesson
    template_name = "LMS/lesson_detail.html"
    context_object_name = "lesson"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()  
        return context

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST, request.FILES)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.creator = request.user
            comment.lesson = self.get_object()
            comment.save()
            return redirect('LMS:lesson_detail', pk=comment.lesson.pk)

class LessonAddView(LoginRequiredMixin, CreateView):
    model = Lesson
    template_name = "LMS/lesson_add.html"
    form_class = LessonAdd
    success_url = reverse_lazy("LMS:course_list")

    def get_initial(self):
        initial = super().get_initial()
        course_pk = self.request.GET.get('course')
        initial['course'] = get_object_or_404(Course, pk=course_pk)
        return initial

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('LMS:course_list', kwargs={'pk': self.object.course.pk})

class LessonUpdateView(LoginRequiredMixin, UpdateView):
    model = Lesson
    template_name = "LMS/lesson_update.html"
    form_class = TaskAdd
    success_url = reverse_lazy("LMS:course_list")

class LessonDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = Lesson
    template_name = "LMS/lesson_delete.html"
    success_url = reverse_lazy("LMS:course_list")

class CommentAddView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = "LMS/comment_add.html"
    form_class = CommentForm
    success_url = reverse_lazy("LMS:course_list")

#class CommentLikeToggle(LoginRequiredMixin, View):
#    def post(self, request, *args, **kwargs):
#        comment_id = kwargs.get('comment_id')
#        comment = Comment.objects.get(pk=comment_id)
#        user = request.user
#        like, created = Like.objects.get_or_create(comment=comment, user=user)
#        if not created:
#           
#            like.delete()
#
#       
#        return redirect('LMS:_detail', pk=comment.post.id)
#
#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        context ["comments"] = Comment.objects.filter(post=self.get_object())
#        return context

class CommentDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = Comment
    template_name = "LMS/comment_delete.html"
    success_url = reverse_lazy("LMS:course_list")

    def get_object(self, queryset = None):
        object = super().get_object(queryset)
        print(object)

class CommentAddView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = "/comment_add.html"
    form_class = CommentForm
    success_url = reverse_lazy("LMS:course_list")

