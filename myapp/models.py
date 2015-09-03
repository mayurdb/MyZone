from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage


class Child(models.Model):
	u_profile = models.ForeignKey('User_profile')
	name = models.CharField(max_length=100)
	dob = models.DateField()
	gender = models.CharField(max_length=10)
	grade =  models.CharField(max_length=50,default=0)
	image = models.ImageField(upload_to='images/',default=None,editable=True,null=True,blank=True)
	def __str__(self):
		return self.name	
		
class User_profile(models.Model):
	user = models.OneToOneField(User)
	confirmation_key = models.IntegerField(default=0)
	def __str__(self):
		return self.user.username

class Friendship(models.Model):
	to_friend = models.ForeignKey('User_profile',related_name='to_friend_set')
	from_friend = models.ForeignKey('User_profile', related_name='from_friend_set')

	class Meta:
		unique_together = (('to_friend', 'from_friend'), )  

	def __str__(self):
		# return str(self.from_friend_req) + " sends req to " + str(self.to_friend_req)
		return str(self.from_friend) + " and " + str(self.to_friend)  	

class Friend_request(models.Model):
	to_friend_req = models.ForeignKey('User_profile',related_name='to_friend_req_set')
	from_friend_req = models.ForeignKey('User_profile',related_name='from_friend_req_set')

	class Meta:
		unique_together = (('to_friend_req', 'from_friend_req'), )  
 
	def __str__(self):
		return str(self.from_friend_req) 
