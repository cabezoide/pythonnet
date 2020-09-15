#!/usr/bin/python

# importamos libreria pexpect python expect
import pexpect
# importamos librerias os y logging para trabajar con logging al terminal
import os
import logging
# import sys para argumentos
import sys
# importamos libreria argparse para parsear argumentos
import argparse
# importamos libreria csv para leer archivo csv
import csv

logging.basicConfig(level=logging.DEBUG)

'''Argumentos'''
# iniciales
archivo = None
user = None
password = None


parser = argparse.ArgumentParser(
    prog='./configura_cpe.py OPTIONS', description='Script que configura router CPE')
parser.add_argument('-a', '--archivo', action="store", dest="archivo",
                    type=str, help="archivo .csv con hosts e interfaces WAN, una IP;INTERFAZ_WAN por linea")
parser.add_argument('-u', '--user', action="store", dest="user",
                    type=str, help="usuario equipo. ej: fistolech")
parser.add_argument('-p', '--password', action="store",
                    dest="password", type=str, help="password. ej: leta123456")

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
    with open(archivo, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            print(row)
            hosts.append(row)


"""Funciones"""

def worker():
    """Realiza el trabajo"""
    global hosts
    equipo = None
    interfaz_wan = None
    for host in hosts:
        equipo = host[0]
        interfaz_wan = host[1]
        equipo = equipo.replace('\n', '')
        ssh_newkey = 'Are you sure you want to continue connecting'
        c = pexpect.spawn('ssh ' + str(user) + '@' + str(equipo))
        #fout = open(str(equipo) + '.log', "w")
        c.logfile = sys.stdout.buffer
        print("Trabajando...en %s" % equipo)
        # Ingresa al equipo
        try:
            ret = c.expect([pexpect.TIMEOUT,ssh_newkey, 'Password: '], timeout=3)
            # CASO EQUIPO NO RESPONDE
            if ret == 0:
                print('[-] Error Conectandose a %s' % equipo)
                continue
            # CASO SERVIDOR NO TIENE LLAVE SSH DEL EQUIPO
            elif ret == 1:
                c.sendline('yes')
                c.expect(['Password: '])
                c.send(str(password) + '\r')
                c.expect('#')
            # CASO SERVIDOR TIENE LLAVE SSH
            else:
                c.send(str(password) + '\r')
                c.expect('#')
            # CONFIG VRF
            cmd = 'configure terminal\r'
            c.sendline(cmd)
            c.expect('#')
            cmd = 'ip vrf VRF_MGMT\r'
            c.sendline(cmd)
            c.expect('#')
            cmd = 'rd 77:77\r'
            c.sendline(cmd)
            c.expect('#')
            cmd = 'route-target export 77:77\r'
            c.sendline(cmd)
            c.expect('#')
            cmd = 'route-target import 77:77\r'
            c.sendline(cmd)
            c.expect('#')
            cmd = 'end\r'
            c.sendline(cmd)
            c.expect('#')
            # CONFIG VRF INTERFACE WAN
            cmd = 'configure terminal\r'
            c.sendline(cmd)
            c.expect('#')
            cmd = 'interface %s.\r' % interfaz_wan
            c.sendline(cmd)
            c.expect('#')
            cmd = 'description WAN\r'
            c.sendline(cmd)
            c.expect('#')
            cmd = 'encapsulation dot1Q 3000\r'
            c.sendline(cmd)
            c.expect('#')
            cmd = 'ip vrf forwarding VRF_MGMT\r'
            c.sendline(cmd)
            c.expect('#')
            cmd = 'ip address dhcp\r'
            c.sendline(cmd)
            c.expect('#')
            cmd = '!\r'
            c.sendline(cmd)
            c.expect('#')
            # CONFIG VRF DEFAULT ROUTE
            cmd = 'ip route vrf VRF_MGMT 0.0.0.0 0.0.0.0 dhcp\r'
            c.sendline(cmd)
            c.expect('#')
            cmd = 'end\r'
            c.sendline(cmd)
            c.expect('#')
            cmd = 'wr\r'
            c.sendline(cmd)
            c.expect('#')
            cmd = 'logout\r'
            c.sendline(cmd)
            # Si falla en enviar comando indica error
            print("EXITO: Termine de configurar en equipo %s" % equipo)
        except:
            print("FALLA: No pude configurar en equipo %s" % equipo)
            continue

"""Hilo principal"""

def main():
    lee_archivo()
    worker()


if __name__ == '__main__':
    main()


