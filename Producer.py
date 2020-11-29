from datetime import datetime
from time import sleep
from json import dumps
from kafka import KafkaProducer


# configuração do kafka
broker = 'localhost:9092'
topico = 'topico-clotilde'
producer = KafkaProducer(bootstrap_servers=[broker],
                         value_serializer=lambda x:
                         dumps(x).encode('utf-8'))


# colhendo os dados conforme texto desejado
for msg in ['Msg 1', 'Msg 2', 'Msg 3', 'Msg 4', 'Msg 1', 'Msg 1', 'Msg 2']:
  data_e_hora_completa = datetime.now()
  data_string = data_e_hora_completa.strftime('%Y-%m-%d %H:%M:%S')
  dados = {"Mensagem": msg, "horario": data_string}
  producer.send(topico, value=dados)
  sleep(1)