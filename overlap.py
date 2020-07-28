# importamos libreria ipaddress para manipular IP

import ipaddress as ip

# importamos libreria itertools para realizar combinaciones

import itertools as it

# creamos un arreglo que contenga todas las direcciones IPv4 (segmentos de red) que queremos evaluar

address = [
'10.10.11.0/255.255.255.0',
'10.12.0.0/255.252.0.0',
'10.12.0.0/255.255.255.0',
'10.12.2.0/255.255.255.0',
'192.168.0.0/21',
'192.168.7.0/24',
'172.16.24.0/255.255.255.248',
'172.16.24.0/255.255.255.0',
'10.0.0.1/255.255.255.255',
'192.168.5.234/32'
]

# primero realizamos todas las combinaciones posibles entre los segmentos de red con it.combinations(address,2)
# luego convertimos estos elementos en una lista con list()
# finalmente obtenemos los elementos unicos de esa lista con set
# esto nos entrega una lista con todas las combinaciones posibles en formato (red1,red2)

combinations = set(list(it.combinations(address, 2)))

# para cada elemento en la lista de combinaciones
 
for element in combinations:
    # network uno (n1) es igual al primer componente de cada elemento de la lista, y lo convertimos en un objeto IPv4Network de libreria ip
    # network dos (n2) es igual al segundo componente de cada elemento de la lista,  y lo convertimos en un objeto IPv4Network de libreria ip
 
    n1 = ip.IPv4Network(element[0])
    n2 = ip.IPv4Network(element[1])

    # usamos la funcion overlaps de la libreria ip, que precisamente evalua si un segmento de red esta sobrepuesto a otro, si el segmento n1 esta sobrepuesto a n2, entonces n2 esta contenido dentro de n1

    if n1.overlaps(n2) == True:
        # creamos una cadena de texto que imprima el resultado
        string = f"Red {n2} contenida dentro de {n1}"
        # imprimimos el resultado
        print(string)
