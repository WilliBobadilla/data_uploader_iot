import requests 
from random import random


temp=random()

url = 'http://127.0.0.1:8000'
myobj = {'temp': str(temp)}

x = requests.post(url, data = myobj)

print(x.text) 
