from django.urls import path
from . import views

urlpatterns = [
    path('', views.deliriumorbs, name="deliriumorbs"),
]