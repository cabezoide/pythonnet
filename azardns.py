# importa libreria subprocess para poder ejecutar comandos en linux

import subprocess

# importa libreria random para crear el puntero random que apunte a un indice del array de dns
import random

# importa la libreria time para hacer que le programa espere X segundos antes de cambiar el DNS

import time

# se crea arreglo de DNS que contiene DNS publicos

dns = ['1.1.1.1', 
        '8.8.8.8',
        '8.8.4.4',
        '9.9.9.9',
        '149.112.112.112',
        '1.0.0.1',
        '185.228.168.9',
        '185.228.169.9',
        '64.6.64.6',
        '64.6.65.6',
        '208.67.222.222',
        '198.101.242.72',
        '23.253.163.53',
        '208.67.222.222',
        '208.67.220.220']

# se define funcion random_dns que cambiar los DNS, toma como entrada el intervalo de cambio de dns

def random_dns(change_time):

    # mientras el programa este corriendo
    while True:
    # la variable random dns toma el valor de un elemento dns de un indice al azar del arreglo dns
        random_dns = dns[random.randint(0,len(dns)-1)]
        # ejecuta el comando que cambiar el archivo /etc/resolv.conf, que es el archivo dns de linux
        cmd = 'echo "nameserver %s" > /etc/resolv.conf' % random_dns
        out = subprocess.Popen(cmd,
           shell='True',        
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT)
        stdout,stderr = out.communicate()
    # espera mientras termina el intervalo especificado
    time.sleep(change_time)


# llamamos a la funcion especificando un intervalo de 10 segundos

random_dns(10)
