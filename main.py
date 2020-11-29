import json
import sys
from serial import Serial
import pandas as pd
import os
from datetime import datetime
from time import sleep
from json import dumps
from kafka import KafkaProducer


PARAM_CARACTER='t'
PARAM_ASCII=str(chr(116))

serial_port_raspi = '/dev/ttyACM0' 
url_raspi = '/home/gabriel/dev/planta_monitor/app/dataset/clotilde_v1.csv'
serial_port_mac = '/dev/cu.usbmodem146101'
url_mac = '/Users/gabriel/Documents/dev/planta_monitor/app/dataset/clotilde_v1.csv'

serial_port = serial_port_mac
data_url =  url_mac

s = Serial(port=serial_port, baudrate=9601, bytesize=8, parity='N', stopbits=1, timeout=None, xonxoff=False, rtscts=False, dsrdtr=False)

# configuração do kafka
broker = 'localhost:9092'
topico = 'topico-clotilde'
producer = KafkaProducer(bootstrap_servers=[broker],
                         value_serializer=lambda x:
                         dumps(x).encode('utf-8'))


data = []
umidade = []
temperatura = []

print(os.getcwd())

def main():
    #this will store the line
    seq = []
    count = 1

    try: 
        df = pd.read_csv(data_url)
        print('Carregou ...')
    except:
        df = pd.DataFrame()

    while True:
        for c in s.read():
            seq.append(chr(c)) #convert from ANSII
            joined_seq = ''.join(str(v) for v in seq) #Make a string from array

            if chr(c) == '\n':
                doc_clotilde = eval(joined_seq)
                #print(doc_clotilde)
                data.append(datetime.now())
                umidade.append(doc_clotilde['umidade_solo'])
                temperatura.append(doc_clotilde['temperatura ambiente'])

                dados = {
                    'data': str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')), 
                    'umidade': doc_clotilde['umidade_solo'], 
                    'temperatura': doc_clotilde['temperatura ambiente']
                }

                producer.send(topico, value=str(dados))
                sleep(1)

                print(str(dados))

                df2 = pd.DataFrame({
                    'data': data, 
                    'umidade': umidade, 
                    'temperatura': temperatura
                })

                #df = df.append(df2, ignore_index=True)
                #df['data'] = pd.to_datetime(df['data'])
                #df.sort_values('data', inplace=True)

                df2.to_csv(data_url, index=False)

                print(df2.tail())
                #print("Line " + str(count) + ': ' + joined_seq)
                seq = []
                count += 1
                break


    ser.close()


main()

