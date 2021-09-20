from baseApp import models
from django.db.models import Q

def recherche1(categorie,prix):
    ventes_list  = models.CommonVente.objects\
                .filter(isPublier=True).filter(isActive=True)\
                    .filter(categorie = categorie)\
                    .filter(prix = prix)\
                                .all()
    return ventes_list

def recherche1_inf(categorie,prix):
    ventes_extra =  models.CommonVente.objects\
        .filter(isPublier=True).filter(isActive=True)\
            .filter(categorie = categorie)\
                    .filter(prix__lt=prix)[:6]
                            
    print(ventes_extra)
    return ventes_extra

def recherche1_sup(categorie,prix):
    ventes_extra =  models.CommonVente.objects\
        .filter(isPublier=True).filter(isActive=True)\
            .filter(categorie = categorie)\
                    .filter(prix__gt=prix)[:6]
                            
    print(ventes_extra)
    return ventes_extra

def recherche2(categorie,prix ,lieux):
    ventes_list  = models.CommonVente.objects\
                .filter(categorie = categorie)\
                    .filter(isPublier=True).filter(isActive=True)\
                    .filter(lieux =lieux)\
                        .filter(prix = prix )\
                                .all()
    return ventes_list

def recherche2_inf(categorie,prix, lieux ):
    ventes_inf = models.CommonVente.objects\
        .filter(prix__lt = prix)\
                .filter(isPublier=True).filter(isActive=True)\
                    .filter(categorie = categorie)\
                        .filter(lieux =lieux)\
                                .order_by('prix')[:6]
    return ventes_inf


def recherche2_sup(categorie,prix, lieux ):
    ventes_inf = models.CommonVente.objects\
        .filter(prix__gt = prix)\
                .filter(isPublier=True).filter(isActive=True)\
                    .filter(categorie = categorie)\
                        .filter(lieux =lieux)\
                                .order_by('prix')[:6]
    return ventes_inf
