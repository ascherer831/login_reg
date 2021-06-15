from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('user/create', views.create),
    path('user/login', views.login),
    path('user/success', views.success),
    path('user/logout', views.logout)

]