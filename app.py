import streamlit as st
import requests

# Obter a API Key do arquivo secrets
api_key = st.secrets["huggingface"]["api_key"]

# Função para chamar a API da Hugging Face
def gerar_resposta(prompt):
    url = "https://api-inference.huggingface.co/models/google/flan-t5-large"
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {"inputs": prompt}

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()[0]["generated_text"]
    else:
        return f"Erro: {response.status_code} - {response.text}"

# Interface Streamlit
st.set_page_config(page_title="Chat com Hugging Face", layout="centered")
st.title("🤖 Chat com Hugging Face")

st.markdown("Preencha suas informações para iniciar a conversa:")

with st.form(key="formulario"):
    nome = st.text_input("1. Qual o seu nome completo?")
    idade = st.text_input("2. Qual a sua idade?")
    local = st.text_input("3. De onde você é? (Cidade, estado ou região)")
    escolaridade = st.selectbox(
        "4. Qual seu nível de escolaridade?",
        ["Ensino fundamental", "Ensino médio", "Faculdade", "Mestrado", "Doutorado", "Pós-doutorado"]
    )
    relacao_ia = st.selectbox(
        "5. Qual sua relação com as Inteligências Artificiais?",
        ["Boa", "Não sei muito", "Gosto, mas não sei usar", "Tenho receio", "Nunca usei", "Uso com frequência"]
    )
    opiniao_ia = st.text_area("6. O que você pensa sobre as Inteligências Artificiais?")
    submitted = st.form_submit_button("Enviar")

if submitted:
    prompt = (
        f"Meu nome é {nome}, tenho {idade} anos, sou de {local}, "
        f"tenho escolaridade de nível {escolaridade}, minha relação com IA é '{relacao_ia}' "
        f"e eu penso o seguinte sobre IA: {opiniao_ia}. "
        f"Com base nisso, me envie uma resposta amigável e clara sobre IA."
    )
    with st.spinner("Aguardando resposta da IA..."):
        resposta = gerar_resposta(prompt)
        st.success("Resposta da IA:")
        st.write(resposta)
