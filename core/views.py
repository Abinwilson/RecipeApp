from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse


# Create your views here.

def home(request):
    return render(request,'home.html',{
        'title':'Home'
        })

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user is  None:
            # No backend authenticated the credentials.
            messages.error(request,"Invalid credentials. please check your username and password.")
            return redirect('core:signin')
        else:
            # A backend authenticated the credentials.
            login(request,user)
            return redirect('core:home')

    return render(request,'signin.html',{
        'title':'Signin'
    })

def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
               messages.error(request,"Entered Username is already taken")
               return redirect('core:signup')
            elif User.objects.filter(email=email).exists():
               messages.error(request,"Entered Email is already taken")
               return redirect('core:signup')
            else:
                new_user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
                new_user.save()
                # Log the user in using the credentials.
                user_credentials = authenticate(username=username,password=password)
                login(request,user_credentials)
                print("Account created successfully! welcome to our community.")
                return redirect('core:home')
        else:
            return HttpResponse("password not matching")
    return render(request,'signup.html',{
        'title':'Signup'
    })

def signout(request):
    logout(request)
    return redirect('core:signin')