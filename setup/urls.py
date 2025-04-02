# from django.contrib import admin
from django.urls import path, include
# from data_sync.views import CashierViewset
# from rest_framework import routers


# router = routers.DefaultRouter()
# router.register('cashiers', CashierViewset, basename='Cashiers')

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('', include(router.urls))
    path('data_sync/', include('apps.data_sync.urls'))
]
