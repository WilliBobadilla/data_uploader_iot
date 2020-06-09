

#app.py

from flask import Flask, request , render_template #import main Flask class and request object
from random import randint
import json 
import csv 
app = Flask(__name__) #create the Flask app


@app.route('/')
def home():

    dato=[]
    for a in range(5):
        dato.append(str(randint(10,50)))
    
    msg=json.dumps({'dato':dato})
    print(msg)
    return render_template('index.html',msg=msg)





@app.route('/post-data',methods = ['POST','GET'])
def formexample():
    if request.method == 'POST':
        nombre = request.form["nombre"]
        apellido=request.form["apellido"]
        print("este es el post", nombre,apellido )
        with open("datos_nuevos.csv","a") as data_temp_csv:
            # agregar lo de leer si es que ya esta escrito open
            # la cabecera, la posible solucion es de abrir el 
            #archivo y verificar si es que ya esta o no 
            nombrefilas= ["Nombre","Apellido"]  # nombre de los campos
            writer=csv.DictWriter(data_temp_csv,fieldnames=nombrefilas) # creamos un objeto writer sobre el archivo, y le especificamos el nombre de kis campos
            #writer.writeheader() #escribimos la primera

            writer.writerow({'Nombre' : '\n' + nombre, 'Apellido':apellido})

        return '<h2> Recibido!  </h2>'
    else:
        return "no recibi nada"