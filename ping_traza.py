#!/usr/bin/python

# importamos libreria icmplib para realizar ping y trazas

from icmplib import ping, traceroute, Host, Hop

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
modo = None

parser = argparse.ArgumentParser(
    prog='./ping_traza.py OPTIONS', description='Script que realiza ping y trazas icmp a partir de una lista de archivos')

parser.add_argument('-a', '--archivo', action="store", dest="archivo",
                    type=str, help="archivo con hosts, una IP por linea")
parser.add_argument('-m', '--modo', action="store", dest="modo",
                    type=str, help="modo, puede ser ping o traceroute")


if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)
args = parser.parse_args()

if args.archivo:
    archivo = args.archivo
if args.modo:
    modo = args.modo

"""Variables"""
equipos = []

"""Funciones"""

def lee_archivo():
    global equipos
    # abre archivo con hosts
    f = open(archivo, 'r')
    # por cada linea en el archivo agrega una entrada al arreglo hosts
    for line in f:
        equipo = line.strip('\n')
        equipos.append(equipo)

def worker(modo):
    """Realiza el trabajo"""
    global equipos
    for equipo in equipos:
        if modo == 'ping':
            host = ping(equipo, count=4, interval=1, timeout=2)
            if host.is_alive:
                print(f'Host:{host.address} RTT_min:{host.min_rtt} RTT_prom:{host.avg_rtt} RTT_max:{host.max_rtt} P_enviados:{host.packets_sent} P_recibidos:{host.packets_received} P_perdidos:{host.packet_loss}')
            else:
                print(f'Host:{host.address} no responde!')

        if modo == 'traceroute':
            hops = traceroute(equipo, count=3, interval=0.05, timeout=1, max_hops=30, fast_mode=True)
            print('_'*20)
            print(f'Host:{equipo}') 
            print('Distancia (ttl)  Address RTT_prom')
            last_distance = 0
            for hop in hops:
                if last_distance + 1 != hop.distance:
                    print(f'* * * * * *')
                print(f'{hop.distance}  {hop.address}   {hop.avg_rtt} ms')
                last_distance = hop.distance
            print('Traza completa')


"""Hilo principal"""
def main():
    lee_archivo()
    worker(modo)

if __name__ == '__main__':
    main()
