from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import now


class Project(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    STATUS_PENDING = 'P'
    STATUS_IN_PROGRESS = 'IP'
    STATUS_COMPLETED = 'C'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_IN_PROGRESS, 'In Progress'),
        (STATUS_COMPLETED, 'Completed'),
    ]

    PRIORITY_LOW = 'L'
    PRIORITY_MEDIUM = 'M'
    PRIORITY_HIGH = 'H'

    PRIORITY_CHOICES = [
        (PRIORITY_LOW, 'Low'),
        (PRIORITY_MEDIUM, 'Medium'),
        (PRIORITY_HIGH, 'High'),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    title = models.CharField(max_length=150)
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING
    )
    priority = models.CharField(
        max_length=1,
        choices=PRIORITY_CHOICES,
        default=PRIORITY_MEDIUM
    )
    due_date = models.DateField()
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if (
            self.status == self.STATUS_COMPLETED
            and self.pk is not None
            and Task.objects.get(pk=self.pk).status == self.STATUS_PENDING
        ):
            raise ValidationError(
                "Task must be In Progress before it can be completed."
            )

    def is_overdue(self):
        return (
            self.due_date < now().date()
            and self.status != self.STATUS_COMPLETED
        )

    def __str__(self):
        return self.title
