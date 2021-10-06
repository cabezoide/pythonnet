#!/usr/bin/env python

import dpkt
import socket
import pandas as pd
import argparse
import sys


'''Argumentos'''
# iniciales
archivo_input= None
archivo_output = None

parser = argparse.ArgumentParser(
    prog='./conversaciones_pcap_a_csv.py OPTIONS', description='Script que toma como entrada un pcap, extrae sus conversaciones tcp/udp, exporta a csv')
parser.add_argument('-i', '--input-file', action="store", dest="archivo_input",
                    type=str, help="archivo captura de entrada. ej: test.pcap")
parser.add_argument('-o', '--output-file', action="store", dest="archivo_output", 
                    type=str, help="archivo csv de salida. ej: salida.csv")

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)
args = parser.parse_args()

if args.archivo_input:
    archivo_input = args.archivo_input
if args.archivo_output:
    archivo_output = args.archivo_output

# Abrir archivo pcap

f = open(archivo_input, 'rb')
pcap = dpkt.pcap.Reader(f)

# Usamos un arreglo como base de datos temporal

db = []

# Abrimos y procesamos el archivo pcap
# Por cada paquete en el archivo pcap
for ts, buf in pcap:
   eth = dpkt.ethernet.Ethernet(buf)
   ip = eth.data
   try:
       if ip.p==dpkt.ip.IP_PROTO_TCP: # Si el paquete es TCP
           try:
               tcp = ip.data
               src_ip = socket.inet_ntoa(ip.src) # Obtiene ip origen 
               dst_ip = socket.inet_ntoa(ip.dst) # Obtiene ip destino
               src_port = tcp.sport # Obtiene puerto origen
               dst_port = tcp.dport # Obtiene puerto destino
               packet_type = 'tcp' # El paquete es de tipo tcp lo etiquetamos como tal
           except:
               continue
       elif ip.p==dpkt.ip.IP_PROTO_UDP: # si el paquete es UDP
           try:
               udp = ip.data
               src_ip = socket.inet_ntoa(ip.src) # Obtiene ip origen
               dst_ip = socket.inet_ntoa(ip.dst) # Obtiene ip destino
               src_port = udp.sport # Obtiene puertp origen
               dst_port = udp.dport # Obtiene puerto destino
               packet_type = 'udp' # El paquete es de tipo udp lo etiquetamos como tal
           except:
               continue
   except:
       continue
       
   # Guardamos los datos del paquete en el arreglo temporal
   db.append((src_ip,src_port,dst_ip,dst_port, packet_type))

f.close()

# Convertimos el arreglo temporal en un pandas dataframe

df = pd.DataFrame(db, columns = ['src_ip','src_port','dst_ip', 'dst_port', 'packet_type'])

# Usamos la funcion de convertir a csv

df.to_csv(archivo_output)

print(df)