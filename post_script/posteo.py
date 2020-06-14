import requests 
from random import random
import csv 
from datetime import datetime
from time import sleep


#url = 'https://data-iot-collect.herokuapp.com/data'
url= 'http://127.0.0.1:8000/data'

with open("datos_nuevos.csv","a") as data_temp_csv:
    nombrefilas= ["token","temp","fecha","lat","long","codigo"]  # nombre de los campos
    writer=csv.DictWriter(data_temp_csv,fieldnames=nombrefilas) # creamos un objeto writer sobre el archivo, y le especificamos el nombre de kis campos
    #writer.writeheader() #escribimos la primera
    while True: 
        try:
            temp=random()*10 
            myobj = { 
                'token':'aBx4Z60o',
                'temp': str(temp),  
                'fecha': str(datetime.now()),
                'lat': -25.509304 , 
                'long':  -54.653337,
                'codigo': 'CDE1'
                    }
            writer.writerow(myobj) 
            x = requests.post(url, data = myobj)
            print(x.text) 
            sleep(2)  # cada 20 seg posteamos datos
        except KeyboardInterrupt: #ctrl + c     
            print("finalizado")
            break

print("programa terminado")