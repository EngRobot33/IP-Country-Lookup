from django.urls import path

from .views import GetCountryAPIView

urlpatterns = [
    path('get-country/', GetCountryAPIView.as_view(), name='get-country'),
]
