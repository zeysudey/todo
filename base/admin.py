from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'branch', 'created', 'deadline', 'complete'] #  displayed columns in the admin list view
    list_filter = ['user', 'branch','complete', 'created', 'deadline'] #  filter options in the admin list view
    search_fields = ['title', 'user__username'] #  search fields in the admin list view
    ordering = ['created'] #  default ordering in the admin list view
    list_editable = ['complete'] #  fields that can be edited directly in the list view
    date_hierarchy = 'created' #  date hierarchy for filtering by date

admin.site.register(Task, TaskAdmin)

