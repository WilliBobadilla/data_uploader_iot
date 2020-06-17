"""
Autor: Williams Bobadilla
Fecha creacion: 14 junio 2020
Breve descripcion: Script donde mide la temperatura y lo postea a un servidor para guardar los datos 
Licencia: GNU General Public License v3.0

"""
# en este script debido a que no poseo fisicamente conmigo la RPi y el sensor,
# lo hago con random para emular las mediciones, de igual manera esta la funcion DHT11 
# que colecta la temperatura 
import requests 
from random import random
import csv 
from datetime import datetime
from time import sleep
from token_disp import token_str
""" Instrucciones para instalar la libreria 
    https://github.com/WilliBobadilla/bootcamp/blob/master/practica4_sensor.py
"""
try: # para usar con la rpi
    import Adafruit_DHT as dht   #renombramos la libreria com dht
    import RPi.GPIO as gpio  	 # libreria para utilizar los puertos de entrada y salida
    gpio.setmode(gpio.BCM) 			# modo BCM de la raspberry pi
except: 
    print("No tenes gpio!")

def DHT11_data():
	# leemos los datos del sensor, la humedad y la temperatura
	humi, temp = dht.read_retry(dht.DHT11, 23)#pin data conectado al GPIO23, si se usa el DHT22, usamos dht.DHT22
	return temp 

url= 'http://127.0.0.1:8000/data'

with open("datos_nuevos.csv","a") as data_temp_csv:
    nombrefilas= ["token","temp","fecha","lat","long","codigo"]  # nombre de los campos
    writer=csv.DictWriter(data_temp_csv,fieldnames=nombrefilas) # creamos un objeto writer sobre el archivo, y le especificamos el nombre de kis campos
    while True: 
        try:
            temp=random()*10 #aca deberia de llamarse a la funcion de la temperatura, DHT11_data()
            myobj = { 
                'token':token_str,
                'temp': str(temp),  
                'fecha': str(datetime.now()),
                'lat': -25.339450 , 
                'long':  -57.551921,
                'codigo': 'ASU1'
                    }
            writer.writerow(myobj) 
            x = requests.post(url, data = myobj)
            print(x.text) 
            sleep(2)  # cada 20 seg posteamos datos
        except KeyboardInterrupt: #ctrl + c     
            print("finalizado")
            break

print("programa terminado")