from rag import buscar_contexto


def test_frequencia_minima():
    resultado = buscar_contexto("Qual é a frequência mínima para aprovação?")
    assert "75%" in resultado


def test_trancamento_inclui_documentos():
    resultado = buscar_contexto("Quais documentos preciso para trancar a matrícula?")
    assert "documento de identificação" in resultado
    assert "formulário de solicitação de trancamento" in resultado
