from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
# Create your views here.
def register(request):
    if request.method == 'POST':

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email =request.POST['email']
        password = request.POST['password']
        conf_password = request.POST['conf_password']
        print("got data!")
        if password == conf_password:
            if User.objects.filter(username=username).exists():
                print("Username Taken!")
                messages.error(request,"Username Taken!")
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    print("mail Taken!")
                    messages.error(request, "Email Taken")
                    return redirect('register')
                else:
                    user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
                    user.save()
                    print("User created!")
                    return redirect('login')
        else:
            print("Pass nom")
            messages.error(request, "Passwords do not match!")
            return redirect('register')
    else:
        return render(request, 'users/register.html')


def login(request):
    if request.method == 'POST':
        username=request.POST['username']
        password1=request.POST['password']
        user=auth.authenticate(username=username,password=password1)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.error(request,'Invalid Credentials')
            return redirect('login')
    else:
        return render(request,'users/login.html')
    
def logout(request):
	auth.logout(request)
	return redirect('/')