import pandas as pd
import argparse
import sys
import ipaddress
#from ipaddress import ip_address

'''Argumentos'''
# iniciales
archivo_input= None
archivo_output = None

parser = argparse.ArgumentParser(
    prog='./encuentra_publicas.py OPTIONS', description='Script que toma como entrada un archivo excel con ipv4 y las clasifica en publicas o privadas')
parser.add_argument('-i', '--input-file', action="store", dest="archivo_input",
                    type=str, help="archivo excel de entrada con todas las ip. ej: ip.xlsx")
parser.add_argument('-o', '--output-file', action="store", dest="archivo_output", 
                    type=str, help="archivo excel de salida con las ip clasificadas. ej: salida.xlsx")

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)
args = parser.parse_args()

if args.archivo_input:
    archivo_input = args.archivo_input
if args.archivo_output:
    archivo_output = args.archivo_output


resultado = []
   
def IPAddress(IP: str) -> str:
    return "Private" if (ipaddress.ip_network(IP).is_private) else "Public"
    
def ClassifyIP():
    df = pd.read_excel(archivo_input, index_col=None, header=None)
    for ipv4 in df[0]:
        resultado.append((ipv4, IPAddress(ipv4)))
    df2 = pd.DataFrame(resultado)
    return df2
    
if __name__ == '__main__' : 
    clasificadas = ClassifyIP()
    clasificadas.to_excel(archivo_output)
    print(clasificadas)