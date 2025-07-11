from django.db import models
from django.db.models.signals import post_save, pre_save, m2m_changed, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail

# Create your models here.
class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


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
        Employee,
        related_name='tasks'
        )
    title=models.CharField(max_length=250)
    description=models.TextField()
    due_date=models.DateField()
    status = models.CharField(max_length=15,choices=STATUS_CHOICES,default=PENDING)
    is_completed=models.BooleanField(default=False)
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

#Implement Signals
#post_save
# @receiver(post_save, sender=Task)
# def notify_task_creation(sender,instance, created,**kwargs):
#     if created:
#         print("Sender" ,sender)
#         print("created", created)
#         print("Instance", instance)
#         print("Kwargs", kwargs)
#         instance.is_completed = True
#         instance.save()

#pre_save
# @receiver(pre_save, sender=Task)
# def notify_task_creation_pre(sender, instance, **kwargs):
#     print("Sender",sender)
#     print("Instance", instance)
#     print("Kwargs", kwargs)
#     instance.is_completed = True

# @receiver(post_save, sender=Task)

# def notify_employees_on_task_creation(sender, instance, created, **kwargs):
#     if created:
#         assigned_emails = [emp.email for emp in instance.assigned_to.all()]

#         send_mail(
#             "New Task Assigned",
#             f"You have been assigned for New Task:{instance.title}",
#             "tscrpbl@gmail.com",
#             assigned_emails,
#             # fail_silently=False,
#         )

@receiver(m2m_changed, sender=Task.assigned_to.through)

def notify_employees_on_task_creation(sender, instance, action, **kwargs):
    if action == 'post_add':
        print(instance, instance.assigned_to.all())
        assigned_emails = [emp.email for emp in instance.assigned_to.all()]
        
        print("Checking", assigned_emails)
        send_mail(  
            "New Task Assigned",
            f"You have been assigned for New Task:{instance.title}",
            "tscrpbl@gmail.com",
            assigned_emails,
            fail_silently=False
        )

# POST Delete Signals
@receiver(post_delete, sender=Task)
def delete_associate_details(sender, instance, **kwargs):
    if instance.details:
        print(isinstance)
        instance.details.delete()

        print("Deleted Successfully")