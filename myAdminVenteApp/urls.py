from django.urls import path, include
from . import views

app_name = 'myAdminVenteApp'
urlpatterns = [
   
    path('<str:lang>/',views.tels_codes, name='tels_codes' ),
    path('telscodes2/<str:lang>/',views.tels_codes2, name='tels_codes2' ),
    
    
    path('index/user/<str:lang>/', views.index_user, name='index_user_vente'  ),
    path('index2/user/<str:lang>/', views.index_user2, name='index_user_vente2'  ),
    
    
    path('details/users/<int:v_id>/<str:lang>/', views.details_users, name='details_users_vente'),
    path('details2/users/<int:v_id>/<str:lang>/', views.details_users2, name='details_users_vente2'),
    

    path('publier/<int:v_id>/<str:lang>/', views.publier_annonce, name='publier') ,
    path('publier2/<int:v_id>/<str:lang>/', views.publier_annonce2, name='publier2') ,
    
    
    path('rejeter/<int:v_id>/<str:lang>/', views.rejeter_annonce, name='rejeter'),
    path('rejeter2/<int:v_id>/<str:lang>/', views.rejeter_annonce2, name='rejeter2'),


   

] 