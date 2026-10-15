from pathlib import Path
from sentence_transformers import SentenceTransformer, util


# Modelo gratuito de embeddings
modelo = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def carregar_documento():
    caminho = Path("documentos/regulamento_academico.txt")

    with open(caminho, "r", encoding="utf-8") as arquivo:
        return arquivo.read()


def criar_secoes():
    documento = carregar_documento()
    partes = documento.split("\n\n")

    secoes = []

    for indice in range(1, len(partes), 2):
        titulo = partes[indice]

        if indice + 1 < len(partes):
            conteudo = partes[indice + 1]
            secoes.append(titulo + "\n\n" + conteudo)

    return secoes


def buscar_contexto(pergunta):
    secoes = criar_secoes()

    embeddings_secoes = modelo.encode(
        secoes,
        convert_to_tensor=True
    )

    embedding_pergunta = modelo.encode(
        pergunta,
        convert_to_tensor=True
    )

    similaridades = util.cos_sim(
        embedding_pergunta,
        embeddings_secoes
    )[0]

    melhor_indice = similaridades.argmax().item()
    melhor_score = similaridades[melhor_indice].item()

    if melhor_score < 0.30:
        return "Não encontrei essa informação nos documentos disponíveis."

    return secoes[melhor_indice]