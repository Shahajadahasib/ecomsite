from django.contrib import admin
from django.urls import include, path
from .views import Index, Signup, Login

import ecomsite.urls
urlpatterns = [
    path('', Index.as_view(), name='index'),
    # path('login', Login.as_view()),
    # path('', views.Index.as_view(), name='index'),
    path('signup', Signup.as_view()),
    path('login', Login.as_view()),


]
