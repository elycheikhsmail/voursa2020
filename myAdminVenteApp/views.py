from django.shortcuts import get_object_or_404, render

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse

from django.utils.translation import get_language, get_language_bidi

from baseApp import models
from  baseApp.AppSettings import (
    vente_per_page,
    max_vente_annoce_by_day,
    number_inf_need_extra
    )

from  baseApp.helpers import  prepare_lang

from django.core.paginator import Paginator
import json

import datetime
from django.utils import timezone

# assurer code celui accede est bien admin avec les droit

def tels_codes(request, lang):
    lang  = prepare_lang( lang )    
    if request.user.is_authenticated :
        print(request.user)
        if  len(models.AssistantAdmin.objects.filter(user = request.user).all()) == 0 :
            return HttpResponseRedirect(reverse( 'usersApp:login',args=(lang,)))
        telscodes = models.TelCode.objects.filter(isRegistred = False).order_by('tel').all()
        context = {'lang':lang, 'telscodes':telscodes ,'status':'les nouveaux utilisateurs'  }
        return render(request, 'myAdminVenteApp/tels_codes.html',context )
    else:
        return HttpResponseRedirect(reverse( 'usersApp:login',args=(lang,)))
        


def tels_codes2(request, lang):
    lang  = prepare_lang( lang )    
    if request.user.is_authenticated :
        if  len(models.AssistantAdmin.objects.filter(user = request.user).all()) == 0 :
            return HttpResponseRedirect(reverse( 'usersApp:login',args=(lang,)))
        telscodes = models.TelCode.objects.filter(isRegistred = True ).order_by('tel').all()
        context = {'lang':lang, 'telscodes':telscodes ,'status':' ancienne utilisateur ' }
        return render(request, 'myAdminVenteApp/tels_codes.html',context )
    else:
        return HttpResponseRedirect(reverse( 'usersApp:login',args=(lang,)))


def details_users(request,v_id, lang):
    lang  = prepare_lang( lang )    
    if request.user.is_authenticated :
        if  len(models.AssistantAdmin.objects.filter(user = request.user).all()) == 0 :
            return HttpResponseRedirect(reverse( 'usersApp:login',args=(lang,)))
        v = models.CommonVente.objects.filter(isActive=True).filter(pk=v_id).first()
        if v is None :
            return HttpResponseRedirect(reverse('usersApp:login',args=(lang,)) )
        else:
            context = {'vente':v,'request':request, 'lang':lang}
            return render(request,'myAdminVenteApp/ventes/details_user.html', context)
    else:
        return HttpResponseRedirect(reverse('usersApp:login',args=(lang,)) )

def index_user(request, lang):
    lang  = prepare_lang( lang )    
    if request.user.is_authenticated :
        if  len(models.AssistantAdmin.objects.filter(user = request.user).all()) == 0 :
            return HttpResponseRedirect(reverse( 'usersApp:login',args=(lang,)))
        ventes_list = models.CommonVente.objects.filter(isActive=True)\
            .filter(isRejected = False)\
            .filter(isPublier=False)\
                .all()
        n = len(ventes_list)
        paginator = Paginator(ventes_list,vente_per_page)
        page = request.GET.get('page')
        ventes = paginator.get_page(page)
        context = {'ventes':ventes,'request':request,'auth':True ,'n':n, 'lang':lang}
        return render(request,'myAdminVenteApp/ventes/index.html', context)
    else:
        return HttpResponseRedirect(reverse('usersApp:login') )




def publier_annonce(request, v_id, lang):
    lang  = prepare_lang( lang )    
    if request.user.is_authenticated :
        if  len(models.AssistantAdmin.objects.filter(user = request.user).all()) == 0 :
            return HttpResponseRedirect(reverse( 'usersApp:login',args=(lang,)))
        cvm = models.CommonVente.objects.filter(pk=v_id).first()
        print('vente model')
        print(cvm)
        if cvm is None:
            # redirect vers index my admin
            return HttpResponseRedirect(reverse('myAdminVenteApp:index_user_vente',args=(lang,)))
        else:
            cvm.isPublier = True
            cvm.save()
            # redirect vers index my admin
            return HttpResponseRedirect(reverse('myAdminVenteApp:index_user_vente',args=(lang,)))
    else:
        return HttpResponseRedirect(reverse( 'usersApp:login',args=(lang,)))

def rejeter_annonce(request, v_id, lang):
    lang  = prepare_lang( lang )    
    if request.user.is_authenticated :
        if  len(models.AssistantAdmin.objects.filter(user = request.user).all()) == 0 :
            return HttpResponseRedirect(reverse( 'usersApp:login',args=(lang,)))
        cvm = models.CommonVente.objects.filter(pk=v_id).first()
        print('vente model')
        print(cvm)
        if cvm is None:
            # redirect vers index my admin
            return HttpResponseRedirect(reverse('myAdminVenteApp:index_user_vente',args=(lang,)))
        else:
            cvm.isRejected = True
            cvm.isPublier = False
            cvm.save()
            # redirect vers index my admin
            return HttpResponseRedirect(reverse('myAdminVenteApp:index_user_vente',args=(lang,)))
    else:
        return HttpResponseRedirect(reverse( 'usersApp:login',args=(lang,)))
        
def details_users2(request,v_id, lang):
    lang  = prepare_lang( lang )    
    if request.user.is_authenticated :
        if  len(models.AssistantAdmin.objects.filter(user = request.user).all()) == 0 :
            return HttpResponseRedirect(reverse( 'usersApp:login',args=(lang,)))
        v = models.CommonLocation.objects.filter(isActive=True).filter(pk=v_id).first()
        if v is None :
            return HttpResponseRedirect(reverse('usersApp:login',args=(lang,)) )
        else:
            context = {'vente':v,'request':request, 'lang':lang}
            return render(request,'myAdminVenteApp/locations/details_user.html', context)
    else:
        return HttpResponseRedirect(reverse('usersApp:login',args=(lang,)) )

    
# views for authentificate user
def index_user2(request, lang):
    lang  = prepare_lang( lang )    
    if request.user.is_authenticated :
        if  len(models.AssistantAdmin.objects.filter(user = request.user).all()) == 0 :
            return HttpResponseRedirect(reverse( 'usersApp:login',args=(lang,)))
        ventes_list = models.CommonLocation.objects.filter(isActive=True)\
            .filter(isRejected = False)\
            .filter(isPublier=False)\
                .all()
        n = len(ventes_list)

        paginator = Paginator(ventes_list,vente_per_page)
        page = request.GET.get('page')
        ventes = paginator.get_page(page)
        context = {'ventes':ventes,'request':request,'auth':True ,'n':n, 'lang':lang}
        return render(request,'myAdminVenteApp/locations/index.html', context)
    else:
        return HttpResponseRedirect(reverse('usersApp:login',args=(lang,)) )




def publier_annonce2(request, v_id, lang):
    lang  = prepare_lang( lang )    
    if request.user.is_authenticated :
        if  len(models.AssistantAdmin.objects.filter(user = request.user).all()) == 0 :
            return HttpResponseRedirect(reverse( 'usersApp:login',args=(lang,)))
        cvm = models.CommonLocation.objects.filter(pk=v_id).first()
        print('vente model')
        print(cvm)
        if cvm is None:
            # redirect vers index my admin
            return HttpResponseRedirect(reverse('myAdminVenteApp:index_user_vente2',args=(lang,)))
        else:
            cvm.isPublier = True
            cvm.save()
            # redirect vers index my admin
            return HttpResponseRedirect(reverse('myAdminVenteApp:index_user_vente2',args=(lang,)))
    else:
        return HttpResponseRedirect(reverse( 'usersApp:login',args=(lang,)))
        

def rejeter_annonce2(request, v_id, lang):
    lang  = prepare_lang( lang )    
    if request.user.is_authenticated :
        if  len(models.AssistantAdmin.objects.filter(user = request.user).all()) == 0 :
            return HttpResponseRedirect(reverse( 'usersApp:login',args=(lang,)))
        cvm = models.CommonLocation.objects.filter(pk=v_id).first()
        print('vente model')
        print(cvm)
        if cvm is None:
            # redirect vers index my admin
            return HttpResponseRedirect(reverse('myAdminVenteApp:index_user_vente2',args=(lang,)))
        else:
            cvm.isRejected = True
            cvm.isPublier = False
            cvm.save()
            # redirect vers index my admin
            return HttpResponseRedirect(reverse('myAdminVenteApp:index_user_vente2',args=(lang,)))
    else :
        return HttpResponseRedirect(reverse( 'usersApp:login',args=(lang,)))
    

