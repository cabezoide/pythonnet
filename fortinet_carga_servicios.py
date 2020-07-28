import pyfortiapi
import json


# Datos de conexion

device = pyfortiapi.FortiGate(ipaddr="IP", port = "PORT",
username="INSERTAR_USERNAME_ACA",
password="INSERTAR_PASSWORD_ACA",
vdom= "VDOM1")

# Base de datos de payload una por cada servicios

bd_payload = [
"{'name': 'TCP 5002', 'tcp-portrange': '5002'}",
"{'name': 'TCP 5003', 'tcp-portrange': '5003'}",
"{'name': 'TCP 13306', 'tcp-portrange': '13306'}",
"{'name': 'TCP 13303', 'tcp-portrange': '13303'}",
"{'name': 'TCP 61616', 'tcp-portrange': '61616'}",
"{'name': 'TCP 61617', 'tcp-portrange': '61617'}",
"{'name': 'TCP 9302', 'tcp-portrange': '9302'}",
"{'name': 'TCP 9304', 'tcp-portrange': '9304'}",
"{'name': 'TCP 9362', 'tcp-portrange': '9362'}",
"{'name': 'TCP 9367', 'tcp-portrange': '9367'}",
"{'name': 'TCP 9364', 'tcp-portrange': '9364'}",
"{'name': 'TCP 9320', 'tcp-portrange': '9320'}",
"{'name': 'TCP 9322', 'tcp-portrange': '9322'}",
"{'name': 'TCP 9323', 'tcp-portrange': '9323'}",
"{'name': 'TCP 9312', 'tcp-portrange': '9312'}",
"{'name': 'TCP 9314', 'tcp-portrange': '9314'}"
]

# Para cada payload en base de datos

for payload in bd_payload:
    # Convertir el string a un string aceptable por json con doble comillas
    json_acceptable_string = payload.replace("'", "\"")
    # Cargar cada string como un string json
    d = json.loads(json_acceptable_string)
    # Extraer el nombre del servicio y convertirlo a string
    service_name = (str(d['name']))
    # Crear el servicio en el firewall
    device.create_firewall_service(service_name, payload)
    print(service_name)




