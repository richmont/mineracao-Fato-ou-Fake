# referencia https://www.geeksforgeeks.org/removing-stop-words-nltk-python/
import nltk
from nltk.corpus import stopwords as sw
import unicodedata
#from spacy.lang.pt import Portuguese
#from spacy import displacy
import spacy

#nlp_pt = Portuguese()
import time

start_time = time.time()

class Token:
    """
    Objeto que representa o pré-processamento
    de texto em tokens limpos de stopwords e pontuação
    """

    def __init__(self, id, nlp, stopwords_customizadas=None, texto=None):
        print("antes de inicializar o objeto ", time.time() - start_time, "seconds")
        """
        Inicializa o objeto Token com stopwords padrões do NLTK,
        mas dá a opção de receber uma lista de stopwords do usuário

        Parâmetros:
        texto (string)
        id (string)
        stopwords_customizadas (set) [opcional]
        """
        #self.nlp = Portuguese() # objeto do processador de linguagem natural
        
        self.texto = texto  # texto a ser tratado
        self.lista_stopwords = []  # inicializa a variável vazia
        self.tokens_filtrados = [] # palavras filtradas sem stopwords e pontuação
        self.nomes_proprios = []
        self.tokens_lematizados = []
        self._id = id # identificador único da notícia
        self.nlp = nlp
        try:
            # passa pra lista as stopwords padrão da língua portuguesa
            self.lista_stopwords = sw.words('portuguese')
        except LookupError:
            """    
            Necessário executar estes dois comandos do NLTK para download
            dos pacotes necessários ao funcionamento das stopwords
            """
            nltk.download("punkt")
            nltk.download("stopwords")
            self.lista_stopwords = sw.words('portuguese')
        print("Recebendo stopwords do NLTK", time.time() - start_time, "seconds")
        if stopwords_customizadas is not None:
            """
            se o método recebeu a lista de stopwords customizadas,
            inclui na lista principal
            """
            for x in stopwords_customizadas:
                # verifica se os membros da lista recebida são strings
                if isinstance(x, str):
                    self.lista_stopwords.append(x)
                else:
                    # ignora valores não string e exibe erro ao usuário
                    print("Apenas strings são aceitas como stopwords,", x ,"ignorado")

        # executa a limpeza automaticamente após inicializar com o texto
        self.limpeza_stopwords()
        print("após limpeza stopwords ",time.time() - start_time, "seconds")
        #self.exibir_entidades()

    def remover_acentos(self, palavra):
        # fonte: https://stackoverflow.com/questions/517923/what-is-the-best-way-to-remove-accents-normalize-in-a-python-unicode-string
        """
        Parâmetros:
        palavra (string)

        Remove os acentos da palavra
        retorna uma palavra do tipo "byte" e não string
        """
        nfkd_form = unicodedata.normalize('NFKD', palavra)
        return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

    def verifica_capitalizacao(self, palavra):
        """
        Parâmetros:
        palavra (string)

        Verifica se a primeira letra da palavra é maiúscula
        ajuda a distinguir nomes próprios para escapar da radicalização
        """
        if palavra[0].isupper():
            return True
        else:
            return False

    def limpeza_stopwords(self):
        """
        Método para remover do token bruto as stopwords
        (nativas do NLTK ou inseridas pelo usuário) e pontuação.
        Cria no objeto a variável tokens_filtrados quando termina de trabalhar
        """
        
        if isinstance(self.texto, str):  # verifica se a var recebida é string
            # tokeniza o texto bruto
            print("antes de processar o token bruto ", time.time() - start_time, "seconds")
            self.token_bruto = self.nlp(self.texto)
            print("processamento do token bruto pra objeto spacy ", time.time() - start_time, "seconds")
            self.tokens_filtrados = []
            for x in self.token_bruto:
                # para cada elemento no token bruto
                # verifica se é alfanumérico (ignorando pontuação)
                # e se não consta na lista de stopwords
                # excecão para palavras com hífen adicionada
                # resultados de dois engines de stopwords divergem
                # como o melhor resultado são menos stopwords, usaremos ambos
                if x.text.isalnum() and (x.text not in self.lista_stopwords) or ("-" in x.text) and (not x.is_stop):
                    #print("após o if ", time.time() - start_time, "seconds")
                    self.tokens_filtrados.append(x)
                    if x.pos_ == 'PROPN':
                        #print("extrair nomes proprios ", time.time() - start_time, "seconds")
                        self.nomes_proprios.append(x.text)
                    self.tokens_lematizados.append(x.lemma_)
                    #print("lematização ", time.time() - start_time, "seconds")

        else:
            raise TypeError("Só consigo tratar strings")
