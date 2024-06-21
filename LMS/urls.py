from django.urls import path
from LMS.views import *

urlpatterns = [
    path('', CourseView.as_view(), name = "main"),
    path('<int:pk>/', TaskListView.as_view(), name = "task_list"),
]

app_name = "lms"