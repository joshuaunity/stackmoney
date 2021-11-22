import io
from django.shortcuts import render, redirect
from django.http import HttpResponse, response
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Transaction
import random, string
from stackmoney.utils import render_to_pdf 
# incase and underscore shows on the restframework imports 
# and u have django and the django restframework modules or package 
# then u can ignore the underline
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from .serializers import TransactionSerializer
from django.contrib.auth.decorators import login_required
from .forms import UserForm
from .forms import TransactionForm
import urllib.request




# Generate reference code for new transaction
def get_random_string(length):
    # With combination of lower and upper case
    result_str = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(length))
    return result_str





# transaction api class for both fethcing and creating new transaction
class TransView(APIView):
    
    permission_classes = (
        IsAuthenticated,
    )
    # get users transactions
    def get(self, request, *args, **kwargs):
        user = request.user
        transactions = Transaction.objects.filter(user_id=user.id)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
        
    # create a new transaction under the current user
    def post(self, request, *args, **kwargs):
        name = request.POST['name']
        price = request.POST['price']
        phone = request.POST['phone']
        address = request.POST['address']
        user = request.user
        # return JsonResponse(  get_random_string(20) , safe=False)
        transaction = Transaction(user=user ,name=name, price=price, ref=f"{get_random_string(20)}", phone=phone, address=address)
        serializer = TransactionSerializer(transaction)
        content = JSONRenderer().render(serializer.data)
        stream = io.BytesIO(content)
        data = JSONParser().parse(stream)
        serializer = TransactionSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)





# function to generate pdf on donload button clicked
def generate_pdf(id, download):
    transaction = Transaction.objects.get(pk=id)
    data = {
            'id': transaction.id, 
            'name': transaction.name, 
            'ref': transaction.ref,
            'address': transaction.address,
            'phone': transaction.phone,
            'price': "{:,.2f}".format(transaction.price),
            'total': transaction.price,
            'date': transaction.created_at,
    }
    
    pdf = render_to_pdf('pdf/invoice.html', data)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = f"{data['name']}_%s.pdf" %("Receipt")
        content = "inline; filename=%s" %(filename)
        # download = req.GET.get("download")
        if download:
            content = "attachment; filename=%s" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")





# download reciept for transaction
@login_required(login_url='/')
def download_receipt(request, id):
    download = request.GET.get("download")
    # domain = Site.objects.get_current().domain
    # url = 'http://{domain}/download/{id}'.format(domain=domain)
                                                 
    if download:
        return generate_pdf(id=id, download=True)

    
    
    
    
    
# home or index page, it also serves as the login page
def index(request):
    return render(request, 'index.html')





# dashboard page to create and see all transcations
@login_required(login_url='/')
def dashboard(request):
    user = request.user
    form = TransactionForm() 
    transactions = Transaction.objects.filter(user_id=user.id).order_by('-created_at')
    return render(request, 'dashboard.html', {'transactions': transactions, 'form': form})





# create transaction with form in user dashboard
@login_required(login_url='/')
def create_transaction(request):
    if request.method == 'POST':
        name = request.POST['name']
        price = request.POST['price']
        phone = request.POST['phone']
        address = request.POST['address']
        
        formdata = TransactionForm(request.POST)
        
        if formdata.is_valid(): 
            transaction_data = formdata.save(commit = False)
            transaction = Transaction(user=request.user ,name=name, price=price, ref=f"{get_random_string(20)}", phone=phone, address=address)
            # messages.info(request, 'Your transaction has been created successfully')
            transaction.save()
            # return HttpResponse("form submitted successfully")
            messages.info(request, 'Your transaction has been created successfully')
            return redirect('dashboard')
        else:
            transactions = Transaction.objects.filter(user_id=request.user.id).order_by('-created_at')
            return render(request, "dashboard.html", {'form':formdata , 'transactions': transactions}) 
    else:
        form = TransactionForm()  
        return render(request, 'dashboard.html', {'form':form})
    




# create a new non admin account
def signup(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        # phone = request.POST['phone']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        formdata = UserForm(request.POST)
        
        if formdata.is_valid(): 
            user_data = formdata.save(commit = False)
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
            user.save()
            messages.info(request, 'Your account has been created successfully')
            return redirect('/')
        else:
            return render(request, "signup.html", {'form':formdata}) 
    else:
        form = UserForm()  
        return render(request, 'signup.html', {'form':form})
            
            
            
            
# login in exsiting user
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





# logout out currently login in user
def logout(request):
    auth.logout(request)
    return redirect('/')