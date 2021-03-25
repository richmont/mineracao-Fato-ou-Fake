class Post:
    def __init__(self, conteudo):
        """
        Inicializa o post com um dicionário com o conteúdo do post
        """
        self._id = conteudo['_id']
        self.titulo = conteudo['titulo']
        self.data_publicacao = conteudo['data_publicacao']
        self.resumo = conteudo['resumo']
        self.post_url = conteudo['post_url']

"""
Métodos para facilitar a criação de objetos Post
"""
def tupla_to_post(tupla):
    """
    SQlite retorna tuplas das consultas
    Converto esta tupla em objeto post

    Parametros:
    tupla (tupla)

    Retorno
    post (Post)
    """
    conteudo = {"_id": tupla[0], "titulo": tupla[1], "data_publicacao": tupla[2], "resumo": tupla[3], "post_url": tupla[4]}
    post = Post(conteudo)
    return post