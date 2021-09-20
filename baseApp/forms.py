from django import forms
from .models import (
CommonVente, ImageVentes, 
CommonLocation, ImageLocations,
#CategorieLocation ,ImageLocations,
VenteRecheche1, LocationRecheche1
) 




class RechecheForm1(forms.ModelForm):
        class Meta:
            model = VenteRecheche1
            fields = ['categorie','prix']

class RechecheForm2(forms.ModelForm):
        class Meta:
            model = VenteRecheche1
            fields = ['categorie','lieux',  'prix' ]

class RechecheLocationForm1(forms.ModelForm):
        class Meta:
            model =  LocationRecheche1
            fields = ['categorie','prix' ]

class RechecheLocationForm2(forms.ModelForm):
        class Meta:
            model =  LocationRecheche1
            fields = ['categorie','lieux',   'prix']
        
      


    
class  CommonVentesForm(forms.ModelForm):
    class Meta:
        model = CommonVente
        fields = ['categorie','lieux', 'prix', 'desc']
        
        
class  ImageVentesForm(forms.ModelForm):
    class Meta:
        model = ImageVentes
        fields = ['img',]
        
  
class  CommonLocationsForm(forms.ModelForm):
    class Meta:
        model = CommonLocation
        fields = ['categorie','lieux', 'prix', 'desc']
        
class  ImageLocationsForm(forms.ModelForm):
    class Meta:
        model = ImageLocations
        fields = ['img',]
        
