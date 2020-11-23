import sys
from serial import Serial
import pandas as pd
import os
from datetime import datetime


PARAM_CARACTER='t'
PARAM_ASCII=str(chr(116))

s = Serial(port='/dev/cu.usbmodem146101', baudrate=9601, bytesize=8, parity='N', stopbits=1, timeout=None, xonxoff=False, rtscts=False, dsrdtr=False)

data = []
umidade = []
temperatura = []

try: 
   df = pd.read_csv('Documents/dev/planta_monitor/app/dataset/clotilde_v1.csv')
   print('Historico')
except:
    df = pd.DataFrame()

print(os.getcwd())

def main():
    #this will store the line
    seq = []
    count = 1

    try:
        while True:
            for c in s.read():
                seq.append(chr(c)) #convert from ANSII
                joined_seq = ''.join(str(v) for v in seq) #Make a string from array

                if chr(c) == '\n':
                    doc_clotilde = eval(joined_seq)
                    # print(doc_clotilde['umidade_solo'])
                    data.append(datetime.now())
                    umidade.append(doc_clotilde['umidade_solo'])
                    temperatura.append(doc_clotilde['umidade_solo'])

                    df.to_csv('Documents/dev/planta_monitor/app/dataset/clotilde_v1.csv', index=False)

                    print(df.tail())
                    #print("Line " + str(count) + ': ' + joined_seq)
                    seq = []
                    count += 1
                    break


        ser.close()
    except: 
        print('ERROR!!!!')


main()

