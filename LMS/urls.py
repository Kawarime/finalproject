from django.urls import path
from LMS.views import *

urlpatterns = [
    path('', CourseView.as_view(), name = "main"),
    path('<int:pk>/', TaskView.as_view(), name = "task_list"),
    path('task_add/', TaskAddView.as_view(), name="task_add"),
    path('<int:pk>/update/', TaskUpdateView.as_view(), name = "task_update"),
    path('<int:pk>/delete/', TaskDeleteView.as_view(), name = "task_delete"),
]

app_name = "lms"