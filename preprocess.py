# referencia https://www.geeksforgeeks.org/removing-stop-words-nltk-python/
import nltk
from nltk.corpus import stopwords as sw
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
import unicodedata


class Token:
    """
    Objeto que representa o pré-processamento
    de texto em tokens limpos de stopwords e pontuação
    """

    def __init__(self, id, stopwords_customizadas=None, texto=None):
        """
        Inicializa o objeto Token com stopwords padrões do NLTK,
        mas dá a opção de receber uma lista de stopwords do usuário

        Parâmetros:
        texto (string)
        id (string)
        stopwords_customizadas (set) [opcional]
        """
        
        self.texto = texto  # texto a ser tratado
        self.lista_stopwords = []  # inicializa a variável vazia
        self.tokens_filtrados = []
        self.tokens_stemmizados = []
        self.tokens_lematizados = []
        self._id = id
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
        self.stemmizacao()
        self.lematizacao()

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
            self.token_bruto = word_tokenize(self.texto)
            self.tokens_filtrados = []
            for x in self.token_bruto:
                # para cada elemento no token bruto
                # verifica se é alfanumérico (ignorando pontuação)
                # e se não consta na lista de stopwords
                # excecão para palavras com hífen adicionada
                if x.isalnum() and x not in self.lista_stopwords or "-" in x:
                    self.tokens_filtrados.append(x)
        else:
            raise TypeError("Só consigo tratar strings")

    def stemmizacao(self):
        # stemmização: https://trainyourmachine.com/extrair-radicais/
        stemmer = SnowballStemmer('portuguese')
        palavras = self.tokens_filtrados
        for palavra_acentuada in palavras:
            palavra = self.remover_acentos(palavra_acentuada)
            if self.verifica_capitalizacao(palavra):
                # se palavra é nome próprio
                # pula a stemmização e coloca direto na lista de resultado
                self.tokens_stemmizados.append(palavra)
            else:
                # não é nome próprio
                self.tokens_stemmizados.append(stemmer.stem(palavra))

    def lematizacao(self):
        # fonte: https://living-sun.com/pt/python/686087-simple-stemming-and-lemmatization-in-python-python-python-27-nlp.html
        try:
            lemmatizer = nltk.WordNetLemmatizer()
        except LookupError:
            nltk.download('wordnet')
            lemmatizer = nltk.WordNetLemmatizer()
        palavras = self.tokens_filtrados
        for palavra_acentuada in palavras:
            palavra = self.remover_acentos(palavra_acentuada)
            if self.verifica_capitalizacao(palavra):
                # se palavra é nome próprio
                # pula a stemmização e coloca direto na lista de resultado
                self.tokens_lematizados.append(palavra)
            else:
                # não é nome próprio
                self.tokens_lematizados.append(lemmatizer.lemmatize(palavra))
        
            
        #print [lemmatizer.lemmatize(t) for t in nltk.word_tokenize(temp_sent)]
