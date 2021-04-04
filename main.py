from db.sqlite import TabelaPosts, conectar
from preprocess import Token, spacy
from post import Post
from conf.settings import SQLITE_POSTS_FILENAME
import time

start_time = time.time()
print("ainda não fiz literalmente nada além de importar ", time.time() - start_time, "seconds")
cursor = conectar(SQLITE_POSTS_FILENAME)
tPosts = TabelaPosts(cursor)
lista_posts = tPosts.consulta_post_titulo("É #FAKE que", limite=100)
print("Tempo de consulta ao banco ", time.time() - start_time, "seconds")
# é preciso adicionar números na lista de stopwords
stopwords_customizadas = {'É', 'FATO', "FAKE", "mostre", 'após', 'logo', 'R'}
#stopwords_customizadas = None
lista_tokens = []
# carrega o idioma português no spacy apenas uma vez, não mais a cada token criado
nlp = spacy.load("pt_core_news_sm")
print("Carregando idioma português ", time.time() - start_time, "seconds")
for x in lista_posts:
    token = Token(id=x._id, nlp=nlp, texto=x.titulo, stopwords_customizadas=stopwords_customizadas)
    print("Tokenizando títulos ", time.time() - start_time, "seconds")
    lista_tokens.append(token)
    
    #print("Nomes próprios: ", token.nomes_proprios)
    print("Tokens lematizados", token.tokens_lematizados)
    #print("Título original: ", token.texto)

    
print(time.time() - start_time, "seconds")