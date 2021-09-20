from django.urls import path
from . import views


app_name = 'usersApp'
urlpatterns = [
    path('login/<str:lang>/', views.loginUser, name='login' ),
    path('logout/<str:lang>/',views.logoutUser,name='logout'),
    path('rpreRegister/<str:lang>/',views.preRegisterUser, name='preRegister'),
    path('register/<int:tel>/<str:lang>/',views.registerUser,name='register'),
    path('dashbord/<str:lang>/', views.dashboard, name='dash')
]