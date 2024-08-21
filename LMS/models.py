from django.db import models


from django.contrib.auth.models import AbstractUser, User
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Permission


class CustomUser(AbstractUser):

    ROLE_CHOICES = (
        ('admin', 'Администратор'),
        ('teacher', 'Учитель'),
        ('student', 'Студент'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='customuser_set',
        related_query_name='user'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='customuser_set',
        related_query_name='user'
    )

    def save(self, *args, **kwargs):
        if not self.id:
            self.set_password(self.password) 

        super().save(*args, **kwargs)
        self.assign_role_permissions()  

    def assign_role_permissions(self):
        if self.role == 'student':
            permissions = Permission.objects.filter(codename__in=['view_info'])
        elif self.role == 'teacher':
            permissions = Permission.objects.filter(codename__in=['add_object', 'change_object'])
        elif self.role == 'admin':
            permissions = Permission.objects.all()
        else:
            permissions = Permission.objects.none()

        self.user_permissions.set(permissions)

    def __str__(self):
        return self.username


class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100,null=True, blank=True)
    image = models.FileField(upload_to="course_media", blank=True, null=True)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)


    def __str__(self):
        return f"{self.name}"


class Task(models.Model):
    name = models.CharField(max_length = 50)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_task')
    description = models.TextField()
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    create_date = models.DateField(auto_now_add=True, null=True, blank=True)
    dead_line = models.DateField()
    
    

    def __str__(self):
        return f"{self.name}"


class Announcement(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    #media
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"

class Course_User(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE,  related_name='course')
    users_courses = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_user') 

class Task_User(models.Model):
    task = models.OneToOneField(Task, on_delete=models.CASCADE, related_name='task')
    user_task = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='task_user')
    MARKS = [
        ("0", "Не оценено"),
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5")
    ]


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    creator = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    

    def get_absolute_url(self):
        return self.post.get_absolute_url()

class Like(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='liked_comments')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('comment', 'user')
