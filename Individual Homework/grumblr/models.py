from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.timezone import make_aware
import datetime

class UserProfile(models.Model):
	username   = models.CharField(max_length=20)
	first_name = models.CharField(max_length=20)
	last_name  = models.CharField(max_length=20)
	email      = models.EmailField(max_length=30)
	age        = models.IntegerField(blank=True,null=True)
	intro      = models.CharField(max_length=420,blank=True,null=True) 
	image      = models.ImageField(upload_to='images/profile',blank=True,null=True)   
	user       = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
	follow     = models.ManyToManyField(User,related_name='follow')

class UserPost(models.Model):
	username      = models.CharField(max_length=20)
	time          = models.DateTimeField(default=timezone.now)
	text          = models.CharField(max_length=100)
	profile       = models.ForeignKey(UserProfile,on_delete=models.CASCADE, null=True)
	user          = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
	last_modified = models.DateTimeField(auto_now=True)
	def __str__(self):
		return self.text
	
	@staticmethod
	def get_changes(timestamp=0):
		t = make_aware(datetime.datetime.fromtimestamp(timestamp/1000.0))
		return UserPost.objects.filter(last_modified__gt=t).distinct()
		
class PostComment(models.Model):
	time          = models.DateTimeField(default=timezone.now)
	comment       = models.CharField(max_length=100)
	user          = models.ForeignKey(UserProfile,on_delete=models.CASCADE, null=True)
	post          = models.ForeignKey(UserPost,on_delete=models.CASCADE, null=True)
	last_modified = models.DateTimeField(auto_now=True)
	def __str__(self):
		return self.comment
	
	@staticmethod
	def get_changes(timestamp=0):
		t = make_aware(datetime.datetime.fromtimestamp(timestamp/1000.0))
		return PostComment.objects.filter(last_modified__gt=t).distinct()
