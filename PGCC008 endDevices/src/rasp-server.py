import socket
import pickle
import numpy as np
import json
import serial
import http.client
import urllib
import time

import time
from datetime import datetime

key = "PJB7IQ5N1GN98PET"

pin_dht11 = 3
pin_bmp180 = 6
pin_bmp280 = 5
pin_uv = 0
pin_chama = 1

t_send = 5

n_nodes = 4
node_list = [4208803281, 4208793911, 4208790561, 4208779354]

def writeSerial(data):
    connection.write(json.dumps(data).encode('ascii'))
    connection.flush()
    time.sleep(0.5)
    print(data)

# Recebe a lista de nós de entrada e atribui para cada um deles quais pinos serão e quais não deve ser ativados
def define_pinTable():
    '''
    Recebe a lista de ids dos nodes e os armazena, ao mesmo tempo que define a pinagem
    para cada nó. Definindo qual nó será ativado para cada node na rede mesh.
    '''
    def inicializar_pinos():
        '''
        Lista de pinos e respectivos sensores:
        1 - Temperatura
        3 - Humidade
        5 - Chama
        6 - UV
        14 - Pressão

        Os números representam o índice do pino na lista de pinos disponíveis
        '''

        # Definir como True todos os pinos que serão utilizados.
        tp = np.zeros([n_nodes, 18])
        tp = tp.tolist()

        # Node com temperatura, humidade, chama e uv
        tp[0][pin_dht11] = 1
        tp[0][pin_uv] = 1
        tp[0][pin_chama] = 1

        # Node com temperatura humidade e chama
        tp[1][pin_dht11] = 1
        tp[1][pin_chama] = 1

        # Node com temperatura humidade e uv
        tp[2][pin_bmp180] = 1
        tp[2][pin_uv] = 1

        # Node com temperatura, humidade, uv e pressão
        tp[3][pin_bmp280] = 1
        tp[3][pin_uv] = 1

        return tp

    id_nodes = [l for l in node_list]
    tp = inicializar_pinos()
    pin_table = {l:tp[ii][:] for ii, l in enumerate(id_nodes)}
    return pin_table


def send_setup_signal(data_in, connection):
    '''
    Envia mensage para o node conectado a porta serial avisando que ele é o nó master, além
    de enviar informações importantes de setup como pinagem e timestamp
    '''

    timestamp = int(time.time())

    pin_table = define_pinTable()

    data = {"node_master":data_in["id_node"],"send": True,"type":3,"t_send":t_send,"timestamp":timestamp}
    writeSerial(data)

    data = {"nodeDestiny":4208793911,"send": True,"type":2,"t_send":t_send,"uvPinDef":0,"bmp280PinDef":6,"pinDef": [1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0]}
    writeSerial(data)

    data = {"nodeDestiny":4208803281,"send": True,"type":2,"t_send":t_send,"dht11PinDef":3,"flamePinDef":15,"pinDef": [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0]}
    writeSerial(data)

    data = {"nodeDestiny":4208790561,"send": True,"type":2,"t_send":t_send,"uvPinDef":0,"dht11PinDef":3,"flamePinDef":15,"pinDef": [1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0]}
    writeSerial(data)

    data = {"nodeDestiny":4208779354,"send": True,"type":2,"t_send":t_send,"uvPinDef":0,"bmp180PinDef":6,"pinDef": [1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0]}
    writeSerial(data)

    return pin_table


def changeFrequency(id, period = t_send):
    data = {}
    data["send"] = True
    data["send_type"] = 2
    data["nodeDestiny"] = id
    data["t_send"] = period
    writeSerial(data)

    return

def verifica_anomalia(data):
    r = False
    chama = False
    if "flame" in data:
        chama = data["flame"]
        r = True
    
    if "uv" in data:    
        uv = data["uv"]
        r = True
        # Se ocorrer muito alta radiação devo considerar como alta radiação tambem ou serão excludentes?
        if uv is None or uv <= 5:
            database["alta_rad"].append(0)
            database["mto_alta_rad"].append(0)
        else: #nesse else o uv ja é maior que 5
            if uv > 7:
                database["mto_alta_rad"].append(1)
                database["alta_rad"].append(0)
            else:
                database["alta_rad"].append(1)
                database["mto_alta_rad"].append(0)


    if "temperature" in data:
        temperatura = data["temperature"]
        r = True
        if temperatura is None or temperatura <= 35:
            if chama:
                database["prin_incendio"].append(1)
            else: database["prin_incendio"].append(0)
            database["calor"].append(0)
            database["susp_incendio"].append(0)
            database["incendio"].append(0)
        else: # nesse else a temperatura ja é maior que 35
            if temperatura > 45: 
                if chama:
                    #print("Incêndio")
                    database["calor"].append(0)
                    database["susp_incendio"].append(0)
                    database["incendio"].append(1)
                    database["prin_incendio"].append(0)
                else:
                    #print("Suspeita de incêndio")
                    database["calor"].append(0)
                    database["susp_incendio"].append(1)
                    database["incendio"].append(0)
                    database["prin_incendio"].append(0)
            else:
                if chama:
                    database["prin_incendio"].append(1)
                else: 
                    database["prin_incendio"].append(0) 
                #print("onda de calor")
                database["calor"].append(1)
                database["susp_incendio"].append(0)
                database["incendio"].append(0)
         
    return r

def leitura_dados(data):
    if "device" in data:
        database["id"].append(data["device"])
    if "timestamp" in data:
        database["timestamp"].append(data["timestamp"])
    if "latitude" in data:
        database["latitude"].append(data["latitude"])
    if "longitude" in data:
        database["longitude"].append(data["longitude"])

    
    if(verifica_anomalia(data)):
        sensorData = []
        sensors = ['temperature', 'humidity', 'flame', 'uv', 'pressure']
        for s in sensors:
            if s in data.keys():
                database[s].append(data[s])
                sensorData.append(data[s])
            else:
                database[s].append(None)
                sensorData.append(0)
        enviaDadosThingSpeak(sensorData)
    return

def enviaDadosThingSpeak(sensorData):
        json = {'field1': sensorData[0],'field2': sensorData[1],'field3': sensorData[2],'field4': sensorData[3],'field5': sensorData[4], 'key':key }
        print(json)
        params = urllib.parse.urlencode(json)
        headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = http.client.HTTPConnection("api.thingspeak.com:80")
        try:
            conn.request("POST", "/update", params, headers)
            response = conn.getresponse()
            print(response.status, response.reason)
            data = response.read()
            conn.close()
        except Exception as e:
            print("connection ThingSpeak failed...................: ",e)


# Dicionário de dados contendo todas as informações recebidas pelo Rasp, desde os valores dos sensores (None caso não estejam presentes no pacote),
# até a indnicação de ocorrência ou não de anomalias como incendios, alta radiação, onda de calor, entre outros
database = {"id":[], "timestamp": [], "latitude":[], "longitude":[], "uv": [], "temperature": [], "flame": [], "humidity": [], "pressure": [],
        "datahora":[], "alta_rad":[], "mto_alta_rad":[], "calor":[], "susp_incendio":[], "prin_incendio":[], "incendio":[]}

connection = serial.Serial(port="/dev/ttyUSB0", baudrate=115200,bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
connection.reset_input_buffer()

while(True):
    if(connection.in_waiting > 0):
        msg = connection.readline()
        try:
            print(msg)
            data = json.loads(msg)
            if "id_node" in  data.keys():
                pin = send_setup_signal(data, connection)
            else:
                leitura_dados(data)
        except Exception as e:
            print("JSON String inválida.....................: ",e)
