from django.urls import path, include
from . import views

app_name = 'commonLocations'
urlpatterns = [
    # anonym user
    #path('', views.index, name='index'  ),
    #path('fr/', views.index_fr, name='index_fr'  ),
    path('index/<str:lang>/', views.index, name='index_vente'  ),
    path('details/<int:v_id>/<str:lang>/', views.details, name='details_vente'),

    # authentificated user
    path('create/<str:lang>/', views.create, name='create_vente'),
   
    path('index/user/<str:lang>/', views.index_user, name='index_user_vente'  ),
    path('details/users/<int:v_id>/<str:lang>/', views.details_users, name='details_users_vente'),

    path('delete/<int:v_id>/<int:why_delete>/<str:lang>/', views.delete, name='delete_vente'),
    path('update/<int:v_id>/<str:lang>/', views.update, name='update_vente'),

    #
    path('recherche/<str:lang>/', views.recherche , name='recherche_vente'),
    path('recherche_handler/<str:lang>/', views.recherche_handler , name='recherche_handler_vente'),

    path('recherche_avence/<str:lang>/', views.recherche_avence , name='recherche_avance_vente'),
    path('recherche_avence_h/<str:lang>/', views.recherche_avence_handeler , 
           name='recherche_avance_h_vente'),
    
    
   

] 