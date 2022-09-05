import json
import requests
import urllib.parse
import pandas as pd
import sys
from urllib.request import Request, urlopen

# DATA CRAWLERS

def data_crawler_virus_total(ip):
    df_analysis_normalized = pd.DataFrame()
    try:
        # VIRUS TOTAL
        URL = 'https://www.virustotal.com/api/v3/ip_addresses/%s' % ip
        req = Request(URL)
        req.add_header('x-apikey', '[inserta tu api key virus total aqui]')
        content = urlopen(req).read()
        d = json.loads(content)
        df_analysis_normalized = pd.json_normalize(d['data'])
    except:
        pass 
    return df_analysis_normalized

def data_crawler_shodan(ip):
    df_analysis_normalized = pd.DataFrame()
    try:
        # SHODAN
        URL = 'https://api.shodan.io/shodan/host/%s?key=[inserta tu api key shodan aqui]' % ip
        req = Request(URL)
        content = urlopen(req).read()
        d = json.loads(content)
        df_analysis_normalized = pd.json_normalize(d['data'])
    except:
        pass
    return df_analysis_normalized

def data_crawler_greynoise(ip):
    df_analysis_normalized = pd.DataFrame()
    try:
        # GREYNOISE
        URL = 'https://api.greynoise.io/v3/community/%s' % ip
        req = Request(URL)
        content = urlopen(req).read()
        d = json.loads(content)
        df_analysis_normalized = pd.json_normalize(d)
    except:
        pass
    return df_analysis_normalized

def data_crawler_abuseipdb(ip):
    df_analysis_normalized = pd.DataFrame()
    try:
        # ABUSE IP DB
        url = 'https://api.abuseipdb.com/api/v2/check'
        querystring = {
        'ipAddress': str(ip),
        'maxAgeInDays': '90'}
        headers = {
        'Accept': 'application/json',
        'Key': '[inserta tu api key abuse ip db aqui]'}
        response = requests.request(method='GET', url=url, headers=headers, params=querystring)
        d = json.loads(response.text)
        df_analysis_normalized = pd.json_normalize(d['data'])
    except:
        pass
    return df_analysis_normalized

# IP como argumento del CLI

ip = sys.argv[1]
    
# Llamar a los crawler, retornan dataframes

df_greynoise = data_crawler_greynoise(str(ip))
df_abuseipdb = data_crawler_abuseipdb(str(ip))
df_virus_total = data_crawler_virus_total(str(ip))
df_shodan = data_crawler_shodan(str(ip))

# Escribir los dataframe en hojas de un archivo excel como informe

writer = pd.ExcelWriter('informe_ip_%s.xlsx' %ip, engine='xlsxwriter')

df_greynoise.to_excel(writer, sheet_name='greynoise')
df_abuseipdb.to_excel(writer, sheet_name='abuseipdb')
df_virus_total.to_excel(writer, sheet_name='virustotal')
df_shodan.to_excel(writer, sheet_name='shodan')

writer.save()