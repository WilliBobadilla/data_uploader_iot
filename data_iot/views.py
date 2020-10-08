from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect
from .models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from datetime import datetime



def index(request):
    if not request.user.is_authenticated:
        return render(request,'index.html')
    else:
        return redirect("/data")

def solcitud_login(request):
    """
    Aca se manejan las solicitudes de login 
    """
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    print("el usuario es: ", user )
    if user is not None and user.is_active: 
        login(request,user)
        return redirect('/data')
    return render(request,'index.html',{'mensaje':"Credenciales invalidas  "})

def logout_request(request):
    logout(request)
    # Redirecciona a la pagina de inicio 
    return HttpResponseRedirect("/")


@csrf_exempt 
def data(request):
    """
    Vista en donde se maneja el post, y tambien se envian \n
    datos al front-end si el metodo es get 
    """
    if request.method=='POST':#primero verificamos el token
        tokens= list(Token.objects.values_list('token', flat=True) )
        if request.POST.get('token') in tokens:# si esta en la lista, agrega 
            temp=request.POST.get('temp')
            fecha=request.POST.get('fecha')
            lat=request.POST.get('lat') 
            long=request.POST.get('long') 
            codigo_id= request.POST.get('codigo') # codigo del dispositivo 
            try:
                codigo= Codigo.objects.get(nombre=codigo_id)
            except: # no existe en la db, entonces vamos a crearlo 
                codigo= Codigo(nombre= codigo_id)
                codigo.save()
            datos= Medida(codigo=codigo,temperatura=temp,fecha=fecha,latitud=float(lat),longitud=float(long)  ) 
            datos.save()
            valores=Medida.objects.all() #hacemos un query 
            cantidad_valores=len(valores)
            return HttpResponse("Recibido! registro num: "+ str(cantidad_valores+1) )  
        else:
            return HttpResponse("No estas registrado para subir datos") 

    else:
        if not request.user.is_authenticated:
            return render(request,'index.html')
        valores=Medida.objects.all() #hacemos un query
        codigos= list(Codigo.objects.values_list("nombre",flat=True))
        cantidad_valores=len(valores)
        if cantidad_valores>12:
            valores= valores[cantidad_valores-12:] #agarramos los ultimos doce, si hay mas de 12 datos 
        datos=[]
        for dato in valores: 
            datos.append({"temperatura":dato.temperatura,"fecha":dato.fecha,"codigo":dato.codigo.nombre})
        
        return render(request,'grafica.html',{'datos':datos,"codigos":codigos,"title":"Grafica","modo":"normal"})

@csrf_exempt
def update_graph(request):
    """
    Vista en donde se actualiza el mapa \n
    en base a una solicitud por post
    """
    #if not request.user.is_authenticated:
        #return render(request,'index.html')
    
    codigo=request.POST.get("codigo")
    if codigo!="paraguay":
        valores= Medida.objects.filter(codigo__nombre__contains=codigo) #hacemos un query y traemos el de interes
    else: 
        valores=Medida.objects.all()
    cantidad_valores=len(valores)
    if cantidad_valores>12:#agarramos los ultimos 12 si es mas que 12 los datos 
        valores= valores[cantidad_valores-12:] 
    temps=[]
    fechas=[]
    for dato in valores: 
        temps.append(dato.temperatura)
        fechas.append(dato.fecha)  
    return JsonResponse({'valores':temps, 'fechas':fechas,"codigo":codigo })


def mapa(request):
    """
    Esta vista retorna el mapa de los dispositivos con su ubicacion y \n
    su ultima medicion 
    """
    if not request.user.is_authenticated:
        return render(request,'index.html')
    
    codigos= list(Codigo.objects.values_list("nombre",flat=True))
    print(codigos) 
    temps=[]
    fechas=[]
    lat=[]
    long=[]
    for codigo in codigos:
        valor=Medida.objects.filter(codigo__nombre__contains=codigo).last() #hacemos un query y ordenamos de forma descendente
        temps.append(valor.temperatura)
        fechas.append(valor.fecha)
        lat.append(valor.latitud)
        long.append(valor.longitud)
    datos= {'valores':temps, 'fechas':fechas, 'codigos':codigos,'lat':lat,'long':long}        
    return render(request,'mapa.html', {'datos':datos, 'title':"Mapa de Sensores","modo":'normal' }  )
#demos 
def demo_grafica(request):
    """
    Demo: devuelve la grafica con las mediciones
    """
    valores=Medida.objects.all() #hacemos un query
    codigos= list(Codigo.objects.values_list("nombre",flat=True))
    cantidad_valores=len(valores)
    if cantidad_valores>12:
        valores= valores[cantidad_valores-12:] #agarramos los ultimos doce, si hay mas de 12 datos 
    datos=[]
    for dato in valores: 
        datos.append({"temperatura":dato.temperatura,"fecha":dato.fecha,"codigo":dato.codigo.nombre})
    
    return render(request,'grafica.html',{'datos':datos,"codigos":codigos,"title":"Grafica","modo":"demo"})

def demo_mapa(request):
    """
    DEMO: Esta vista retorna el mapa de los dispositivos con su ubicacion y \n
    su ultima medicion 
    """
    codigos= list(Codigo.objects.values_list("nombre",flat=True))
    print(codigos) 
    temps=[]
    fechas=[]
    lat=[]
    long=[]
    for codigo in codigos:
        valor=Medida.objects.filter(codigo__nombre__contains=codigo).last() #hacemos un query y ordenamos de forma descendente
        temps.append(valor.temperatura)
        fechas.append(valor.fecha)
        lat.append(valor.latitud)
        long.append(valor.longitud)
    datos= {'valores':temps, 'fechas':fechas, 'codigos':codigos,'lat':lat,'long':long}        
    return render(request,'mapa.html', {'datos':datos, 'title':"Mapa de Sensores","modo":'demo' }  )