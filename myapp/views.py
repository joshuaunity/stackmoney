from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Transaction
import random, string



# Create your views here.
def get_random_string(length):
    # With combination of lower and upper case
    result_str = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(length))
    # print random string
    return result_str
    
def index(request):
    return render(request, 'index.html')

def dashboard(request):
    user = request.user
    transactions = Transaction.objects.filter(user_id=user.id)
    return render(request, 'dashboard.html', {'transactions': transactions})

def create_transaction(request):
    if request.method == 'POST':
        name = request.POST['name']
        price = request.POST['price']
        
        if name == "" or price == "":
            messages.info(request, 'Name or Price not filled')
            return redirect('dashboard')
        else:
            user = request.user
            # transaction = Transaction.objects.create_transaction(name=name, price=price)
            transaction = Transaction(user=user ,name=name, price=price, ref=get_random_string(20))
            messages.info(request, 'Your transaction has been created successfully')
            transaction.save()
            return redirect('dashboard')
        
    return render(request, 'dashboard.html')

def signup(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']


        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username already used')
            return redirect('signup')
        elif username == "":
            messages.info(request, 'fill in your username')
            return redirect('signup')
        elif User.objects.filter(email=email).exists():
            messages.info(request, 'Email already used or you didnt fill in your email')
            return redirect('signup')
        elif email == "":
            messages.info(request, 'Fill in your email')
            return redirect('signup')
        else:
            if password == confirmpassword:
                user = User.objects.create_user(username=username, email=email, password=password)
                messages.info(request, 'Your account has been created successfully')
                user.save();
                return redirect('dashboard')
            else:
                messages.info(request, 'Passoword does not match')
                return redirect('signup')
    else:
        return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            fail = False
            auth.login(request, user)
            return redirect('dashboard')
        else:
            fail = True
            messages.info(request, 'User does not exist')
            return redirect('index')
    
    return render(request, '/')

def logout(request):
    auth.logout(request)
    return redirect('/')