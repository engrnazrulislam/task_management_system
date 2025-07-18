from django.db import models
from django.contrib.auth.models import User


# Create your models here.
# class Employee(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)

#     def __str__(self):
#         return self.name


class Task(models.Model):
    PENDING='P'
    IN_PROGRESS='IP'
    COMPLETED='C'    
    STATUS_CHOICES = [
        (PENDING,'Pending'),
        (IN_PROGRESS,'In Progress'),
        (COMPLETED,'Completed')
    ]
    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,
        default=1,
        related_name="tasks"
        )
    assigned_to = models.ManyToManyField(
        # Employee,
        User,
        related_name='tasks'
        )
    title=models.CharField(max_length=250)
    description=models.TextField()
    due_date=models.DateField()
    status = models.CharField(max_length=15,choices=STATUS_CHOICES,default=PENDING)
    # is_completed=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    # taskDetails
    #Dunder method to return data
    def __str__(self):
        return f"Title: {self.title}, Status: {self.status}"

# one to one
class TaskDetail(models.Model):
    HIGH='H'
    MEDIUM='M'
    LOW='L'
    PRIORITY_OPTIONS=(
        (HIGH,'High'),
        (MEDIUM,'Medium'),
        (LOW,'Low')
    )
    # for work with images
    asset = models.ImageField(upload_to='tasks_asset', blank=True, null=True, default='tasks_asset/default_img.png')
    # assigned_to=models.CharField(max_length=250)
    priority=models.CharField(max_length=1,choices=PRIORITY_OPTIONS,default=LOW)
    # std_id = models.CharField(max_length=200, primary_key=True) # define customized primary key
    task=models.OneToOneField(
        Task,
        on_delete=models.CASCADE,
        related_name='taskDetails'
        )
    notes = models.TextField(blank=True, null=True)

    # Dunder method to return details of task title
    def __str__(self):
        return f"Details of {self.task.title}"
# many to many
class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()

# Dunder Method
    def __str__(self):
        return self.name
# many to one
# task = one task is perform by many people
# employee = one employee perform too many task.

#