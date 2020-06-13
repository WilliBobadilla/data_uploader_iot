from django.shortcuts import render,HttpResponse
from .models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from datetime import datetime

@csrf_exempt 
def index(request):
    """
    Vista en donde se maneja el post y se envia los datos al front
    """
    if request.method=='POST':
        temp=request.POST.get('temp')
        fecha=request.POST.get('fecha')
        lat=request.POST.get('lat') 
        long=request.POST.get('long') 
        codigo_id= request.POST.get('ciudad') # id de la ciudad
        try:
            codigo= Codigo.objects.get(id=codigo_id)
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
    datos= {'valores':temps, 'fechas':fechas, 'codigos':agregados,'lat':lat,'long':long }
    print(datos)         
    return render(request,'mapa.html', {'datos':datos}  )
    