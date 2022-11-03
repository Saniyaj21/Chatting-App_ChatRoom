from django.urls import path
from . import views

urlpatterns=[


    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),

    path('', views.index, name='index'),
    path('first/', views.home, name='home'),
    path('games/', views.games, name='games'),
    path('devolopers/', views.devolopers, name='devolopers'),
    path('feedback/', views.feedback, name='feedback'),

    path('chat/<str:id>/', views.chat, name='chat'),
     path('delete-message/<str:pk>/', views.deleteMessage, name='delete-message'),
      path('create-room/', views.createRoom, name='create-room'),
      path('joinRoom/', views.joinRoom, name='joinRoom'),
      
    path('profile/<str:id>/', views.profile, name='profile'),
    path('editProfile/<str:id>/', views.edit_profile, name='edit_profile'),
    path('delete-room/<str:id>/', views.deleteRoom, name='delete-room'),
     
]