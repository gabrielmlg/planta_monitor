import sys
import time
import serial
 
"""
VARIAVEIS GLOBAIS (NESTE EXEMPLO)
"""
 
def InfoComSerial():
    print('\nObtendo informacoes sobre a comunicacao serial\n')
    # Iniciando conexao serial
    comport = serial.Serial(port='/dev/cu.usbmodem146101', baudrate=9602)
    time.sleep(1.8) # Entre 1.5s a 2s
    print('\nStatus Porta: %s ' % (comport.isOpen()))
    print('Device conectado: %s ' % (comport.name))
    print('Dump da configuracao:\n %s ' % (comport))
    print('\n###############################################\n')
    # Fechando conexao serial
    comport.close()
 
""" main """
if __name__ == '__main__':
    InfoComSerial()