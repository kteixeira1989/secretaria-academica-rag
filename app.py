import streamlit as st
from rag import buscar_contexto, gerar_resposta

st.title("Assistente Virtual de Secretaria Acadêmica")
st.write("Faça uma pergunta sobre procedimentos e regras acadêmicas.")

pergunta = st.text_input("Digite sua pergunta:")

if st.button("Perguntar"):
    if pergunta:
        contexto = buscar_contexto(pergunta)
        resposta = gerar_resposta(pergunta, contexto)

        st.subheader("Resposta")
        st.write(resposta)
    else:
        st.warning("Digite uma pergunta antes de continuar.")