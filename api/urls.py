from django.urls import path, include

urlpatterns = [
    path('ip/', include('ip.urls')),
]
