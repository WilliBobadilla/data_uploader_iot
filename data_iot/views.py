from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect
from .models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login

# Create your views here.
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
    # Redirect to a success page.
    return HttpResponseRedirect("/")


@csrf_exempt 
def data(request):
    if not request.user.is_authenticated:
        return render(request,'index.html')
    """
    Vista en donde se maneja el post y se envia los datos al front
    """
    if request.method=='POST':
        temp=request.POST.get('temp')
        fecha=request.POST.get('fecha')
        lat=request.POST.get('lat') 
        long=request.POST.get('long') 
        codigo_id= request.POST.get('codigo') # id de la ciudad
        try:
            codigo= Codigo.objects.get(nombre=codigo_id)
        except: # no existe en la db, entonces vamos a crearlo 
            codigo= Codigo(nombre= codigo_id)
            codigo.save()
        datos= Medida(codigo=codigo,temperatura=temp,fecha=fecha,latitud=float(lat),longitud=float(long)  ) 
        datos.save()
        valores=Medida.objects.all() #hacemos un query 
        cantidad_valores=len(valores)
        return HttpResponse("Recibido! registro num: "+ str(cantidad_valores+1) )  #render(request,'grafica.html',{'valores':temps, 'fechas':fechas })
    else:
        valores=Medida.objects.all() #hacemos un query 
        cantidad_valores=len(valores)
        if cantidad_valores>12:
            valores= valores[cantidad_valores-12:] 
        temps=[]
        fechas=[]
        for dato in valores: 
            temps.append(dato.temperatura)
            fechas.append(dato.fecha)  
        print(valores)
        
        return render(request,'grafica.html',{'valores':temps, 'fechas':fechas })

def update(request):
    if not request.user.is_authenticated:
        return render(request,'index.html')
    valores=Medida.objects.all() #hacemos un query 
    cantidad_valores=len(valores)
    if cantidad_valores>12:
        valores= valores[cantidad_valores-12:] 
    temps=[]
    fechas=[]
    for dato in valores: 
        temps.append(dato.temperatura)
        fechas.append(dato.fecha)  
    return JsonResponse({'valores':temps, 'fechas':fechas })


def mapa(request):
    if not request.user.is_authenticated:
        return render(request,'index.html')
    """
    Esta vista retorna el mapa de los dispositivos con su ubicacion y \n
    su ultima medicion 
    """
    valores=Medida.objects.all().order_by('-id') #hacemos un query y ordenamos de forma descendente
    agregados=[] # almacenamos los ya agregados 
    temps=[]
    fechas=[]
    lat=[]
    long=[] 
    for dato in valores:
        if not dato.codigo.nombre in agregados: # vemos si es que no esta 
            agregados.append(dato.codigo.nombre) # agregamos a la lista de los ya agregados
            temps.append(dato.temperatura)
            fechas.append(dato.fecha)
            lat.append(dato.latitud)
            long.append(dato.longitud) 
    rango= [ str(rango) for rango in range(len(agregados)) ] 
    datos= {'valores':temps, 'fechas':fechas, 'codigos':agregados,'lat':lat,'long':long,'range':rango }
    print(datos)         
    return render(request,'mapa.html', {'datos':datos}  )
    