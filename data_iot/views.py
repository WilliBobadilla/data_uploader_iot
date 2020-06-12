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
        fecha_ahora= datetime.now()
        datos= Medida(temperatura=temp,fecha=fecha_ahora) 
        datos.save()
        #valores=Medida.objects.all() #hacemos un query 
        
        return HttpResponse("Recibido!" )  #render(request,'grafica.html',{'valores':temps, 'fechas':fechas })
    else:
        valores=Medida.objects.all() #hacemos un query 
        temps=[]
        fechas=[]
        for dato in valores: 
            temps.append(dato.temperatura)
            fechas.append(dato.fecha)  
        print(valores)
        
        return render(request,'grafica.html',{'valores':temps, 'fechas':fechas })
def update(request):
    valores=Medida.objects.all() #hacemos un query 
    temps=[]
    fechas=[]
    for dato in valores: 
        temps.append(dato.temperatura)
        fechas.append(dato.fecha)  
    print(valores)
    return JsonResponse({'valores':temps, 'fechas':fechas })
