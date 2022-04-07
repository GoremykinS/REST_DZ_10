from django.db import models


class Project(models.Model):
    project_users = models.CharField(max_length=64)
    project_name = models.CharField(max_length=64)
    git_name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.project_users}'

class Todo(models.Model):
    text = models.CharField(max_length=64)
    time = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(Project, on_delete = models.CASCADE)

class User(models.Model):
    age = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    user_name = models.ForeignKey(Project, on_delete = models.CASCADE)