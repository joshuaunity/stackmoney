from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('logout', views.logout, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('transaction.create', views.create_transaction, name='createtransaction'),
    path('download/<str:id>', views.download_receipt, name='download_receipt'),
    # path('download/<str:id>', views.generate_pdf, name='generatepdf'),
]