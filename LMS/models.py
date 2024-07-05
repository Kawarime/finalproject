from django.db import models


from django.contrib.auth.models import AbstractUser, User
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Permission



class CustomUser(AbstractUser):
    password = models.CharField(max_length=128)
    
    role = models.CharField(max_length=20, choices=(
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Administrator'),
    ), default='user')
  
    
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


    def clean(self):
        super().clean()
        if len(self.password) < 8:
            raise ValidationError("Your password must contain at least 8 characters.")
        if self.password.isdigit():
            raise ValidationError("Your password can’t be entirely numeric.")
        if self.password.isalpha():
            raise ValidationError("Your password must contain at least one digit.")
        if self.password.islower() or self.password.isupper():
            raise ValidationError("Your password must contain both uppercase and lowercase letters.")
        if not any(char.isdigit() for char in self.password):
            raise ValidationError("Your password must contain at least one digit.")
        if not any(char.isupper() for char in self.password) or not any(char.islower() for char in self.password):
            raise ValidationError("Your password must contain both uppercase and lowercase letters.")
        if not any(char.isalnum() for char in self.password):
            raise ValidationError("Your password must contain at least one special character.")
        if self.password.lower() in ['password', '123456', 'qwerty']:
            raise ValidationError("Your password is too common.")
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.set_password(self.password) 
        self.full_clean() 
        
        if (
            'username' in kwargs or 'first_name' in kwargs or 'last_name' in kwargs or
            'email' in kwargs or 'role' in kwargs
        ):
            self.full_clean()

        super().save(*args, **kwargs)
        self.assign_role_permissions()  


    def assign_role_permissions(self):
        if self.role == 'student':
            permissions = Permission.objects.filter(codename__in=['view_info'])
        elif self.role == 'teacher':
            permissions = Permission.objects.filter(codename__in=['add_object', 'change_object'])
        elif self.role == 'admin':
            permissions = Permission.objects.all()
        
        
        self.user_permissions.set(permissions)

    def __str__(self):
        return self.username
    


class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    short_description = models.CharField(max_length=100,null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


class Task(models.Model):
    STATUSES= [
        ("notdone", "Not Done"),
        ("done", "Done")
    ]
    name = models.CharField(max_length = 50)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_task')
    description = models.TextField()
    status = models.CharField(max_length = 50, choices = STATUSES, default = "notdone")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    priority = models.IntegerField()
    start_date = models.DateField()
    dead_line = models.DateField()
    
    

    def __str__(self):
        return f"{self.name}"

class Lesson(models.Model):
    name = models.CharField(max_length=100)
    content = models.TextField()
    #media
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_lesson')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"




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
    post = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    creator = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    media = models.FileField(upload_to='comments_media/',blank = True, null =True)

    def get_absolute_url(self):
        return self.post.get_absolute_url()

class Like(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes')
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='liked_comments')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: 
        unique_together = ('comment', 'creator')
