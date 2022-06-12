from django.urls import path, include
from django.contrib import admin
from . import views
from users.views import Register

boost_list = views.BoostViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

boost_details = views.BoostViewSet.as_view({
    'put': 'partial_update',
})

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', Register.as_view(), name='register'),
    path('login/', views.UserLoginView, name='login'),
    path('cookie/', views.CookieView.as_view(), name='cookie'),

    path('tasks/', views.taskTables, name='tables'),
    path('taskCreate/', views.taskCreate, name='create'),

    path('game/', views.Game, name='game'),

    path('update_coins/', views.update_coins),
    path('core/', views.get_core),
    path('boosts/', boost_list, name='boosts'),
    path('boosts/<int:pk>/', boost_details, name='buy_boosts'),
]
