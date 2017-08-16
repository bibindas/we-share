from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save, sender=User)

def member_create(sender,instance,created,**kwargs):

	if created:
		Member.objects.create(user=instance) 