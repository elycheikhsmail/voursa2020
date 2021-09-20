from django.contrib import admin
from django.urls import path, re_path , include
from django.conf.urls.i18n import i18n_patterns

from django.conf import settings 
from django.conf.urls.static import static 

#from usersApp.views import 

urlpatterns = [

    path('admin/', admin.site.urls),
    path('usersApp/', include('usersApp.urls')),

    path('', include('commonVentes.urls')),
    path('myadmin/', include('myAdminVenteApp.urls')),

    path('locations/', include('commonLocations.urls')),

    path('imagesVentesApp/', include('imagesVentesApp.urls')),
    path('imagesLocationsApp/', include('imagesLocationsApp.urls')),

   #path('devApp/', include('devApp.urls')),
]


if settings.DEBUG: 
        urlpatterns += static(settings.MEDIA_URL, 
                              document_root=settings.MEDIA_ROOT) 
