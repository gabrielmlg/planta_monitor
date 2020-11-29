# importando as bibliotecas
from kafka import KafkaConsumer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import json
from IPython.display import clear_output
import ast

#configuração do kafka
brokers = ['localhost:9092']
topic = 'topico-clotilde'
consumer = KafkaConsumer(topic, group_id = 'group1', bootstrap_servers = brokers)

print('Consumer ...')
print(consumer.resume())

#geração da nuvem de palavras em tempo real
frases = ''
for messagem in consumer:
    texto = json.loads(messagem.value)
    print(texto)
    texto = ast.literal_eval(texto)
    print(texto['umidade'])

print('sem mensagem ... fim!')

    #clear_output()
    #wordcloud = WordCloud(max_font_size=100, width = 1520, height = 535).generate(frases)
    #plt.figure(figsize=(16,9))
    #plt.imshow(wordcloud)
    #plt.axis("off")
    #plt.show()