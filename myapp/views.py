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
    if download:
        return generate_pdf(id=id, download=True)
    #  domain = Site.objects.get_current().domain
    #  url = 'http://{domain}/download/{id}'.format(domain=domain)
    
# home or index page, it also serves as the login page
def index(request):
    return render(request, 'index.html')





# dashboard page to create and see all transcations
@login_required(login_url='/')
def dashboard(request):
    user = request.user
    transactions = Transaction.objects.filter(user_id=user.id).order_by('-created_at')
    return render(request, 'dashboard.html', {'transactions': transactions})





# create transaction with form in user dashboard
@login_required(login_url='/')
def create_transaction(request):
    if request.method == 'POST':
        name = request.POST['name']
        price = request.POST['price']
        phone = request.POST['phone']
        address = request.POST['address']
        
        if name == "" or price == "":
            messages.info(request, 'Name or Price not filled')
            return redirect('dashboard')
        else:
            user = request.user
            transaction = Transaction(user=user ,name=name, price=price, ref=f"{get_random_string(20)}", phone=phone, address=address)
            messages.info(request, 'Your transaction has been created successfully')
            transaction.save()
            return redirect('dashboard')
    else:
        messages.info(request, 'Wrong method called')
        return redirect('dashboard')
    return render(request, 'dashboard.html')





# create a new non admin account
def signup(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        # phone = request.POST['phone']
        email = request.POST['email']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']
        
        formdata = UserForm(request.POST)
        
        if formdata.is_valid(): 
            if password == confirmpassword:
                user = formdata.save(commit = False)
                user = User.objects.create_user(username=username, first_name=firstname, last_name=lastname, email=email, password=password)
                user.save()
                messages.info(request, 'Your account has been created successfully')
                return redirect('dashboard')
            else:
                messages.info(request, 'Passoword does not match')
                return redirect('login')
        else:
            # Redirect back to the same page if the data
            # was invalid
            messages.info(request, 'Something went wrong')
            return redirect('signup')
    return render(request, 'signup.html')
            
            
            
            
            
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