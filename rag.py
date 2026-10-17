import os
from pathlib import Path

from google import genai
from google.genai import errors
from sentence_transformers import SentenceTransformer, util


# Modelo gratuito de embeddings
modelo = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Modelo gratuito de geração (free tier do Gemini)
MODELO_GERACAO = "gemini-3.8-flash"


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


def montar_prompt(pergunta, contexto):
    return (
        "Responda à pergunta usando apenas o contexto abaixo, em português, "
        "de forma direta. Você pode fazer inferências simples e cálculos "
        "aritméticos diretamente derivados do contexto. Se a resposta não "
        "estiver no contexto e não puder ser deduzida dele, diga que não "
        "encontrou a informação.\n\n"
        f"Contexto:\n{contexto}\n\n"
        f"Pergunta: {pergunta}\n\n"
        "Resposta:"
    )


def gerar_resposta(pergunta, contexto):
    if contexto.startswith("Não encontrei"):
        return contexto

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    try:
        resposta = client.models.generate_content(
            model=MODELO_GERACAO,
            contents=montar_prompt(pergunta, contexto),
        )
    except errors.APIError as erro:
        if erro.code == 503:
            return (
                "O serviço de IA está temporariamente indisponível. "
                "Tente novamente em alguns instantes."
            )
        raise
    return resposta.text