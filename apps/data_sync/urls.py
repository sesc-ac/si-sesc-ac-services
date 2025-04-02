from django.urls import path

from .views import *

app_name = 'data_sync'

urlpatterns = [
    path('cashiers/', cashiers, name='cashiers')
]