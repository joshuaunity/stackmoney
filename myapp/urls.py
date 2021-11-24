from django.urls import path
from . import views
from .views import TransView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # landing page and also contains login 
    path('', views.index, name='index'),
    # login in the user
    path('login', views.login, name='login'),
    # create new user
    path('signup', views.signup, name='signup'),
    # logout the current logged in user
    path('logout', views.logout, name='logout'),
    # User dashboard, user lands here after logging in
    path('dashboard', views.dashboard, name='dashboard'),
    # create a new transaction
    path('createtransaction', views.create_transaction, name='createtransaction'),
    # url path to generate or download transactio receipt
    path('download/<str:id>', views.download_receipt, name='download_receipt'),
    
    
    #***
    #***
    # API PATHS ************
    #***
    #***
    # API to create a transaction
    path('api/transaction', TransView.as_view(), name='transaction'),
    # API to generate authentication token
    path('api/token', obtain_auth_token, name='gettoken'),
    
]