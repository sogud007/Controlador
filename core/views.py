from django.shortcuts import render
from django.conf import settings
from github import Github, GithubException
import requests
import core.functions
import json

def index(request):
    return render(request, 'core/index.html')

def logout(request):
    if "user" in request.session:
        request.session['login'] = False        
        del request.session['user']
        del request.session['propiedad']
        del request.session['noticias']
    return render(request, 'core/index.html')

def home(request):
    if(request.session['login']):
        return render(request, 'core/news.html') 
    else:
        mensaje = {}
        mensaje['mensaje'] = 'Login Incorrecto!'
        request.session['login'] = False
        if request.method == 'POST':
            if ('userName' in request.POST):
                username = request.POST['userName']
                password = request.POST['password']
                url = "http://127.0.0.1:8000/Usuario/api/"
                response = requests.get(url)
                user = response.json()
                for u in user:
                    if (u['CORREO'] == username):
                        if (u['PASSWORD'] == password):
                            request.session['login'] = True
                            request.session['user'] = u
                            print (u)
                            unidad = u['ASIGNACION_UP'][0]['UNIDAD']
                            propiedad_id = core.functions.extractId(unidad['PROPIEDAD_ID'])         
                            propiedad = core.functions.getPropiedadHorizontal(propiedad_id)
                            request.session['propiedad'] = propiedad
                            noticias = core.functions.getNoticias(propiedad_id)
                            request.session['noticias'] = noticias
                            return render(request, 'core/news.html', {'usuario': u})    
                        else:
                            mensaje['mensaje'] = 'Contraseña Incorrecta'
                            return render(request, 'core/index.html', {'mensaje': mensaje})                    
                mensaje['mensaje'] = 'Usuario No Valido'
        return render(request, 'core/index.html', {'mensaje': mensaje})
    

def billing(request):
    user = request.session['user']
    unidad = user['ASIGNACION_UP'][0]['UNIDAD']
    unidad_id = core.functions.extractId(unidad['UNIDAD_PRIVADA_ID'])
    cuentas = core.functions.getCuentasCobro(unidad_id)    
    return render(request, 'core/billing.html', {'cuentas': cuentas})