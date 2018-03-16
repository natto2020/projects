from django.urls import path
from personal import views

urlpatterns = [
    path("", views.index, name ="index"),
    path("", views.test1, name ="test1"),
    ]
