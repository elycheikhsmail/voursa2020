from django.shortcuts import render


from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse

from baseApp import models
from baseApp.forms import ImageVentesForm

from  baseApp.helpers import  prepare_lang
from  baseApp.AppSettings import allow_extensions , max_img

from django.core.files.storage import default_storage

# Create your views here.

def create(request,vente_id, lang):
    lang = prepare_lang( lang )
    vente = models.CommonVente.objects.filter(pk=vente_id).first()
    nombre_img = len(vente.images.all() )
    if nombre_img >= max_img :
        return HttpResponseRedirect(reverse('commonVentes:index_user_vente',args=(lang,)))

    print(vente)
    if vente is None :
        print('vente is non')
        return HttpResponseRedirect(reverse('commonVentes:index_user_vente',args=(lang,)))

    if request.method == 'POST':
        
        img = models.ImageVentes()
    
        data = request.FILES
        print(data['img'])
        print(data['img'].name)
        print('')
        lst = data['img'].name.split(".")
        print(lst)
        print("")
        if len(lst) < 2:
            return render(request,'imagesApp/create_pb.html' )
        else:
            if lst[-1] not in allow_extensions :
                return render(request,'imagesApp/create_pb.html' )


        form = ImageVentesForm(request.POST, request.FILES)  # , instance=img
        #print('form')
        
        print(form)
        print()
        if form.is_valid(): 
            img.img = form.cleaned_data['img']
            try :
                img.save()
                vente.images.add(img)
                print('img is added')
                return HttpResponseRedirect(reverse('commonVentes:index_user_vente',args=(lang,)))
            except:
                return render(request,'imagesVentesApp/create_pb.html' )
                
    else: 
        form = ImageVentesForm()
        context = {'form':form, 'lang':lang}
        return render(request,'imagesApp/create.html',context)

def delete(request,img_id,vente_id, lang):
    lang = prepare_lang( lang )
    if request.user.is_authenticated :
        if request.method == 'POST':
            #user =request.user
            print('post methd')
            #vente = models.CommonVente.objects.filter(pk=vente_id).first()
           # print(vente)
            img = models.ImageVentes.objects.filter(pk=img_id).first()
            if img is None:
                print('img is Non')
                return HttpResponseRedirect(reverse('commonVentes:index_user_vente',args=(lang,)))
            else:
                try :
                    # delete from file
                    if default_storage.exists(img.img.path) == True :
                        default_storage.delete(img.img.path )
                    # delete from db
                    img.delete()
                    print('img is deleted ')
                except:
                    pass
                return HttpResponseRedirect(
                    reverse('commonVentes:details_users_vente',args=(vente_id,lang))
                    )
        else:
            context = {'lang':lang}
            return render(request,'imagesApp/delete.html',context)
    else:
        HttpResponseRedirect(reverse('usersApp:login',args=(lang,)))
