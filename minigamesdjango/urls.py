"""
URL configuration for minigamesdjango project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from website import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path("add_word/", views.add_word, name="add_word"),
    path("start_cemantox/", views.start_cemantox, name="start_cemantox"),
    path("play_cemantox/", views.play_cemantox, name="play_cemantox"),
    path("reset_cemantox/", views.reset_cemantox, name="reset_cemantox"),
    path("start_pendu/", views.start_pendu, name="start_pendu"),
    path("play_pendu/", views.play_pendu, name="play_pendu"),
    path("reset_pendu/", views.reset_pendu, name="reset_pendu"),
    path('start_morpion/', views.start_morpion, name='start_morpion'),
    path('play_morpion', views.play_morpion, name='play_morpion'),
    path("reset_morpion/", views.reset_morpion, name='reset_morpion'),
]
