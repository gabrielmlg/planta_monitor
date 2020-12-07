from pymongo import MongoClient
import pandas as pd
from datetime import datetime

string_conn_raspi = 'mongodb://admin:v73jMSPw9EQI@192.168.68.116:27017/admin'
string_conn_mac = 'mongodb://root:example@localhost:27017/admin'

string_conn =string_conn_mac

client = MongoClient(string_conn)

print(client.list_database_names())

db = client.clotilde
collection_arduino = db.arduino

print(collection_arduino.delete_many({}))

#cursor = collection_arduino.find({})

#print(pd.DataFrame(list(cursor)))

#print(datetime.now())

#data = {'data': datetime.now(), 'temperatura': 12, 'umidade':60}
#print(collection_arduino.insert_one(data))
