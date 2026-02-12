from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.contrib import messages
from settle_subscribe.models import *
# User = settings.AUTH_USER_MODEL
# Create your views here.

@csrf_exempt
def login_page(request):

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print(password)
        user = authenticate(username=email,password=password)
        print(user)
        if user is not None:
            login(request,user)
            print('correct password')
            return redirect('/sign_in/')
        elif user is None: 
            print('wrong password')
            messages.error(request, "Invalid Password")
            return redirect('/sign_in/')   
    # now = datetime.datetime.now()
    # html = 'Welcome to login page' 
    # return HttpResponse(html)
    # return render(request, 'login.html')
    # template = loader.get_template('login.html')
    # return HttpResponse(template.render())
    return render(request, 'login.html')


# def authorize_login(request):
#     email = request.POST["email"]
#     password = request.POST["password"]
#     user = authenticate(request, username=email, password=password)
#     if user is not None:
#         login(request, user)
#         print("user found")
#         # Redirect to a success page.
#         ...
#     else:
#         print("user not found")


# def signup(request):
#     template = loader.get_template('signup.html')
#     return HttpResponse(template.render())
#     return HttpResponse(loader.get_template('register.html').render())

def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        # user = User.objects.get(email=email)
        user = User.objects.filter(email=email)
        if user.exists():
            messages.info(request,"Email Already Exists!")
            return redirect('/sign_up/') 
        elif(password==confirm_password):
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email
            )
            user.set_password(password)
            user.save
            messages.info(request, "Account created Successfully!")
            return redirect('/sign_up/')
        else:
            messages.info(request, "Account not created. Passwords don't match")

    
    return render(request, 'signup.html')



def dashboard(request):

    return render(request, 'dashboard.html')
