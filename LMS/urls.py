from django.urls import path
from LMS.views import *

urlpatterns = [
    path('', CourseView.as_view(), name = "main"),
    path('<int:pk>/', TaskView.as_view(), name = "task_list"),
    path('task_add/', TaskAddView.as_view(), name = "task_add"),
    path('<int:pk>/update/', TaskUpdateView.as_view(), name = "task_update"),
    path('<int:pk>/delete/', TaskDeleteView.as_view(), name = "task_delete"),
    path('<int:pk>/detail/', TaskDetailView.as_view(), name = "task_detail"),
    path('comment_add/', CommentAddView.as_view(), name="comment_add"),
    path('comment/<int:comment_id>/like-toggle/', CommentLikeToggle.as_view(), name='comment-like-toggle'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name = "comment_delete"),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', edit_profile_view, name='edit_profile'),
]

app_name = "lms"