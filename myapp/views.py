from django.db.models import Q
from django.shortcuts import render, render_to_response,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.core.mail import send_mail
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.decorators import login_required
import random
from django.views.decorators.cache import cache_control
from django.views.generic.edit import UpdateView
from django.http import Http404

@cache_control(no_cache=True, must_revalidate=True)
def index(request):
	if request.method == 'POST':
		data=request.POST
		form1 = SignUpForm(request.POST)
		form2 = SignInForm()
		if form1.is_valid():
			i = random.randint(1000,9999)
			user = User.objects.create_user(data['username'], data['email'], data['password'])
			user.last_name = data['last_name']
			user.first_name = data['first_name']
			user.is_active=False
			user.save()
			user_profile=User_profile.objects.create(user=user)
			user_profile.confirmation_key=i
			user_profile.save()
			content = "Confirmation Key for Smartfeed Account Registeration: " + str(i)
			request.session['user_id'] = user.id
			send_mail('Account-Confirmation',content,'persontest42@gmail.com',[data['email']], fail_silently=False)
			return render(request,"myapp/key.html")
			# user_list.append(user)
		else:
			return render(request, "myapp/index.html", {'form1': form1,'form2':form2})
		
			
	else:
		form1 = SignUpForm()
		form2 = SignInForm()
		return render(request, "myapp/index.html", {'form1': form1,'form2':form2})


def sign_up(request):
	# return HttpResponse(request.POST['confirmation_key'])
	user_id = request.session.get('user_id')
	if user_id is None:
		user = request.user
	else :	
		user = User.objects.get(id=user_id)
	user_profile = user.user_profile

	if request.method=='POST':
		try:	
			if int(request.POST['confirmation_key']) == user_profile.confirmation_key :
				user.is_active=True
				user.save()
				user_profile.save()
				# user = authenticate(username=user.username, password=user.password)
				# login(request, user)
				cform = Child_Profile_Form()
				return render(request, 'myapp/child_setup.html',{ "cform":cform })  
			else :
				message='Invalid Key'	
				return render(request,"myapp/key.html",{'message':message})
		except ValueError:
			message='The field cannot be left blank.'	
			return render(request,"myapp/key.html",{'message':message})
	
	else :

		cform = Child_Profile_Form()
		return render(request,'myapp/child_setup.html',{"cform":cform}) 



@cache_control(no_cache=True, must_revalidate=True)
def sign_in(request):
	if request.method == 'POST':	
		data = request.POST
		user = authenticate(username=data['username'], password=data['password'])
		if user is not None:
			if user.is_active==True:
				login(request, user)
				# search_form = Search_Form()
				user = request.user
				user_profile = user.user_profile
				return render(request, 'myapp/home.html', {'user_profile' : user_profile})  
			else :
				request.session['user_id'] = user.id
				return render(request,"myapp/key.html")
		else:
			form1 = SignUpForm()
			form2 = SignInForm()
			return render(request,'myapp/index.html',{'error':"Please enter valid login details",'form1':form1,'form2':form2})



@login_required
def search(request):
	if request.method == 'POST' :
		your_search_query=request.POST['Parents']
		request.session['your_search_query'] = your_search_query
	else :
		your_search_query = request.session.get('your_search_query')
	user_id = request.session.get('user_id')
	if user_id is not None:
		loggedin_user = User.objects.get(id=user_id)
	else :	
		loggedin_user = request.user
	results = User.objects.filter(Q(first_name__icontains=your_search_query) | Q(last_name__icontains=your_search_query))
	results = [x for x in results if x != loggedin_user]
	result1 = []
	result2 = []
	result3 = []
	result4 = []
	for user in results:
		key = 0
		for f in loggedin_user.user_profile.to_friend_set.all():
			if (f.from_friend == user.user_profile):
				key = 1
				result1.append(user)
				break			
			else :
				key = 0					
		for f in loggedin_user.user_profile.from_friend_set.all():
			if (f.to_friend == user.user_profile):
				key = 1			
				result1.append(user)
				break
			else :
				key = 0		
		if key == 0: 		
			result2.append(user)
	for user in result2:
		key = 0
		for f in loggedin_user.user_profile.to_friend_req_set.all():
			if (f.from_friend_req == user.user_profile):
				key = 1
				result3.append(user)
				break			
			else :
				key = 0					
		for f in loggedin_user.user_profile.from_friend_req_set.all():
			if (f.to_friend_req == user.user_profile):
				key = 1			
				result3.append(user)
				break
			else :
				key = 0		
		if key == 0: 		
			result4.append(user)
			
	return render(request,'myapp/search_list.html', {'result1':result1, 'result3':result3, 'result4':result4})

@cache_control(no_cache=True, must_revalidate=True)
def send_friend_request(request,user_id):
	user_1 = get_object_or_404(User, pk=user_id)
	user_id = request.session.get('user_id')
	if user_id is not None:
		user_2 = User.objects.get(id=user_id)
	else :	
		user_2 = request.user
	f = Friend_request(to_friend_req=user_1.user_profile,from_friend_req=user_2.user_profile)
	f.save()
	content = "You have a friend request from " + user_2.first_name + " " + user_2.last_name
	send_mail('Smartfeed-Friend Request',content,'persontest42@gmail.com',[user_1.email], fail_silently=False)
	your_search_query = request.session.get('your_search_query')
	request.session['your_search_query'] = your_search_query
	return HttpResponseRedirect('/myapp/search_results/')

@login_required
def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/myapp/')		

@login_required
def view_requests(request):	
	user_id = request.session.get('user_id')
	if user_id is not None:
		user = User.objects.get(id=user_id)
	else :	
		user = request.user
	user_profile = user.user_profile
	return render(request,"myapp/view_requests.html", {"user_profile":user_profile})

@login_required
def make_friends(request, decision, frndreq_id):
	r = get_object_or_404(Friend_request, pk=frndreq_id)
	user_id = request.session.get('user_id')
	if user_id is not None:
		user = User.objects.get(id=user_id)
	else :	
		user = request.user
	user_profile = user.user_profile

	if int(decision) == 1:
		f = Friendship(to_friend=r.to_friend_req,from_friend=r.from_friend_req)
		f.save()
		r.delete()
		return HttpResponseRedirect('/myapp/view_requests')
	else:
		r.delete()
		return HttpResponseRedirect('/myapp/view_requests')

def update(request, child_id):
	
	user_id = request.session.get('user_id')
	if user_id is not None:
		user = User.objects.get(id=user_id)
	else :	
		user = request.user
	u_profile = user.user_profile
	q = get_object_or_404(Child, pk=child_id)
	child = Child.objects.get(pk=q.id)
	form = Child_Profile_Form(instance=child)
	request.session['child_id'] = child.id
	return render(request, 'myapp/update.html', { 'form': form })

def cprofile(request):
	# search_form = Search_Form()
	user_id = request.session.get('user_id')
	if user_id is not None:
		user = User.objects.get(id=user_id)
	else :	
		user = request.user
	u_profile = user.user_profile
	cform = Child_Profile_Form(request.POST,request.FILES)
	# return HttpResponse(cform)
	if cform.is_valid():
		data = cform.cleaned_data
		cprofile = u_profile.child_set.create(name=data['name'],dob=data['dob'],gender=data['gender'],image=data['image'],grade=data['grade'])
		return render(request,"myapp/home.html",{"name":cprofile.name,"user_profile":u_profile})
	else :
		return render(request,"myapp/child_setup.html",{"cform":cform})		

def cprofile_update(request):
	user_id = request.session.get('user_id')
	if user_id is not None:
		user = User.objects.get(id=user_id)
	else :	
		user = request.user
	u_profile = user.user_profile
	child_id = request.session.get('child_id')
	q = get_object_or_404(Child, pk=child_id)
	child = Child.objects.filter(pk=q.id)
	cform = Child_Profile_Form(request.POST,request.FILES)
	if cform.is_valid():
		data=cform.cleaned_data
		child.delete()
		cprofile = u_profile.child_set.create(name=data['name'],dob=data['dob'],gender=data['gender'],grade=data['grade'],image=data['image'])
		# child.update(name=data['name'],dob=data['dob'],gender=data['gender'],image=data['image'],grade=data['grade'])
		return render(request,"myapp/home.html",{"user_profile": u_profile})


# 
def home(request):
	user_id = request.session.get('user_id')
	if user_id is not None:
		user_2 = User.objects.get(id=user_id)
	else :	
		user_2 = request.user
	user_profile = user_2.user_profile	
	return render(request,"myapp/home.html",{"user_profile":user_profile})

def friend_list(request):
	user_id = request.session.get('user_id')
	if user_id is not None:
		user_2 = User.objects.get(id=user_id)
	else :	
		user_2 = request.user
	user_profile = user_2.user_profile	
	return render(request,"myapp/friend_list.html", { 'user_profile':user_profile })
