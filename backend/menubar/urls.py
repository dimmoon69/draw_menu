from django.urls import path

from backend.menubar.views import home

urlpatterns = [
    path('', home, name='home'),
    path('<slug>/', home, name='home'),
    path('<slug>/<path:url>/', home, name='home')
]
