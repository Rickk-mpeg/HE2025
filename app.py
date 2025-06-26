import streamlit as st
import requests

api_key = st.secrets["huggingface"]["api_key"]

def gerar_resposta(prompt):
    url = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.post(url, headers=headers, json={"inputs": prompt})
    if response.status_code == 200:
        return response.json()[0].get("generated_text", "")
    return f"Erro: {response.status_code} – {response.text}"
    
# Função para avaliar o nível do funcionário em relação à IA
def avaliar_nivel_ia(relacao_ia, ferramentas_ia, uso_ia):
    pontuacao = 0

    # Peso da autoavaliação
    pesos_relacao = {
        "Nunca usei": 0,
        "Tenho receio": 10,
        "Não sei muito": 20,
        "Gosto, mas não sei usar": 30,
        "Boa": 60,
        "Uso com frequência": 80
    }
    pontuacao += pesos_relacao.get(relacao_ia, 0)

    # Peso das ferramentas citadas
    ferramentas = ferramentas_ia.lower().split(",")
    ferramentas_usadas = len([f for f in ferramentas if len(f.strip()) >= 3])
    pontuacao += min(ferramentas_usadas * 5, 20)

    # Peso do uso descrito
    if len(uso_ia.strip()) > 100:
        pontuacao += 20
    elif len(uso_ia.strip()) > 50:
        pontuacao += 10
    elif len(uso_ia.strip()) > 10:
        pontuacao += 5

    return min(pontuacao, 100)

# Interface
st.set_page_config(page_title="Diagnóstico de IA – RH", layout="centered")
st.title("📊 Diagnóstico de Familiaridade com Inteligência Artificial")

st.markdown("Preencha o formulário abaixo para avaliar seu nível de conhecimento e uso de IA:")

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
    ferramentas_ia = st.text_area("7. Quais ferramentas de IA você já usou? (ex: ChatGPT, Midjourney, Copilot, etc.)")
    uso_ia = st.text_area("8. Em que situações você já utilizou ou usaria uma IA?")
    
    submitted = st.form_submit_button("Enviar")

if submitted:
    erros = []
    if len(opiniao_ia.strip()) < 10:
        erros.append("A resposta da pergunta 6 deve ter pelo menos 10 caracteres.")
    if len(ferramentas_ia.strip()) < 10:
        erros.append("A resposta da pergunta 7 deve ter pelo menos 10 caracteres.")
    if len(uso_ia.strip()) < 10:
        erros.append("A resposta da pergunta 8 deve ter pelo menos 10 caracteres.")

    if erros:
        for erro in erros:
            st.error(erro)
    else:
        prompt = (
            f"Meu nome é {nome}, tenho {idade} anos, sou de {local}, "
            f"tenho escolaridade de nível {escolaridade}, minha relação com IA é '{relacao_ia}'. "
            f"Minha opinião sobre IA: {opiniao_ia}. "
            f"Já usei as seguintes ferramentas de IA: {ferramentas_ia}. "
            f"Utilizei ou usaria IA nas seguintes situações: {uso_ia}. "
            f"Com base nessas informações, me envie uma resposta amigável e clara sobre IA."
        )
        nivel_ia = avaliar_nivel_ia(relacao_ia, ferramentas_ia, uso_ia)
        st.info(f"Nível estimado de familiaridade com IA: **{nivel_ia}%**")

        with st.spinner("Aguardando resposta da IA..."):
            resposta = gerar_resposta(prompt)
            st.success("Resposta da IA:")
            st.write(resposta)
