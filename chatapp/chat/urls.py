from django.urls import path

from . import views

urlpatterns = [
    path("trigger/", views.trigger, name="trigger"),
    path('', views.index, name='index'),
    path('<str:room_name>/', views.room, name='room'),

]
