from pymongo import MongoClient, errors
from pprint import pprint
import math
local = "mongodb://python:penis@localhost"
cliente = MongoClient(local)
banco = cliente.fato_ou_fake
posts = banco.posts


def tamanho_numero(numero):
    if numero is 0:
        return None
    elif isinstance(numero, int):
        digits = int(math.log10(numero))+1
        return digits
    else:
        return None


def consulta_campo_regex(colecao, consulta, limite=10):
    """
    colecao (MongoDB Collection) \n
    campo (str) \n
    consulta (set) \n
    Consulta no banco filtrando pelo campo e seu conteúdo por regex
    """
    for chave in consulta.keys():
        query = {chave: {'$regex': consulta[chave]}}
        resultado = colecao.find(query).limit(limite)
        r_lista = list(resultado)
        
        return r_lista


def consulta_posts_data(colecao=posts, ano=None, mes=None, dia=None, limite=10, pular=None):
    """
    colecao (MongoDB Collection)\n
    ano (int{4}) \n
    mes (int{2}) \n
    dia (int{2}) \n
    limite (int)
    
    Consulta no banco filtrando pela data do post
    """
    """
    verificação rápida se qualquer um dos valores é nulo
    """

        
    """
    Caso um dos valores de data seja None
    Associa esse valor com a regex para funcionar com um range de números
    """
    if dia is None:
        dia = "\d{2}"
    else:
        int_dia = dia
        if tamanho_numero(int_dia) is 1:
            # acrescenta 0 na frente de número de um dígito
            dia = "0" + str(dia)
            # dia ok com 2 digitos
        elif tamanho_numero(int_dia) is 2:
            # número no tamanho correto, dois dígitos
            # checa se o valor do dia está no alcance de dias normais
            if int_dia < 1 or int_dia > 31:
                # retorna None e termina
                print("valor do dia inválido: ", dia)
                return None
        else:
            print("valor do dia inválido: ", dia)
            return None
    if mes is None:
        mes = "\d{2}"
    else:
        int_mes = mes
        if tamanho_numero(int_mes) is 1:
            # acrescenta 0 na frente de número de um dígito
            mes = "0" + str(mes)
            # mes ok com 2 digitos
        elif tamanho_numero(int_mes) is 2:
            # número no tamanho correto, dois dígitos
            # checa se o valor do mes está no alcance de mess normais
            if int_mes < 1 or int_mes > 12:
                # retorna None e termina
                print("valor do mes inválido: ", mes)
                return None
        else:
            print("valor do mes inválido: ", mes)
            return None

    if ano is None:
        ano = "\d{4}"
    else:
        int_ano = ano
        if tamanho_numero(int_ano) is 2:
            ano = "20" + str(ano)
            # ano ok com 4 digitos
        elif tamanho_numero(int_ano) is 4:
            # número no tamanho correto, dois dígitos
            # checa se o valor do ano está no alcance de anos normais
            if int_ano < 1900 or int_ano > 3000:
                print("valor do ano inválido: ", ano)
                return None
        else:
            print("valor do ano inválido: ", ano)
            return None

    data = str(ano) + "." + str(mes) + "." + str(dia)
    # se pular é nulo ou não é um inteiro
    if pular is None or isinstance(pular, int) is not True:
        query = {'data_publicacao': {'$regex': data}}
        resultado = colecao.find(query).limit(limite)
        return resultado
    else:
        # consulta definindo o skip com var pular
        query = {'data_publicacao': {'$regex': data}}
        resultado = colecao.find(query).skip(pular).limit(limite)
        return resultado


def consulta_post_id(colecao, id):
    # recebe o documento compatível com o ID informado
    resultado = colecao.find_one({"_id": id})
    return resultado


def quantidade_total(colecao, consulta=None):
    if consulta is None:
        # consulta vazia para retornar todos os documentos da coleção
        resultado = colecao.count_documents({})
        return resultado
    else:
        # consulta obedecendo a query recebida
        resultado = colecao.count_documents(consulta)
        return resultado

def inserir(colecao, conteudo, **kwargs):
    """
    Parâmetros:
    colecao (MongoDB Collection)
    conteudo (json)
    id (str)
    Em caso de ausência do id, programa continua e
    deixa que o MongoDB gerencie o registro chave

    retorna o id do documento inserido
    """

    # se recebemos um id
    id = kwargs.get("id")
    if id is not None:
        # verifique se este id já existe no banco
        try:
            resposta = colecao.find_one({"_id": id})
        except errors.ServerSelectionTimeoutError:
                raise TimeoutError("Não consegui consultar o banco, verifique permissões de rede no servidor")
        if resposta is None:
            # elemento com id informado não existe no banco, inserir
            # retorna o id inserido
            campo = {}
            id_campo = {"_id": id}
            campo.update(id_campo)
            campo.update(conteudo)
            inserir = campo
            try:
                resultado = colecao.insert_one(inserir)
                return resultado.inserted_id
            except errors.ServerSelectionTimeoutError:
                raise TimeoutError("Não consegui gravar no banco, verifique permissões de rede no servidor")
            
        else:
            # elemento com id já existe no banco, retorna None
            print("Documento já existe no banco")
            return None
    else:
        # se não recebemos uma id o Mongo cria automaticamente
        try:
            resultado = colecao.insert_one(conteudo)
            return resultado.inserted_id
        except errors.ServerSelectionTimeoutError:
            raise TimeoutError("Não consegui gravar no banco, verifique permissões de rede no servidor")


def alterar(colecao, busca, alterado):
    """
    Parãmetros:
    colecao (MongoDB Collection)
    busca (json)
    alterado (json)

    Altera um documento já existente no banco
    localiza o campo correto pelo parâmetro de busca

    retorna o conteúdo do campo alterado
    """
    resposta = colecao.find_one(busca)
    if resposta is None:
        # elemento não encontrado, não alterar nada e retornar none
        return None
    else:
        mudanca = {"$set": alterado}
        try:
            resultado = colecao.update_one(busca, mudanca)
            return resultado
        except errors.ServerSelectionTimeoutError:
            raise TimeoutError("Não consegui gravar no banco, verifique permissões de rede no servidor")


def lista_chave_banco(colecao, chave, chave_interna):
    """
    colecao (MongoDB Collection)
    chave (str)
    chave_interna (str)

    Busca no banco o conteúdo de uma chave dentro de outra
    Por enquanto é o bastante pra colher metadados
    """
    # filtra apenas os documentos que contém o campo "items"
    try:
        bruto = colecao.distinct(chave)
    except errors.ServerSelectionTimeoutError:
            raise TimeoutError("Não consegui gravar no banco, verifique permissões de rede no servidor")
    conteudo = []
    for x in bruto:
        # agora pega o conteúdo e passa pra uma lista
        conteudo.append(x[chave_interna])
    return conteudo

"""
consulta = {"titulo": "#FAKE"}
resultado = consulta_campo_regex(posts, consulta)
print(resultado)
#for x in resultado:
#    print(x)

resultado = consulta_posts_data(colecao=posts, ano=2020)
for x in resultado:
    pprint(x)
"""
