from django.urls import path
from LMS.views import *

urlpatterns = [
    path('', CourseView.as_view(), name = "main"),
]

app_name = "lms"