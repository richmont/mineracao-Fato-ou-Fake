from pymongo import MongoClient, errors
from conf.settings import MONGO_URL
from stopwords import limpeza_stopwords
local = MONGO_URL
try:
    cliente = MongoClient(local)
except errors.InvalidURI:
    raise errors.InvalidURI("Verifique o endereço de acesso ao banco")
banco = cliente.fato_ou_fake
posts = banco.posts


data = "2021"
query = {'data_publicacao': {'$regex': data}, "titulo": {'$regex': "É #FAKE que"}}
limite = 5
resultado = posts.find(query).limit(limite)

for x in resultado:
    print()
    print(x['titulo'])
    limpeza_stopwords(x['titulo'].strip('É #FAKE que '))
    
