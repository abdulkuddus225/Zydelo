from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Blog(models.Model):

	userid = models.IntegerField(null=False, blank=False)
	title = models.CharField(max_length=200)
	blog_detail = models.TextField(max_length=500)
	firstname = models.CharField(max_length=100, null=False, blank=False, default="Error")
	lastname = models.CharField(max_length=100, null=False, blank=False, default="Error")
	blog_pic = models.ImageField(upload_to = 'media', null=True, blank=True)
	def __str__(self):
		return self.title

class Follow(models.Model):
	userid = models.ForeignKey(User,on_delete=models.CASCADE)
	follow_id = models.IntegerField(null=False, blank=False)

