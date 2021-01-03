#!/usr/bin/python
import argparse
import sys
import csv
from pysnmp import hlapi
from sysdescrparser import sysdescrparser
from openVulnQuery import query_client

'''Variables'''

snmp_community = []
address_ipv4 = []

# CISCO Openvuln API PRE-SET VARIABLES, CHANGE ACCORDINGLY

CLIENT_ID =  'YOUR_API_KEY_HERE'
CLIENT_SECRET = 'YOUR_API_CLIENT_SECRET_HERE'

'''Arguments'''

parser = argparse.ArgumentParser(
    prog='./snmp_cisco_vulns.py OPTIONS', description='Script that obtains Cisco Vulns given IPv4 host list and snmp community')
parser.add_argument('-f', '--file', action="store", dest="file",
                    type=str, help=".csv or plain-text file with IP or hostname list, one per line", required = True)
parser.add_argument('-c', '--community', action="store", dest="snmp_community",
        type=str, help="SNMP v1/v2c read-only community e.g: public", required = True)

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)
args = parser.parse_args()

if args.file:
    file = args.file
if args.snmp_community:
    snmp_community = hlapi.CommunityData(args.snmp_community)


'''SNMP Functions'''

def construct_object_types(list_of_oids):
    object_types = []
    for oid in list_of_oids:
        object_types.append(hlapi.ObjectType(hlapi.ObjectIdentity(oid)))
    return object_types

def get(target, oids, credentials, port=161, engine=hlapi.SnmpEngine(), context=hlapi.ContextData()):
    handler = hlapi.getCmd(
        engine,
        credentials,
        hlapi.UdpTransportTarget((target, port)),
        context,
        *construct_object_types(oids)
    )
    return fetch(handler, 1)[0]

def fetch(handler, count):
    result = []
    for i in range(count):
        try:
            error_indication, error_status, error_index, var_binds = next(handler)
            if not error_indication and not error_status:
                items = {}
                for var_bind in var_binds:
                    items[str(var_bind[0])] = cast(var_bind[1])
                result.append(items)
            else:
                raise RuntimeError('Got SNMP error: {0}'.format(error_indication))
        except StopIteration:
            break
    return result

def cast(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        try:
            return float(value)
        except (ValueError, TypeError):
            try:
                return str(value)
            except (ValueError, TypeError):
                pass
    return value

'''Functions'''

def read_file():
    """Read file with IPv4 list"""
    global address_ipv4
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            address_ipv4.append(row)
    return address_ipv4

def worker():
    """Obtains host version by SNMP, then queries Cisco Openvuln API"""
    global query_client
    query_client = query_client.OpenVulnQueryClient(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    for address in address_ipv4:
        address = str(address[0])
        result = get(address, ['1.3.6.1.2.1.1.1.0'], snmp_community)
        sysdescr = sysdescrparser(result['1.3.6.1.2.1.1.1.0'])

        print('HOST: %s; vendor: %s; model: %s; version: %s' % (address, sysdescr.vendor, sysdescr.model, sysdescr.version))

        if sysdescr.vendor == 'CISCO':
            try:
                advisories = query_client.get_by_ios('ios', sysdescr.version)
                for element in advisories:
                    print('title: %s; cves: %s; cvss_base_score: %s' % (element.advisory_title, element.cves, element.cvss_base_score))
            except:
                print('version not found')

"""Main thread"""

def main():
    read_file()
    worker()

if __name__ == '__main__':
    main()
