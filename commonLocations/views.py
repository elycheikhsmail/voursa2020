from django.shortcuts import render
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
from baseApp.forms import (
    CommonLocationsForm, 
    RechecheLocationForm1,
    RechecheLocationForm2,
    ImageVentesForm
    )

from  baseApp.helpers import  prepare_lang


from . import db_requests


from django.core.paginator import Paginator


import datetime
from django.utils import timezone

from django.core.files.storage import default_storage


def index(request, lang):
    lang  = prepare_lang( lang )

    ventes_list = models.CommonLocation.objects\
        .filter(isPublier=True).filter(isActive=True)\
            .order_by('-date_add').all()
    n = len(ventes_list)

    paginator = Paginator(ventes_list,vente_per_page)

    page = request.GET.get('page')
    ventes = paginator.get_page(page)

    context = {
        'ventes':ventes,'request':request, 'n':n,'lang':lang}
    return render(request,'commonLocations/index.html', context)

def details(request,v_id, lang):
    prepare_lang( lang )
    v = models.CommonLocation.objects.filter(isPublier=True).filter(isActive=True).filter(pk=v_id).first()
    if v is None:
        return HttpResponseRedirect(reverse('CommonLocations:index_vente',args=(lang,) ) )
    context = {'vente':v,'request':request, 'lang':lang }
    return render(request,'commonLocations/details.html', context)

def details_users(request,v_id, lang):
    lang  = prepare_lang( lang )
    print('user',request.user)
    print('is auth ',request.user.is_authenticated )
    if request.user.is_authenticated :
        user = request.user
        print(user)
        v = models.CommonLocation.objects.filter(isActive=True).filter(pk=v_id).filter(user=user).first()
        if v is None :
            return HttpResponseRedirect(reverse('usersApp:login',args=(lang,)) )
        else:
            context = {'vente':v,'request':request, 'lang':lang}
            return render(request,'commonLocations/details_user.html', context)
    else:
        return HttpResponseRedirect(reverse('usersApp:login',args=(lang,)) )

    
# views for authentificate user
def index_user(request, lang):
    lang  = prepare_lang( lang )    
    print('user',request.user)
    print('is auth ',request.user.is_authenticated )
    if request.user.is_authenticated :
        user = request.user
        ventes_list = models.CommonLocation.objects\
            .filter(isActive=True).filter(user=user)\
                .order_by('-date_add').all()
        n = len(ventes_list)

        paginator = Paginator(ventes_list,vente_per_page)
        page = request.GET.get('page')
        ventes = paginator.get_page(page)
        context = {'ventes':ventes,'request':request,'auth':True ,'n':n, 'lang':lang}
        return render(request,'commonLocations/index.html', context)
    else:
        return HttpResponseRedirect(reverse('usersApp:login',args=(lang,)) )

def max_ventes_annonces(request,lang):
    pass

def create(request, lang):
    lang  = prepare_lang( lang )
    if  not request.user.is_authenticated : 
        return HttpResponseRedirect(reverse('usersApp:login',args=(lang,)))
    # tester si cette utilisateur a publier deja 5 annonces
    user = request.user
    ventes1 = models.CommonLocation\
        .objects.filter(isActive=True)\
            .filter(user=user)\
                .order_by('-date_add').reverse()[:5]
                    
    print(ventes1)
    now = timezone.now()
    if len(ventes1) > max_vente_annoce_by_day -1 :
        if now - ventes1[0].date_add < datetime.timedelta(days=1) :
            for item in ventes1:
                print(item.date_add)
            print(type(ventes1))
            print('------------')
            print(ventes1[0].date_add )
            print('------------')
            d = ventes1[0].date_add + datetime.timedelta(days=1)
            print( d)
            context = {'lang':lang, 'd':d}
            return render(request,'commonLocations/max_ventes_annonce.html',context)
           
    categories = models.CategorieLocation.objects.all()
    lieux = models.Lieux.objects.all()

    form_vide = CommonLocationsForm()
    context = {
        'form':form_vide,
        'lieux':lieux,
        'categories':categories,
        'request':request,
         'lang':lang
        }

    if request.method == 'POST':
        cvm = CommonLocationsForm(request.POST)
        #print('request.POST', request.POST)
        print('cvm.is_valid()' , cvm.is_valid() )
        if cvm.is_valid() : 
            cvm1 = models.CommonLocation()
            cvm1.user = request.user
            cvm1.categorie = cvm.cleaned_data['categorie']
            cvm1.lieux = cvm.cleaned_data['lieux']
            cvm1.prix = cvm.cleaned_data['prix']
            cvm1.desc = cvm.cleaned_data['desc']
            cvm1.save()
            return HttpResponseRedirect( reverse( 'imagesLocationsApp:create_img',args=(cvm1.id, lang)))
        else:
            context['form'] = cvm 
            return render(request,'commonLocations/create.html',context)
    return render(request,'commonLocations/create.html',context)

def delete(request,v_id, why_delete, lang):
    lang  = prepare_lang( lang )
    if request.user.is_authenticated :
        user = request.user
        v = models.CommonLocation.objects.filter(pk=v_id).filter(user=user).first()
        print(v)
        if v is None:
            return HttpResponseRedirect(reverse('CommonLocations:index_user_vente',args=(lang,)) )
        context = {'vente': v, 'request': request, 'v_id': v_id, 'lang': lang}
        if request.method == 'POST':
            try:

                print('post')
                v.isActive = False
                if v_id == 1:
                    v.isVendue = True
                for img in v.images.all():
                    if default_storage.exists(img.img.path) == True:
                        default_storage.delete(img.img.path)
                v.images.clear()
                v.save()
                return HttpResponseRedirect(reverse('commonLocations:index_user_vente', args=(lang,)))
            except:
                # msg = notre sys n'a pas retirer votre annonce
                # un probleme technique a eu lieu ..
                return render(request, 'commonLocations/delete.html', context)
        else:
            return render(request,'commonLocations/delete.html', context)
    else:
        return HttpResponseRedirect(reverse('usersApp:login') )

def update(request, v_id, lang):
    lang  = prepare_lang( lang )
    
    if not request.user.is_authenticated :
        return HttpResponseRedirect(reverse('usersApp:login',args=(lang,)) )
    else:
        user = request.user
        cvm = models.CommonLocation.objects.filter(pk=v_id).filter(user=user).first()
        print('vente model')
        print(cvm)
        if cvm is None:
            return HttpResponseRedirect(reverse('CommonLocations:index_user_vente',args=(lang,)))
        else:

            categories = models.CategorieLocation.objects.all()
            lieux = models.Lieux.objects.all()

            form_remplit1 = CommonLocationsForm( instance=cvm)
            context = {
                'form':form_remplit1,
                'vente':cvm,
                'lieux':lieux,
                'categories':categories,
                'lang':lang
                }
            if request.method == 'POST':
                form_remplit = CommonLocationsForm(request.POST)
                print('POST \n form_remplit.is_valid() \n',form_remplit.is_valid() ,'\n --- \n')
                print( form_remplit.errors)
                if form_remplit.is_valid() :
                    cvm.user = request.user
                    cvm.categorie = form_remplit.cleaned_data['categorie']
                    cvm.lieux = form_remplit.cleaned_data['lieux']
                    cvm.prix = form_remplit.cleaned_data['prix']
                    cvm.desc = form_remplit.cleaned_data['desc']
                    cvm.save()
                    return HttpResponseRedirect(reverse('CommonLocations:index_user_vente',args=(lang,)))
    
    return render(request,'commonLocations/update.html',context)


def recherche_avence(request, lang):
    lang  = prepare_lang( lang )

    form = RechecheLocationForm2
    categories = models.CategorieLocation.objects.all()
    lieux = models.Lieux.objects.all()
    context = {
        'form':form, # form vide
        'lieux':lieux,
        'categories':categories,
        'request':request,
         'lang':lang
        }
    return render(request,'commonLocations/recherche/rechercheForm2.html',context)



def recherche_avence_handeler(request, lang):
    lang  = prepare_lang( lang )
    if request.method == 'POST' :
        form2 = RechecheLocationForm2(request.POST)
        nbre_res = 0
        if form2.is_valid()  :
            isEXTRA = False
            categorie = form2.cleaned_data['categorie']
            lieux = form2.cleaned_data['lieux']

            prix = form2.cleaned_data['prix']
            
            ventes_list  = db_requests.recherche2(categorie,prix,lieux)
            n = len(ventes_list )
            nbre_res += n
            #number_inf_need_extra = 20 # and not need pagination
            ventes_extra = []
            if n < number_inf_need_extra :
                ventes_inf = db_requests.recherche2_inf(categorie,prix,lieux)
                ventes_sup = db_requests.recherche2_sup(categorie,prix,lieux)
                ventes_extra =  list(ventes_inf) + list(ventes_sup)
            
                if len(ventes_extra) > 0  :
                    isEXTRA = True
                    nbre_res += len(ventes_extra)
            cxt = {
                'ventes':ventes_list , 'ventes_extra':ventes_extra,'request':request,
                'isEXTRA':isEXTRA,
                'nbre_res': nbre_res ,
                'n':n,'lang':lang
                }
            return render( request, 'commonLocations/recherche/rechercheResult.html',  cxt)
      
    else:
        return HttpResponseRedirect( reverse('commonVente:recherche_vente',args =(lang,) ))

    

def recherche(request, lang):
    lang  = prepare_lang( lang )
    form = RechecheLocationForm2()
    categories = models.CategorieLocation.objects.all()
    context = {
        'form':form, # form vide
        'categories':categories,'request':request,
         'lang':lang
        }
    return render(request,'commonLocations/recherche/rechercheForm1.html',context)


def recherche_handler(request, lang):
    lang  = prepare_lang( lang )
    if request.method == 'POST' :
        print('post')
        form2 = RechecheLocationForm1(request.POST)
        nbre_res = 0
        if form2.is_valid()  :
            isEXTRA = False
            categorie = form2.cleaned_data['categorie']
            prix = form2.cleaned_data['prix']
           
            ventes_list  = db_requests.recherche1(categorie,prix)
            n = len(ventes_list )
            nbre_res += n
           # number_inf_need_extra = 1
            ventes_extra = []

            if n < number_inf_need_extra :
                ventes_inf = db_requests.recherche1_inf(categorie,prix)
                ventes_sup = db_requests.recherche1_sup(categorie,prix)
                ventes_extra =  list(ventes_inf) + list(ventes_sup)
                if len(ventes_extra) > 0  :
                    isEXTRA = True
                    nbre_res += len(ventes_extra)
            cxt = {
                'ventes':ventes_list ,
                'isEXTRA':isEXTRA ,
                'ventes_extra':ventes_extra,
                'request':request,
                'nbre_res':nbre_res ,
                'n':n,'lang':lang
                }
            print(cxt)
            return render(request, 'commonLocations/recherche/rechercheResult.html', cxt)
        else:
            return HttpResponseRedirect(
                reverse('commonLocation:recherche_vente',args =(lang,) )
            )

