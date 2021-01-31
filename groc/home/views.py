from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.views.generic import ListView,DeleteView
import datetime
from .models import Grocery



# Create your views here.
def home(request):
    if(request.user.is_authenticated):
        current_user = request.user
        context = {
            'groceries' : Grocery.objects.filter(owner = current_user),
        }
        return render(request,'home/index.html',context )
    else:
        return render(request,'home/index.html')
        



def update(request):
    if request.method == 'POST':
        iday = request.POST['id']
        try:
            g = Grocery.objects.filter(owner = request.user).get(id=iday)
            g.name = request.POST['name']
            g.quantity = request.POST['quantity']
            g.status = request.POST['status']
            date = request.POST['date']
            date = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%d-%m-%y')
            g.date = datetime.datetime.strptime(date, '%d-%m-%y')
            owner = request.user
            g.save()
            return redirect('/')
        except:
            messages.error(request,'Not Found! or Details are Incomplete')
            return render(request,'home/update.html')
        
        
        
        
    else:
        return render(request,'home/update.html')
    



def add(request):
    if(request.user.is_authenticated):
        if request.method == 'POST':
            name = request.POST['name']
            quantity = request.POST['quantity']
            status = request.POST['status']
            date = request.POST['date']
            date = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%d-%m-%y')
            date = datetime.datetime.strptime(date, '%d-%m-%y')
            owner = request.user
            
            item = Grocery(name =name,quantity=quantity,status = status,date_given = date, owner = owner)
            item.save()
            print("grocery created!")
            return redirect('/')
        else:
            return render(request,'home/add.html')
    else:
        return render(request, 'users/login.html')
    
def delete(request):
    if request.method == 'POST':
        iday = request.POST['id']
        try:
            g = Grocery.objects.filter(owner = request.user).get(id=iday)
            g.delete()
            print('Deleted')
            return redirect('/')
        except:
            messages.error(request,'Enter Correct Id')
            return render(request,'home/delete.html')
    else:
        return render(request, 'home/delete.html')

def filter(request):
    if(request.user.is_authenticated):
        if request.method == 'POST':
            date = request.POST['date']
            date = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%d-%m-%y')
            date = datetime.datetime.strptime(date, '%d-%m-%y')
            
            filtered_context ={
                'groceries': Grocery.objects.filter(date_given = date,owner=request.user).all()
            }
            print(filtered_context['groceries'])
            if not filtered_context['groceries'].exists():
                print("not found any element")
                messages.info(request,"No Items found for that date!")
                return render(request,'home/index.html')
            
            return render(request,'home/index.html',filtered_context)
        else:
            print("REquest was not post")
            return redirect('/')

    else:
        return render(request,"users/login.html")

    