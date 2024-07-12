from django.urls import path
from LMS.views import *

urlpatterns = [
    path('', CourseView.as_view(), name = "main"),
    path('<int:pk>/', TaskView.as_view(), name = "task_list"),
    path('task_add/', TaskAddView.as_view(), name = "task_add"),
    path('<int:pk>/update/', TaskUpdateView.as_view(), name = "task_update"),
    path('<int:pk>/delete/', TaskDeleteView.as_view(), name = "task_delete"),
    path('<int:pk>/detail/', TaskDetailView.as_view(), name = "task_detail"),
    path('<int:pk>/lessons/', LessonView.as_view(), name = "lesson_list"),
    path('lesson_add/', LessonAddView.as_view(), name="lesson_add"),
    path('<int:pk>/lesson_update/', LessonUpdateView.as_view(), name="lesson_update"),
    path('<int:pk>/lesson/detail/', LessonDetailView.as_view(), name = "lesson_detail"),
    path('<int:pk>/lesson/delete/', LessonDeleteView.as_view(), name = "lesson_delete"),
    path('lessons/<int:lesson_pk>/task_done_add/', TaskDoneView.as_view(), name = "task_done"),
    
]

app_name = "lms"