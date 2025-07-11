from django.db.models.signals import post_save, pre_save, m2m_changed, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from tasks.models import Task

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