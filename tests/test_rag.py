import rag
from google.genai import errors
from rag import buscar_contexto, gerar_resposta, montar_prompt


def test_frequencia_minima():
    resultado = buscar_contexto("Qual é a frequência mínima para aprovação?")
    assert "75%" in resultado


def test_trancamento_inclui_documentos():
    resultado = buscar_contexto("Quais documentos preciso para trancar a matrícula?")
    assert "documento de identificação" in resultado
    assert "formulário de solicitação de trancamento" in resultado


def test_gerar_resposta_sem_contexto_nao_chama_api():
    sem_resposta = "Não encontrei essa informação nos documentos disponíveis."
    assert gerar_resposta("Pergunta qualquer?", sem_resposta) == sem_resposta


def test_montar_prompt_inclui_pergunta_e_contexto():
    prompt = montar_prompt("Qual é a frequência mínima?", "FREQUÊNCIA MÍNIMA: 75%")
    assert "Qual é a frequência mínima?" in prompt
    assert "75%" in prompt


def test_gerar_resposta_erro_temporario(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "chave-falsa")

    class ClienteFalso:
        def __init__(self, *args, **kwargs):
            self.models = self

        def generate_content(self, *args, **kwargs):
            raise errors.APIError(503, {"error": {"message": "unavailable"}})

    monkeypatch.setattr(rag.genai, "Client", ClienteFalso)

    resultado = gerar_resposta("Qualquer pergunta?", "contexto qualquer")
    assert "temporariamente indisponível" in resultado
