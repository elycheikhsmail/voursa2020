from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import PBKDF2PasswordHasher

from django.contrib.auth.models import User
from baseApp.models import TelCode , SiteTel

from django.http import  *
from django.urls import reverse

from  baseApp.helpers import  prepare_lang

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import *
from django.views.generic import TemplateView

from django.conf import settings



import random
def get_random():
    lst = []
    for item in range(4):
        lst.append( random.choice(['0','1','2','3','4','5','6','7','8', '9']))
    txt = ''.join(lst)
    return txt



def loginUser(request, lang):
    lang  = prepare_lang( lang )
    #  template_name = 'eboutque/ventes/index.html'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password) #
        print('user')
        print(user)
        if user is not None :
            login(request, user)
            # plus tard redirection vers index_user
            return HttpResponseRedirect(reverse('commonVentes:index_user_vente',args=(lang,)))
    context = {'lang':lang}
    return render(request,'usersApp/login.html',context)

def logoutUser(request, lang):
    lang  = prepare_lang( lang )
    logout(request)
    context = {'lang':lang}
    return HttpResponseRedirect(reverse('commonVentes:index_vente',args=(lang,)))

def preRegisterUser(request, lang):
    lang  = prepare_lang( lang )
    context = {'lang':lang,'error':''}
    if request.method == 'POST':
        tel = request.POST['tel']
        # validation
        try:
            tel1 = int(tel)
            if  20000000 > tel1 or tel1 > 49999999 :
                error = ''' le numero doit etre compris entre 2000000 et 49999999 ,
                donc un numero de portable valable
                '''
                context['error'] = error
                return render(request,'usersApp/tel.html',context)
        except:
            error='le numero doit etre compose de huis chiffre sans espace'
            context['error'] = error
            return render(request,'usersApp/tel.html',context)
        telcode = TelCode.objects.filter(tel=tel).first()
        if telcode is None :
            # si le numero n'exist pas dans la base de donnee
            telCode = TelCode(code=get_random() ,tel=tel)
            telCode.save()
        else :
            telcode.code = get_random()
            telcode.save()
            
        #?
         # si le numero existe deja dans la base de donnee
         # regarder la derniere envoi du sms 
         # si c'est plus de 24 heure
         # lui envoyer le code 


         # sinon informer lui que le sms est envoyer il y a mois de 24
         # donc il regarde son tel  ou appeller le numero 
        print('code saved')
        
        return HttpResponseRedirect(reverse('usersApp:register',args=(tel,lang,)))
    
    return render(request,'usersApp/tel.html',context)
  

def registerUser(request, tel, lang):
    lang  = prepare_lang( lang )
    context = {'lang':lang,'tel':tel,
               'site_tel': SiteTel.objects.first()
                }
    if request.method == 'POST':
        username = tel
        code = request.POST['code']
        password = request.POST['password']
        telCode = TelCode.objects.filter(tel=tel).filter(code=code).first()
        if telCode is None:
            context['error']= 'code invalide'
            return render(request,'usersApp/register.html',context)
        u = User.objects.filter(username=username).first()
        if u is  None :
            user = User()
            user.username = tel
            user.set_password(password)
            user.save()
            telCode.isRegistred = True
            telCode.save()
            login(request, user)
            print('registred with succes')
            return HttpResponseRedirect(reverse('commonVentes:index_user_vente',args=(lang,)))
        else:
            u.set_password(password)
            u.save()
            telCode.isRegistred = True
            telCode.save()
            login(request, u)
            print('registred with succes')
            return HttpResponseRedirect(reverse('commonVentes:index_user_vente',args=(lang,)))
    
            
    return render(request,'usersApp/register.html',context)



def dashboard(request, lang):
    lang  = prepare_lang( lang )
    context = {'lang':lang}
    return render(request,'usersApp/dashboard.html',context)

