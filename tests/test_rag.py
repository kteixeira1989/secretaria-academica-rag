from rag import buscar_contexto


def test_buscar_contexto_retorna_texto():
    resultado = buscar_contexto("Qual é a frequência mínima?")
    assert isinstance(resultado, str)
