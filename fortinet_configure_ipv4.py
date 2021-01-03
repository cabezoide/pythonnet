#!/usr/bin/python
import pyfortiapi
import json
import pexpect
import os
import logging
import sys
import argparse
import csv

logging.basicConfig(level=logging.DEBUG)

'''Variables'''
#initial variables, please replace accordingly

IP_FW = "FW_IP_ADDRESS_HERE"
PORT_FW = "FW_HTTPS_PORT_HERE"
VDOM_FW = "VDOM_NAME_HERE"

# initial variables

address_ipv4 = []
bd_payload= []

'''Argumentos'''
# iniciales

file = None
USER_FW = None
PASSWORD_FW = None

parser = argparse.ArgumentParser(
    prog='./fortinet_configure_ipv4.py OPTIONS', description='Script that configures a list of IPv4 /32 on FW')
parser.add_argument('-f', '--file', action="store", dest="file",
                    type=str, help=".csv file with IPv4 list one per line (/32)")
parser.add_argument('-u', '--user', action="store", dest="user",
                    type=str, help="FW user. ej: fistolech")
parser.add_argument('-p', '--password', action="store",
                    dest="password", type=str, help="password. ej: lethal123456")

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)
args = parser.parse_args()

if args.file:
    file = args.file
if args.user:
    USER_FW = args.user
if args.password:
    PASSWORD_FW = args.password

def lee_file():
    """Read file with IPv4 list"""
    global address_ipv4
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            print(row)
            address_ipv4.append(row)
    return address_ipv4

def genera_base_datos():
    """Generate payload database one for each ipv4"""
    #payload = "{'name': 'Test', 'type': 'subnet', 'subnet': '192.168.0.0 255.255.255.0'}
    for address in address_ipv4:
        address = str(address[0])
        payload = str("{'name': '%s/32', 'type': 'subnet', 'subnet': '%s 255.255.255.255'}" % (address, address))
        bd_payload.append(payload)
    return bd_payload

def worker():
    """Generate connection and configures ipv4"""
    # connection data
    device = pyfortiapi.FortiGate(ipaddr=IP_FW, port=PORT_FW,
    username=USER_FW,
    password=PASSWORD_FW,
    vdom=VDOM_FW)
    # for each payload on database
    for payload in bd_payload:
        json_acceptable_string = payload.replace("'", "\"")
        d = json.loads(json_acceptable_string)
        subnet_name = (str(d['name']))
        # create fw address
        device.create_firewall_address(subnet_name, payload)
        print(subnet_name)

"""Main thread"""

def main():
    print(lee_file())
    print(genera_base_datos())
    worker()


if __name__ == '__main__':
    main()
