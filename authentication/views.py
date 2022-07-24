from email.message import EmailMessage
from telnetlib import LOGOUT
from cmath import log
import imp
from operator import imod
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from aditya import settings
from django.core.mail import send_mail
from . token import generate_token
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text


# all my functions starts here

def home(request):
    return render(request, "authentication/index.html")

def signup(request):

    print('signup definition working')

    if request.method == 'POST':

        print('hey there')
        
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')  
        print('if also working')

        if User.objects.filter(username = username):
            messages.error(request, "Username already taken, please try something different")
            return redirect('signup')

        if User.objects.filter(email = email):
            messages.error(request,"Email already in use, please try something different")
            return redirect('signup')

        if len(username) > 10:
            messages.error(request,"Username should contain maximum 10 characters")
            return redirect('signup')

        if pass1 != pass2:
            messages.error(request,"Passwords do not match. Please fill it carefully")
            return redirect('signup')

        if not username.isalnum():
            messages.error(request,"Username must be alpha-numeric")
            return redirect('signup')

        myuser = User.objects.create_user(username, email, pass1)
        # myuser = User.objects.crear(username, email, pass1)
        print('dekhte hain')
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False

        myuser.save()
        messages.success(request, "Your account has been succefully created\nCheck your email to verify the account for its activation")

        # WELCOME MESSAGE VIA EMAIL 

        subject = "Welcome to ANAND'S BUSINESS- DJANGO LOGIN !!"
        message = "Hello"+ myuser.first_name + " !!\n"+ "Welcome to ANAND'S BUSINESS\nThank you for chosing ANAND'S Platform to grow yourself\nWe have aso sent you an another email for activating your account. Plese checkout and confirm the email.\n\n Thank you\nAditya ANAND\nFounder"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        print('send ho rha hai')

        # AND SENDING CONFIRMATION EMAIL
        current_site = get_current_site(request)
        email_subject = "Confirm your Email @ GFG - Django Login!!"
        message2 = render_to_string('email_confirmation.html',{
            
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
        email_subject,
        message2,
        settings.EMAIL_HOST_USER,
        [myuser.email],
        )
        email.fail_silently = True
        email.send()

        return redirect('signin')

    return render(request, "authentication/signup.html")
    # Aditya x

def signin(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')
        
        user = authenticate(username=username, password = pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "authentication/index.html", {'fname': fname})

        else:
            messages.error(request, 'Wrong Credentials')
            return redirect('home')

    return render(request, "authentication/signin.html")

def signout(request):
    # return render(request, 'authentication/signup.html')
    logout(request) 
    messages.success(request, "Logged out successfully !!")
    return redirect("home")
