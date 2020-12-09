import json
import sys
from serial import Serial
import pandas as pd
import os
from datetime import datetime
from time import sleep
from json import dumps
from pymongo import MongoClient


serial_port_raspi = '/dev/ttyACM0' 
url_raspi = '/home/pi/dev/planta_monitor/app/dataset/clotilde_v1.csv'
serial_port_mac = '/dev/cu.usbmodem146101'
url_mac = '/Users/gabriel/Documents/dev/planta_monitor/app/dataset/clotilde_v1.csv'
serial_port_macair = '/dev/cu.usbmodem14201'
url_macair = '/Users/gabriel.lopes/Documents/pessoal/dev/planta_monitor/app/dataset/clotilde_v1.csv'
string_conn_raspi = 'mongodb://admin:v73jMSPw9EQI@192.168.68.116:27017/admin'
string_conn_macair = 'mongodb://root:example@localhost:27017/admin'

serial_port = serial_port_macair
data_url =  url_macair
string_conn = string_conn_macair

s = Serial(port=serial_port, baudrate=9601, bytesize=8, parity='N', stopbits=1, timeout=None, xonxoff=False, rtscts=False, dsrdtr=False)


data = []
umidade = []
umidade2 = []
temperatura = []

print(os.getcwd())

def main():
    #this will store the line
    seq = []
    count = 1
    
    client = MongoClient(string_conn)
    db = client.clotilde
    collection_arduino = db.arduino

    try: 
        df = pd.read_csv(data_url)
        print('Carregou ...')
    except:
        df = pd.DataFrame()

    while True:
        for c in s.read():
            seq.append(chr(c)) #convert from ANSII
            joined_seq = ''.join(str(v) for v in seq) #Make a string from array

            # {'umidade_solo': 1.39, 'per_solo': 25.00, 'umidade_solo2': 1.02, 'per_solo2': 67.00, 'temperatura ambiente': 26.70}
            if chr(c) == '\n':
                doc_clotilde = eval(joined_seq)
                #print(doc_clotilde)
                data.append(datetime.now())
                umidade.append(doc_clotilde['per_solo'])
                umidade2.append(doc_clotilde['per_solo2'])
                temperatura.append(doc_clotilde['temperatura ambiente'])

                dados = {
                    'data': str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')), 
                    'vol_umidade1': doc_clotilde['umidade_solo'], 
                    'umidade': doc_clotilde['per_solo'], 
                    'vol_umidade2': doc_clotilde['umidade_solo2'], 
                    'umidade2': doc_clotilde['per_solo2'], 
                    'temperatura': doc_clotilde['temperatura ambiente']
                }

                collection_arduino.insert_one(dados)
                sleep(1)

                print(str(dados))

                #df = df.append(df2, ignore_index=True)
                #df['data'] = pd.to_datetime(df['data'])
                #df.sort_values('data', inplace=True)

                #df2.to_csv(data_url, index=False)

                #print(df2.tail())
                #print("Line " + str(count) + ': ' + joined_seq)
                seq = []
                count += 1
                break


main()

