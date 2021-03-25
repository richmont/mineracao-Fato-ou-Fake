from db.sqlite import Banco, conectar
from preprocess import Token
from post import Post
from conf.settings import SQLITE_POSTS_FILENAME


cursor = conectar(SQLITE_POSTS_FILENAME)
banco = Banco(cursor)
lista_posts = banco.consulta_post_titulo("É #FAKE que", limite=30)
stopwords_customizadas = {'É', 'FATO', "FAKE", "mostre", 'após', 'logo'}
lista_tokens = []
for x in lista_posts:
    token = Token(id=x._id, texto=x.titulo, stopwords_customizadas=stopwords_customizadas)
    lista_tokens.append(token)
    print("Titulo original: ", x.titulo)
    #print("id do post", x._id)
    print("Tokenizado: ", token.tokens_filtrados)
