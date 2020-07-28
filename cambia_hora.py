#!/usr/bin/python

# importamos libreria pexpect python expect
import pexpect

# importamos liberia system para abrir el archivo de hosts
import sys

# importamos librerias os y logging para trabajar con logging al terminal
import os
import logging

# importamos libreria argparse para parsear argumentos
import argparse

logging.basicConfig(level=logging.DEBUG)

'''Argumentos'''
# iniciales
archivo = None
user = None
password = None

parser = argparse.ArgumentParser(
    prog='./cambia_hora.py OPTIONS', description='Script que cambia hora de equipos cisco')
parser.add_argument('-u', '--user', action="store", dest="user",
                    type=str, help="usuario equipo. ej: marcelo")
parser.add_argument('-p', '--password', action="store",
                    dest="password", type=str, help="password. ej: leta123456")
parser.add_argument('-a', '--archivo', action="store", dest="archivo",
                    type=str, help="archivo con hosts, una IP por linea")

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)
args = parser.parse_args()

if args.archivo:
    archivo = args.archivo
if args.user:
    user = args.user
if args.password:
    password = args.password

"""Variables"""
hosts = []

"""Funciones"""

def lee_archivo():
    global hosts
    # abre archivo hosts
    f = open(archivo, 'r')
    # por cada linea en el archivo agrega una entrada al arreglo hosts
    for line in f:
        hosts.append(line)

def worker():
    """Realiza el trabajo"""
    global hosts
    for equipo in hosts:
        equipo = equipo.replace('\n', '')
        c = pexpect.spawn('telnet ' + str(equipo))
        #fout = open(str(equipo) + '.log', "w")
        c.logfile = sys.stdout.buffer
        print("Trabajando...en %s" % equipo)

        # Ingresa al equipo
        c.expect(['Username: '])
        c.send(str(user) + '\r')
        c.expect(['Password: '])
        c.send(str(password) + '\r')
        c.expect('#')
        # Intenta enviar comando
        try:
            # Envia comando para cambiar la hora
            cmd = 'clock set 14:12:00 04 feb 2020\r'
            c.sendline(cmd)
            c.expect('#')
            # Envia comando end
            cmd = 'end\r'
            c.sendline(cmd)
            c.expect('#')
            # Envia comando logout
            cmd = 'logout\r'
            c.sendline(cmd)
        # Si falla en enviar comando indica error
        except:
            print("No pude configurar en equipo %s" % equipo)
            continue

"""Hilo principal"""

def main():
    lee_archivo()
    worker()

if __name__ == '__main__':
    main()
