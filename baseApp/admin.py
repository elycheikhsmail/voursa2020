from django.contrib import admin
from django.contrib import admin
from . import models
#from simple_history.admin import SimpleHistoryAdmin


class CommonVenteAdmin(admin.ModelAdmin):
    search_fields = [ 'user__username','prix']
    

class CommonLocationAdmin(admin.ModelAdmin):
    search_fields = [ 'user__username','prix']



class CodeTelAdmin(admin.ModelAdmin):
    search_fields = [ 'code','tel']
    

admin.site.register(models.Lieux)
admin.site.register(models.CategorieVente)
admin.site.register(models.CategorieLocation)

admin.site.register(models.CommonVente, CommonVenteAdmin) # SimpleHistoryAdmin,
admin.site.register( models.ImageVentes )

admin.site.register(models.CommonLocation , CommonLocationAdmin )
admin.site.register( models.ImageLocations )



admin.site.register(models.TelCode, CodeTelAdmin)

admin.site.register(models.AssistantAdmin)
admin.site.register(models.SiteTel)

