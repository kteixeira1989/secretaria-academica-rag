from pathlib import Path
from sentence_transformers import SentenceTransformer, util


# Modelo gratuito de embeddings
modelo = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def carregar_documento():
    caminho = Path("documentos/regulamento_academico.txt")

    with open(caminho, "r", encoding="utf-8") as arquivo:
        return arquivo.read()


def _eh_titulo(paragrafo):
    return paragrafo == paragrafo.upper() and any(
        letra.isalpha() for letra in paragrafo
    )


def criar_secoes():
    documento = carregar_documento()
    paragrafos = [
        paragrafo.strip()
        for paragrafo in documento.split("\n\n")
        if paragrafo.strip()
    ]

    secoes = []
    titulo = None
    conteudo = []

    for paragrafo in paragrafos:
        if _eh_titulo(paragrafo):
            if titulo is not None and conteudo:
                secoes.append(titulo + "\n\n" + "\n\n".join(conteudo))
            titulo = paragrafo
            conteudo = []
        elif titulo is not None:
            conteudo.append(paragrafo)

    if titulo is not None and conteudo:
        secoes.append(titulo + "\n\n" + "\n\n".join(conteudo))

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