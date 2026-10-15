import streamlit as st
from rag import buscar_contexto

st.title("Assistente Virtual de Secretaria Acadêmica")
st.write("Faça uma pergunta sobre procedimentos e regras acadêmicas.")

pergunta = st.text_input("Digite sua pergunta:")

if st.button("Perguntar"):
    if pergunta:
        contexto = buscar_contexto(pergunta)

        st.subheader("Resposta")
        st.write(contexto)
    else:
        st.warning("Digite uma pergunta antes de continuar.")