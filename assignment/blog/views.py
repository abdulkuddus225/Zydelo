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
from django.contrib.auth.decorators import login_required
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

@login_required
def bloghome(request):
	form = BlogForm()
	get_blog = Blog.objects.all()
	cur_user = request.user.id
	followers = Follow.objects.filter(userid_id = cur_user)
	follow_id = []
	for i in followers:
		follow_id.append(i.follow_id)
	if request.method == 'POST':
		form = BlogForm(request.POST, request.FILES)
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
	context = {'form':form,'follow_id':follow_id,'get_blog':get_blog}
	return render(request, 'bloghome.html', context)

@login_required
def myblog(request):
	current_user = request.user
	data = Blog.objects.filter(userid=current_user.id)
	context = {'data':data}
	return render(request,'myblogs.html', context)

@login_required
def delete_blog(request,id):
	obj = get_object_or_404(Blog, pk=id)
	if request.method=='POST':
		obj.delete()
		return redirect('../')
	context = {"obj":obj}
	return render(request, 'delete.html', context)

@login_required
def suggestions(request):
	
	User = get_user_model()
	users = User.objects.all()
	current_user = request.user.id
	form = FollowForm()
	followers = Follow.objects.filter(userid_id = current_user)
	who_follows_me = Follow.objects.filter(follow_id = current_user)
	who_follows_me_get = []
	follow_id_get = []
	for j in who_follows_me:
		who_follows_me_get.append(j.userid_id)
	for i in followers:
		follow_id_get.append(i.follow_id)

	if request.method=='POST':
		# form = FollowForm(request.POST)
		# if form.is_valid():
		# 	form.objects.get_or_create()
		userid_f = request.POST.get('userid')
		follow_f = request.POST.get('follow_id')
		firstname = request.POST.get('firstname')
		lastname = request.POST.get("lastname")

		try:
			obj = Follow.objects.get(userid_id = userid_f, follow_id=follow_f)
		except Follow.DoesNotExist:
			obj = Follow(userid_id=userid_f, follow_id=follow_f,firstname=firstname,lastname=lastname)
			obj.save()
		return redirect('suggestions')
	context = {'users':users, 'current_user':current_user,'form':form,'follow_id_get':follow_id_get,'who_follows_me_get':who_follows_me_get}
	return render(request,'suggestions.html', context)

@login_required
def edit_blog(request,id):
	blog_edit = Blog.objects.get(id=id)
	form = BlogForm()
	if request.method=='POST':
		form = BlogForm(data=request.POST, files=request.FILES, instance=blog_edit)
		print(form)
		if form.is_valid():
			form.save()
		return redirect('../')
	context = {"blog_edit": blog_edit, "form":form}
	return render(request, 'edit_blog.html', context)







