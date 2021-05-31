from db.sqlite import TabelaPosts, TabelaTokens, conectar
from preprocess import Token, spacy
from post import Post
from conf.settings import SQLITE_POSTS_FILENAME, SQLITE_TOKENS_FILENAME
import time

start_time = time.time()

#print("ainda não fiz literalmente nada além de importar ", time.time() - start_time, "seconds")
cursor_posts = conectar(SQLITE_POSTS_FILENAME)
cursor_tokens = conectar(SQLITE_TOKENS_FILENAME)
tPosts = TabelaPosts(cursor_posts)
tTokens = TabelaTokens(cursor_tokens)
tTokens.criar_tabela()
lista_posts_fake = tPosts.consulta_post_titulo("É #FAKE que", limite=200000)
#print("Tempo de consulta ao banco ", time.time() - start_time, "seconds")
# é preciso adicionar números na lista de stopwords
stopwords_customizadas = {'É', 'FATO', "FAKE", "mostre", 'após', 'logo', 'R', 'ser', 'dizer', 'usar', 'meio'}
#stopwords_customizadas = None
lista_tokens_fake = []
# carrega o idioma português no spacy apenas uma vez, não mais a cada token criado
nlp = spacy.load("pt_core_news_sm")
#print("Carregando idioma português ", time.time() - start_time, "seconds")
for x in lista_posts_fake:
    token = Token(id=x._id, nlp=nlp, texto=x.titulo, stopwords_customizadas=stopwords_customizadas)
    #print("Tokenizando títulos ", time.time() - start_time, "seconds")
    lista_tokens_fake.append(token)
    # último parametro, 0, representa que é uma notícia falsa
    tTokens.inserir_token(token._id, token.tokens_lematizados, 0)

lista_posts_fato = tPosts.consulta_post_titulo("É #FATO que", limite=200000)
stopwords_customizadas = {'É', 'FATO', "FAKE", "mostre", 'após', 'logo', 'R', 'ser', 'dizer', 'usar', 'meio'}
lista_tokens_fato = []
for y in lista_posts_fato:
    token = Token(id=y._id, nlp=nlp, texto=y.titulo, stopwords_customizadas=stopwords_customizadas)
    lista_tokens_fato.append(token)
    # último parametro, 0, representa que é uma notícia verdadeira
    tTokens.inserir_token(token._id, token.tokens_lematizados, 1)
print(time.time() - start_time, "seconds")