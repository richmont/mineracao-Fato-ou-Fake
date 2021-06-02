import sqlite3
import math
from sqlite3 import Error
# permite importar de diretório acima mesmo sem estar em um pacote
# fonte https://gist.github.com/JungeAlexander/6ce0a5213f3af56d7369
import os, sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from post import *
#from token import Token


def conectar(nome_arquivo):
    """
    nome_arquivo (string)
    realiza a conexão SQLite ao arquivo informado nesta variável
    Caso não exista, será criado
    não esqueça de criar as tabelas antes de inserir dados
    """
    conexao = sqlite3.connect(nome_arquivo)
    # definindo um cursor
    cursor = conexao.cursor()
    return cursor


class Banco:
    """
    Objeto que contém todos os métodos para interagir com dados do banco SQLite
    seu parâmetro de criação é o cursor referente ao banco usado
    """
    def __init__(self, cursor):
        self.cursor = cursor      

    def tamanho_numero(self, numero):
        if numero == 0:
            return None
        elif isinstance(numero, int):
            digits = int(math.log10(numero))+1
            return digits
        else:
            return None

    def existe_by_id(self, _id, tabela='posts'):
        """
        Parâmetros:
        _id (string)

        Consulta o banco e verifica se determinada entrada existe, localizando pelo id
        retorna booleano
        """
        query_verificar_existe = f"SELECT _id from {tabela} where _id = '{_id}'"
        self.cursor.execute(query_verificar_existe)
        # o resultado do fetchone é None caso não seja encontrado nada no banco
        resultado = self.cursor.fetchone()
        if resultado is None:
            return False
        else:
            return True

    def alterar(self, _id, alteracao, tabela='posts'):
        """
        Parãmetros:
        cursor (SQLite cursor)
        _id (string)
        alteracao (lista)

        Altera uma entrada já existente no banco
        localiza o campo pelo _id, o registro chave
        """
        if self.existe_by_id(_id):
            string_alteracoes = str()
            # para cada chave da alteração
            for x in alteracao.keys():
                # concatena o trecho da alteração
                # com a chave (x) e seu conteúdo (alteracao[x])
                
                string_alteracoes += f"'{x}' = '{alteracao[x]}'"
            # monta a query incluindo o trecho dos campos alterados e o _id
            # importante ter aspas simples em cada entrada
            query_alterar = str(f"update {tabela} set {string_alteracoes} where _id = '{_id}'")
            try:
                self.cursor.execute(query_alterar)
                self.cursor.connection.commit()
            # tentar alterar uma coluna que não existe retorna esse erro
            except sqlite3.OperationalError as e:
                print("Alteração falhou: ", e)
        else:
            print("_id não localizado, alteração falhou")

    def apagar(self, _id, tabela='posts'):
        """
        Parâmetros:
        _id (string)

        Apaga do banco de dados a entrada correspondente a _id informada
        """
        if self.existe_by_id(_id):
            query_apagar = f"delete from {tabela} where '_id' = '{_id}'"
            try:
                self.cursor.execute(query_apagar)
                self.cursor.connection.commit()
            except sqlite3.OperationalError as e:
                print("Apagar falhou: verifique as tabelas do banco ou execute criar_tabela ", e)
        else:
            print("Apagar falhou, id não existe")

    """
    CONSULTAS
    """

    def quantidade_total(self, tabela='posts'):
        """
        Conta quantas entradas há no banco de dados
        Retorna um inteiro
        """
        query_contar = f"select count() from {tabela}"
        self.cursor.execute(query_contar)
        resultado = self.cursor.fetchone()
        return resultado[0]

    def consulta_tudo(self, limite=5, tabela='posts'):
        """
        Consulta a tabela inteira do banco

        Parâmetros:
        limite (int) Limita a quantidade máxmma de posts retornados

        Retorna lista de objetos Post
        """
        if limite is None:
            query_tudo = f"select * from {tabela}"
        elif isinstance(limite, int):
            query_tudo = f"select * from {tabela} limit {limite}"
        else:
            raise TypeError("Valor de limite inválido: ", limite)
        self.cursor.execute(query_tudo)
        resultado = self.cursor.fetchall()
        lista_consulta = []
        for x in resultado:
            if tabela == 'posts':
                # se consultamos a tabela "posts", retorna objeto Post
                post = tupla_to_post(x)
                lista_consulta.append(post)
                del post
            else:
                # senão retorna dados simples do banco
                # preparar objeto referente a outra tabela
                lista_consulta.append(x)
        return lista_consulta


class TabelaPosts(Banco):
    def __init__(self, cursor):
        super().__init__(cursor)
    
    def existe_by_titulo(self, titulo):
        """
        Parâmetros:
        titulo (string)

        Consulta o banco e verifica se determinada entrada existe, localizando pelo titulo
        retorna booleano
        """
        
        self.cursor.execute('''select _id from posts where titulo like (?)''', [titulo])
        # o resultado do fetchone é None caso não seja encontrado nada no banco
        resultado = self.cursor.fetchone()
        
        if resultado is None:
            return False
        else:
            return True

    def criar_tabela(self):
        """
        Cria as tabelas necessárias ao funcionamento do banco, 
        requisito rodar esse método antes de inserir dados
        """
        # criando a tabela (schema)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
                _id TEXT NOT NULL PRIMARY KEY,
                titulo TEXT NOT NULL,
                data_publicacao TEXT NOT NULL,
                resumo     TEXT NOT NULL,
                post_url TEXT NOT NULL
        );
        """)
        self.cursor.connection.commit()
        print('Tabela criada com sucesso.')
        #self.cursor.close()

    def inserir(self, post):
        """
        Parâmetros:
        Post (objeto post que contém o conteúdo)
        insere as informações de um objeto Post na tabela do banco

        retorna o id da entrada inserido
        """

        
        # única maneira de evitar que textos com aspas causem erro na query é inserir desta maneira
        # também é mais fácil, no fim das contas
        query_inserir = f'''INSERT INTO posts (_id, titulo, data_publicacao, resumo, post_url) VALUES (?,?,?,?,?)'''
        valores = [post._id, post.titulo, post.data_publicacao, post.resumo, post.post_url]
        
        if self.existe_by_id(f"{post._id}"):
            print("Já existe um post com este id no banco, pulando")
            return None
        if self.existe_by_titulo(f"{post.titulo}"):
            print("Já existe um post com este título no banco, pulando")
            return None
        else:
            try:
                self.cursor.execute(query_inserir, valores)
                # cursor pode commitar a query usando o método "connection"
                # fonte: https://stackoverflow.com/questions/50429589/python-sqlite3-is-commit-used-on-the-connect-or-cursor/50429875
                self.cursor.connection.commit()
            # exceção ao erro de entrada duplicada no banco
            except sqlite3.IntegrityError:
                print("Documento já existe no banco")
                return None
            #except sqlite3.OperationalError:
                # exceção da ausência das tabelas, oo que impede inserção dos dados
                # necessário rodar o método "criar_tabelas" caso haja esse problema
                #print("Por favor, crie as tabelas no banco antes de inserir dados")
            # consulta o id recém inserido, retorna caso localize
            consulta_id_query = f"SELECT _id from posts where _id = '{post._id}'"
            self.cursor.execute(consulta_id_query)
            # consulta apenas uma entrada, é o bastante aqui
            resultado = self.cursor.fetchone()
            # fecha o cursor após terminar de consultar o banco
            #self.cursor.close()
            # cursor retorna uma tupla, com o valor que interessa na primeira posição
            return resultado[0]
 
    def consulta_posts_data(self, ano=None, mes=None, dia=None, limite=10, pular=None, query_secundaria = None):
        """
        ano (int{4}) \n
        mes (int{2}) \n
        dia (int{2}) \n
        limite (int) \n
        pular (int)
        
        Consulta no banco filtrando pela data do post

        verificação rápida se qualquer um dos valores é nulo

        Caso um dos valores de data seja None
        Associa esse valor com a regex para funcionar com um range de números
        """
        data = ""
        if ano is None:
            ano = "\d{4}"
        else:
            int_ano = ano
            if self.tamanho_numero(int_ano) == 2:
                ano = "20" + str(ano)
                # ano ok com 4 digitos
            elif self.tamanho_numero(int_ano) == 4:
                # número no tamanho correto, dois dígitos
                # checa se o valor do ano está no alcance de anos normais
                if int_ano < 1900 or int_ano > 3000:
                    print("valor do ano inválido: ", ano)
                    return None
                else:
                    # se o valor de ano passou nas checagens, concatena na data, começando pelo ano
                    data += str(ano )
            else:
                print("valor do ano inválido: ", ano)
                return None
        
        if mes is None:
            mes = "\d{2}"
        else:
            int_mes = mes
            if self.tamanho_numero(int_mes) == 1:
                # acrescenta 0 na frente de número de um dígito
                mes = "0" + str(mes)
                # mes ok com 2 digitos
            elif self.tamanho_numero(int_mes) == 2:
                # número no tamanho correto, dois dígitos
                # checa se o valor do mes está no alcance de mess normais
                if int_mes < 1 or int_mes > 12:
                    # retorna None e termina
                    print("valor do mes inválido: ", mes)
                    return None
                else:
                    data += "-"+str(mes)
            else:
                print("valor do mes inválido: ", mes)
                return None

        if dia is None:
            dia = "\d{2}"
        else:
            int_dia = dia
            if self.tamanho_numero(int_dia) == 1:
                # acrescenta 0 na frente de número de um dígito
                dia = "0" + str(dia)
                # dia ok com 2 digitos
            elif self.tamanho_numero(int_dia) == 2:
                # número no tamanho correto, dois dígitos
                # checa se o valor do dia está no alcance de dias normais
                if int_dia < 1 or int_dia > 31:
                    # retorna None e termina
                    print("valor do dia inválido: ", dia)
                    return None
                else:
                    data += "-"+str(dia)
            else:
                print("valor do dia inválido: ", dia)
                return None
        lista_posts = []
        # se pular é nulo ou não é um inteiro
        if pular == None or isinstance(pular, int) is not True:
            if query_secundaria != None:
                query_consulta_data = f"select * from posts where data_publicacao like '%{data}%' and {query_secundaria} limit {limite}"
                print(query_consulta_data)
                self.cursor.execute(query_consulta_data)
                resultado = self.cursor.fetchall()
                for x in resultado:
                    post = tupla_to_post(x)
                    lista_posts.append(post)
            query_consulta_data = f"select * from posts where data_publicacao like '%{data}%' limit {limite}"
            self.cursor.execute(query_consulta_data)
            resultado = self.cursor.fetchall()
            for x in resultado:
                    post = tupla_to_post(x)
                    lista_posts.append(post)
            # caso a consulta não retorne nada, resultado será None
            return lista_posts
        else:
            
            query_consulta_data = f"select * from posts where data_publicacao like '%{data}%' limit {limite} offset {pular}"
            self.cursor.execute(query_consulta_data)
            resultado = self.cursor.fetchall()
            for x in resultado:
                post = tupla_to_post(x)
                lista_posts.append(post)
            # caso a consulta não retorne nada, resultado será None
            return lista_posts

    def consulta_post_id(self, _id):
        """
        Parametros:
        _id = (string)

        Retorna um objeto Post
        """
        if self.existe_by_id(_id):
            query_post_by_id = f"select * from posts where _id = '{_id}'"
            self.cursor.execute(query_post_by_id)
            resultado = self.cursor.fetchone()
            post = tupla_to_post(resultado)
            return post
        else:
            return None

    def consulta_post_titulo(self, titulo, limite=5):
        """
        Parametros:
        titulo = (string)

        Retorna uma lista com objetos post localizados
        """
        self.cursor.execute("select * from posts where titulo like (?) limit (?)", [f"%{titulo}%", limite])
        resultado = self.cursor.fetchall()
        lista_posts = []
        for x in resultado:
            # para cada tupla recebida na consulta, 
            # cria um objeto post e insere no fim da lista
            post = tupla_to_post(x)
            lista_posts.append(post)
            del post
        # retorna a lista de objetos post
        return lista_posts


class TabelaTokens(Banco):
    def __init__(self, cursor):
        super().__init__(cursor)
    
    def criar_tabela(self):
        """
        Cria as tabelas necessárias ao funcionamento do banco, 
        requisito rodar esse método antes de inserir dados
        """
        # criando a tabela (schema)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS tokens (
                id_base INTEGER PRIMARY KEY,
                id_post TEXT NOT NULL,
                token TEXT NOT NULL,
                status INTEGER NOT NULL
        );
        """)
        self.cursor.connection.commit()
        print('Tabela criada com sucesso.')

    def consulta_tokens_by_id_post(self, id_post):
        """
        Retorna uma lista com todos os tokens 
        identificados pelo id do post
        Parâmetros:
        id_post (string)

        Retorna:
        list
        """
        # retorna None se um ou ambos os parametros são None
        if token is None:
            return None
        elif id_post is None:
            return None

        consulta_id_post_query = f"SELECT token from tokens where id_post = '{id_post}'"
        self.cursor.execute(consulta_id_post_query)
        resultado = self.cursor.fetchall()
        lista_tokens = []
        if resultado is None:
            return None
        else:
            for x in resultado:
                lista_tokens.append(x)
            return lista_tokens

    def consulta_id_base_by_id_post(self, id_post):
        """
        Retorna uma lista com todos os id_base 
        identificados pelo id_post
        Parâmetros:
        id_post (string)

        Retorna:
        list
        """
        # retorna None se um ou ambos os parametros são None
        if id_post is None:
            return None
        else:
            consulta_id_post_query = f"SELECT id_base from tokens where id_post = '{id_post}'"
            self.cursor.execute(consulta_id_post_query)
            resultado = self.cursor.fetchall()
            lista_id_base = []
            if resultado is None:
                return None
            else:
                for x in resultado:
                    lista_id_base.append(x)
                return lista_id_base

    def inserir_token(self, id_post, tokens, status):
        """
        Insere no banco os tokenss recebidos por
        parâmetros de id_post e tokens (string)
        Parâmetros:
        id_post (string)
        tokens (list),
        status (int)

        Retorna: 
        lista com id_base dos tokenss inseridos
        """
        if id_post is None:
            return None
        elif tokens is None:
            return None
        elif status is None:
            return None
        else:
            valores = []
            for x in tokens:
                
                if self.existe_by_token_e_id(token=x, id_post=id_post):
                    # já existe entrada no banco com esses dados
                    print("token", x, "com id_post", id_post, "já existe no banco, pulando")
                else:
                    # não existe, inclui na lista
                    token_para_inserir = [id_post, x, status]
                    valores.append(token_para_inserir)
                    token_para_inserir = None
            if len(valores) is None:
                # nenhum token inserido
                return False
            else:
                for y in valores:
                    self.cursor.execute('INSERT INTO tokens (id_post, token, status) VALUES (?, ?, ?)', y)
                    self.cursor.connection.commit()
                lista_id_base = self.consulta_id_base_by_id_post(id_post)
                return lista_id_base    

    def existe_by_token_e_id(self, token, id_post):
        """
        Verifica se já existe no banco uma entrada com
        o mesmo token e o mesmo _id
        evitando duplicidade
        """

        # retorna None se um ou ambos os parametros são None
        if token is None:
            return None
        elif id_post is None:
            return None

        consulta_id_query = f"SELECT id_base from tokens where id_post = '{id_post}' and token = '{token}'"
        self.cursor.execute(consulta_id_query)
        resultado = self.cursor.fetchone()
        
        if resultado is None:
            # objeto do resultado é None, consulta vazia
            return False  # não existe
        # consulta tem conteúdo, então
        else:
            return True  # existe

    def consulta_by_palavra(self, palavra):
        """
        Consulta no campo "token" a palavra recebida
        retorna uma lista com os ids_base e id_post onde a palavra ocorre

        Parâmetros:
        palavra (string)

        Retorna:
        ids_post (lista)
        """
        # retorna None se um ou ambos os parametros são None
        if token is None:
            return None
        else:
            consulta_id_post_query = f"SELECT token, id_post from tokens where token = '{palavra}'"
            self.cursor.execute(consulta_id_post_query)
            resultado = self.cursor.fetchall()
            lista_tokens = []
            if resultado is None:
                return None
            else:
                for x in resultado:
                    lista_tokens.append(x)
                return lista_tokens

    def recupera_posts(self):
        """
        Recupera todos os posts a partir do banco de tokens
        
        Retorna:
        lista_posts (dict)
        Dicionário que contém id_post, titulo, status
        """

        self.cursor.execute('select id_post from tokens')
        resultado = self.cursor.fetchall()
        lista = list()
        for x in resultado:
            id_post = x[0]
            elemento = {'id_post': id_post}
            lista.append(elemento)
            del elemento
        del resultado
        data = lista
        # sets não aceitam valores duplicados
        lista_ids = set()
        for x in data:
            lista_ids.add(x['id_post'])        

        lista_token_post = list()
        for x in lista_ids:
            id_post = x
            self.cursor.execute(f'select id_post,status,token from tokens where id_post = "{x}"')
            resultado = self.cursor.fetchall()
            # status coletado apenas do primeiro resultado
            #print(resultado[0])
            status = resultado[0][1]
            titulo = str()
            for y in resultado:
                titulo += str(y[2]+ " ")
            un_post = {'id_post': id_post, 'status': status, 'titulo': titulo}
            lista_token_post.append(un_post)
        return lista_token_post