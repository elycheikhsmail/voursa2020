from django.urls import path
from . import views

app_name = 'imagesVentesApp'
urlpatterns = [
    path('<int:vente_id>/<str:lang>/', views.create, name='create_img'),
    path('<int:img_id>/<int:vente_id>/<str:lang>/', views.delete, name='delete_img'),
   


] 