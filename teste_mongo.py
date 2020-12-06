from pymongo import MongoClient

string_conn = 'mongodb://xxx:xxx@192.168.68.116:27017/admin'

client = MongoClient(string_conn)

print(client.list_database_names())

db = client.clotilde
collection_arduino = db.arduino

print(collection_arduino.delete_many({'temperatura': 10}))

cursor = collection_arduino.find({})

for doc in cursor:
    print(doc)

#data = {'temperatura': 10, 'umidade':40}

#print(collection_arduino.insert_one(data))
