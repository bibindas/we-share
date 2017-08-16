from __future__ import unicode_literals
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db import models



class WSGroup(models.Model):
	group_name=models.CharField(max_length=30)
	group_members=models.ManyToManyField("Member")
	description=models.CharField(max_length=50)
	def __str__(self):
		return self.group_name

class Member(models.Model):
	user= models.ForeignKey(User,on_delete= models.CASCADE)
	phonenumber=models.CharField(max_length=50,blank=True,null=True)
	date=models.DateTimeField(blank=True,null=True)
	profilepic=models.ImageField(blank=True,null=True)
		
class Bill(models.Model):
	description=models.CharField(max_length=30)
	amount=models.CharField(max_length=30)
	date=models.DateTimeField()
	
class Transaction(models.Model):
	lender=models.ForeignKey(Member,blank=True,null=True,related_name="lender")
	receiver=models.ForeignKey(Member,blank=True,null=True,related_name="receiver")
	amount=models.IntegerField()
	description=models.CharField(max_length=50)
	date=models.DateTimeField()
	group=models.ForeignKey(WSGroup,blank=True,null=True)
	settled = models.BooleanField(default=False)
	
@receiver(post_save, sender=User)

def member_create(sender,instance,created,**kwargs):

	if created:
		Member.objects.create(user=instance) 