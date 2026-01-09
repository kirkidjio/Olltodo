from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Group(models.Model):
    leader = models.ForeignKey(User, on_delete=models.CASCADE, related_name="leader")
    members = models.ManyToManyField(User, related_name="members")
    name = models.CharField(max_length=250)
    

class TaskList(models.Model):
    name = models.CharField(max_length=250)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)


class Task(models.Model):
    performer = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length = 250)
    tasklist = models.ForeignKey(TaskList, on_delete=models.CASCADE)
    class Status(models.TextChoices):
        OPEN = 'open', 'Open'
        SUBMITTED = "submitted", 'Submitted'
        ACCEPTED = "accepted", 'Accepted'
        REJECTED = "rejected", 'Rejected'
    
    status = models.CharField(choices=Status.choices, default=Status.OPEN)
    
    class Priority(models.IntegerChoices):
        HIGH = 3, "High"
        MEDIUM = 2, "Medium"
        Low = 1, "Low"
        NONE = 0, ""
    
    priority = models.IntegerField(choices=Priority.choices, default=Priority.NONE)
    

class Note(models.Model):
    title = models.CharField()
    content = models.TextField(null=True)
    tasklist = models.ForeignKey(TaskList, on_delete=models.CASCADE)
    last_update = models.DateTimeField('last-update', auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
