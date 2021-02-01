from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Blog

from .models import *
  
class BlogForm(forms.ModelForm): 
	class Meta:
		model = Blog
		fields = ['title', 'blog_detail','firstname', 'lastname', 'userid', 'blog_pic']

class CreateUserForm(UserCreationForm):
	"""docstring for CreateUserForm"""
	class Meta:
		model = User
		fields = ['username','first_name', 'last_name',  'email', 'password1', 'password2']

class FollowForm(forms.ModelForm):
	"""docstring for FollowForm"""
	class Meta:
		model = Follow
		fields = ['userid', 'follow_id','firstname', 'lastname']
