from django.urls import path
from . import views

urlpatterns = [
    path('', views.fossils, name="fossils"),
]