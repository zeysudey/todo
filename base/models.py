from django.db import models
from datetime import date
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Task(models.Model): # Task model
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("User")
    )
    title = models.CharField(max_length=200, verbose_name=_("Title")) # Task title
    description = models.TextField(null=True, blank=True, verbose_name=_("Description")) # Task description
    complete = models.BooleanField(default=False, verbose_name=_("Complete")) # Task completion status
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Created")) # Task creation date
    deadline = models.DateTimeField(null=True, blank=True, verbose_name=_("Deadline")) # Task deadline
    branch = models.CharField(max_length=200, null=True, blank=True, verbose_name=_("Branch")) # Task branch

    def __str__(self): # String representation of the Task model
        return self.title
    
    class Meta: # Meta options for the Task model
        order_with_respect_to = 'user'