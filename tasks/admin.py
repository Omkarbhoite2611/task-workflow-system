from django.contrib import admin
from .models import Project, Task


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'project',
        'status',
        'priority',
        'due_date',
        'is_deleted',
    )
    list_filter = ('status', 'priority', 'is_deleted')
    search_fields = ('title',)
