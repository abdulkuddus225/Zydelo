from django.shortcuts import render, redirect
from django.contrib .auth.forms import UserCreationForm
from .forms import CreateUserForm, BlogForm, FollowForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Blog, Follow
from datetime import datetime
from django.contrib.auth import get_user_model
from django.db import connection
from django.shortcuts import get_object_or_404
# Create your views here.
def userlogin(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username=username, password=password)
		context = {'user': user}
		if user is not None:
			login(request, user)
			messages.info(request, context)
			return redirect('bloghome')

		else:
			messages.info(request, 'Username or password is incorrect!!')
	return render(request,'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

def register(request):
	
	form = CreateUserForm()

	if request.method == 'POST':
		form  = CreateUserForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request,"Account Created!!")
			return redirect('login')
	context = {'form' : form, 'messages': messages}
	return render(request, 'register.html', context)

def bloghome(request):
	form = BlogForm()
	print(form)
	get_blog = Blog.objects.all()
	followers = Follow.objects.all()
	cur_user = request.user.id
	query = "SELECT * FROM blog_blog b, blog_follow f where b.userid = f.follow_id and b.userid = %s;"
	follow_blogs = Blog.objects.raw(query, [cur_user])
	
	if request.method == 'POST':
		form = BlogForm(request.POST, request.FILES)
		print(form)
		if form.is_valid():
			form.save()
			return redirect('myblog')
		#if request.POST.get('title') and request.POST.get('firstname') and request.POST.get('lastname') and request.POST.get('blog_detail'):
			#post = Blog()
			#post.title = request.POST.get('title')
			#post.firstname = request.POST.get('firstname')
			#post.lastname = request.POST.get('lastname')
			#post.blog_detail = request.POST.get('blog_detail')
			#post.release_date = myDate.strftime("%Y-%m-%d")
			#post.blog_Main_Img = request.POST.get('blog_Main_Img')
			#post.save()
		else:
			print("Error")
	context = {'form':form, 'follow_blogs':follow_blogs}
	return render(request, 'bloghome.html', context)


def myblog(request):
	current_user = request.user
	data = Blog.objects.filter(userid=current_user.id)
	context = {'data':data}
	return render(request,'myblogs.html', context)


def delete_blog(request,id):
	obj = get_object_or_404(Blog, pk=id)
	if request.method=='POST':
		obj.delete()
		return redirect('../')
	context = {"obj":obj}
	return render(request, 'delete.html', context)


def suggestions(request):
	
	User = get_user_model()
	users = User.objects.all()
	current_user = request.user.id
	form = FollowForm()
	context = {'users':users, 'current_user':current_user,'form':form}

	if request.method=='POST':
		form = FollowForm(request.POST)
		if form.is_valid():
			form.save()
		return redirect('suggestions')

	return render(request,'suggestions.html', context)

	
def edit_blog(request,id):
	blog_edit = Blog.objects.get(id=id)
	form = BlogForm()
	if request.method=='POST':
		form = BlogForm(request.POST, instance=blog_edit)
		if form.is_valid():
			form.save()
		return redirect('../')
	context = {"blog_edit": blog_edit, "form":form}
	return render(request, 'edit_blog.html', context)







