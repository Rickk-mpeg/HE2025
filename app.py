
import streamlit as st
from google import genai

# Configurar API Gemini
genai.configure(api_key=st.secrets["gemini"]["api_key"])
model = genai.GenerativeModel("gemini-2.5-flash")

st.set_page_config(page_title="Chat com IA Gemini", layout="centered")
st.title("🤖 Chat com IA Gemini")
st.markdown("Preencha suas informações para iniciar a conversa com a IA:")

# Formulário
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
    aplicacao_ia = st.text_area("7. Como você aplicaria o uso das Inteligências Artificiais no seu dia a dia ou trabalho?")
    enviar = st.form_submit_button("🔁 Enviar para IA")

# Identificação de região
def identificar_regiao(local):
    local = local.lower()
    if any(p in local for p in ["ceará", "bahia", "pernambuco", "nordeste", "fortaleza", "recife", "salvador"]):
        return "Nordeste"
    elif any(p in local for p in ["rio grande do sul", "santa catarina", "paraná", "sul", "porto alegre", "curitiba"]):
        return "Sul"
    elif any(p in local for p in ["rio de janeiro", "são paulo", "espírito santo", "minas", "sudeste", "bh", "campinas"]):
        return "Sudeste"
    elif any(p in local for p in ["goiás", "mato grosso", "brasília", "centro-oeste"]):
        return "Centro-Oeste"
    elif any(p in local for p in ["amazonas", "pará", "roraima", "norte", "belém", "manaus"]):
        return "Norte"
    else:
        return "Indefinida"

# Geração do prompt
def gerar_prompt(nome, idade, escolaridade, regiao, opiniao, aplicacao, relacao):
    return f"""Aja como uma IA amigável, respeitosa e empática.

Informações do usuário:
- Nome: {nome}
- Idade: {idade}
- Região: {regiao}
- Escolaridade: {escolaridade}
- Relação com IA: {relacao}
- Opinião sobre IA: {opiniao}
- Aplicações pretendidas da IA: {aplicacao}

Responda de forma gentil e acolhedora, baseada nas informações fornecidas.
""".strip()

# Processamento após envio
if enviar:
    if not nome or not idade or not local or not opiniao_ia or not aplicacao_ia:
        st.warning("⚠️ Por favor, preencha todos os campos obrigatórios.")
    else:
        regiao = identificar_regiao(local)
        prompt = gerar_prompt(nome, idade, escolaridade, regiao, opiniao_ia, aplicacao_ia, relacao_ia)

        with st.spinner("💬 Enviando para a IA Gemini..."):
            try:
                response = model.generate_content(prompt)
                st.success("✅ Resposta recebida!")
                st.markdown("**Resposta da IA:**")
                st.write(response.text)
            except Exception as e:
                st.error("❌ Erro ao conversar com a IA.")
                st.code(str(e))
