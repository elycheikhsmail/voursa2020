from django.db import models
from django.contrib.auth.models import User
#from simple_history.models import HistoricalRecords
#from django.utils.timezone import now
from django.utils import timezone
#import datetime
#now = datetime.datetime.now()

# Create your models here.

class TimeStamp(models.Model):
    date_add = models.DateTimeField(auto_now_add=True)
    date_last_change = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class Lieux(TimeStamp):
    nom = models.CharField(max_length=200)
    nom_ar = models.CharField(max_length=200,default='')
    def __str__(self):
        return self.nom
    def show(self,lang):
        if lang == 'fr':
            return self.nom
        else:
            return self.nom_ar

class CommonCategorie(TimeStamp):
    nom = models.CharField(max_length=200)
    nom_ar = models.CharField(max_length=200,default='')
    def __str__(self):
        return self.nom
    def show(self,lang):
        if lang == 'fr':
            return self.nom

    class Meta:
        abstract = True

class CategorieVente(CommonCategorie):
    pass
    
class CategorieLocation(CommonCategorie):
    pass
    
class ImageVentes(TimeStamp):
    img = models.ImageField(upload_to='images/ventes/') 
    #history = HistoricalRecords()

class ImageLocations(TimeStamp):
    img = models.ImageField(upload_to='images/locations/') 
    #history = HistoricalRecords()


class CommonArticle(TimeStamp):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    #categorie = models.ForeignKey(CategorieVente,on_delete=models.CASCADE)
    lieux = models.ForeignKey(Lieux,on_delete=models.CASCADE)
    prix = models.PositiveIntegerField( )
    desc = models.CharField(max_length=200)
    isActive = models.BooleanField(default=True)
    isPublier = models.BooleanField(default=False)
    isPublicite = models.BooleanField(default=False)
    isVendue = models.BooleanField(default=False)
    isRejected =  models.BooleanField(default=False)
    class Meta:
        abstract = True


class CommonVente( CommonArticle ):
    categorie = models.ForeignKey(CategorieVente,on_delete=models.CASCADE)
    images = models.ManyToManyField(ImageVentes,default=None)
    #history = HistoricalRecords()
    def __str__(self):
        return str(self.categorie)\
            +' - '+str(self.lieux)\
                +' - '+str(self.prix)+' - '+self.desc


class CommonLocation( CommonArticle ):
    categorie = models.ForeignKey(CategorieLocation,on_delete=models.CASCADE)
    images = models.ManyToManyField(ImageLocations,default=None)
    #history = HistoricalRecords()
    def __str__(self):
        return str(self.categorie)\
            +' - '+str(self.lieux)\
                +' - '+str(self.prix)+' - '+self.desc


class VenteRecheche(TimeStamp):
    categorie = models.ForeignKey(CategorieVente,on_delete=models.CASCADE)
    lieux = models.ForeignKey(Lieux,on_delete=models.CASCADE)
    prix_min = models.PositiveIntegerField( )
    prix_max = models.PositiveIntegerField( )

    #history = HistoricalRecords()

class VenteRecheche1(TimeStamp):
    categorie = models.ForeignKey(CategorieVente,on_delete=models.CASCADE)
    lieux = models.ForeignKey(Lieux,on_delete=models.CASCADE)
    prix = models.PositiveIntegerField( )

    #history = HistoricalRecords()



class LocationRecheche(TimeStamp):
    categorie = models.ForeignKey(CategorieLocation,on_delete=models.CASCADE)
    lieux = models.ForeignKey(Lieux,on_delete=models.CASCADE)
    prix_min = models.PositiveIntegerField( )
    prix_max = models.PositiveIntegerField( )

    #history = HistoricalRecords()


class LocationRecheche1(TimeStamp):
    categorie = models.ForeignKey(CategorieLocation,on_delete=models.CASCADE)
    lieux = models.ForeignKey(Lieux,on_delete=models.CASCADE)
    prix = models.PositiveIntegerField( )

    #history = HistoricalRecords()



class TelCode(TimeStamp):
    code = models.CharField(max_length=200)
    tel = models.CharField(max_length=200) # unique by code
    isRegistred = models.BooleanField(default=False)
    #history = HistoricalRecords()
    def __str__(self):
        return self.tel+' / '+self.code


class AssistantAdmin(TimeStamp):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username


class SiteTel(TimeStamp):
    tel = models.CharField(max_length=200)
    def __str__(self):
        return self.tel

