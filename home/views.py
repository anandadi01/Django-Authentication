import re
from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
# from django.contrib.auth import 


# password for amisha is aditya@01

# Create your views here.

def index(request):
    if request.user.is_anonymous:
        print(request.user)

        return redirect("/login")

    return render(request, 'index.html')

def loginUser(request):
    print("rahul")

    if request.method=="POST":
        # check if user has entered correct credentials
        print('working')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        print(username, password)

        user = authenticate(username= username, password= password) 

        if user is not None:
            # Backend authenticated the credentials
            # I am unable to fetch the password which user is typing
            # an due to this every user is getting considered as anonymous user
            # what should I do now coZ I am feeling helpless
            login(request, user, backend=None) 
            return redirect("/") 

        else:
            # No backend authenticated the credentials
            return render(request, 'login.html')

    return render(request, 'login.html')

def logoutUser(request):
    logout(request)
    return redirect("/login")
