
import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["openai"]["api_key"])

st.set_page_config(page_title="Chat Personalizado", layout="centered")
st.title("🤖 Chat Amigável e Respeitoso")
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
        return "Nordeste", ["arretado", "migué", "avexado", "visse", "oxente"]
    elif any(p in local for p in ["rio grande do sul", "santa catarina", "paraná", "sul", "porto alegre", "curitiba"]):
        return "Sul", ["bah", "tri", "tchê", "lagartear"]
    elif any(p in local for p in ["rio de janeiro", "são paulo", "espírito santo", "minas", "sudeste", "bh", "campinas"]):
        return "Sudeste", ["rolê", "padoca", "suave", "zueira", "daora"]
    elif any(p in local for p in ["goiás", "mato grosso", "brasília", "centro-oeste"]):
        return "Centro-Oeste", ["uai", "sô", "trem", "bereré"]
    elif any(p in local for p in ["amazonas", "pará", "roraima", "norte", "belém", "manaus"]):
        return "Norte", ["égua", "moscou", "gaiato", "de rocha"]
    else:
        return "Indefinida", []

# Geração do prompt
def gerar_prompt(nome, idade, escolaridade, regiao, girias, opiniao, aplicacao, relacao):
    return f"""
Haja como uma IA amigável e respeitosa, como se estivesse falando com um amigo.

A pessoa com quem você vai conversar:
- Se chama {nome}
- Tem {idade} anos
- É da região {regiao}
- Tem o nível de escolaridade: {escolaridade}
- Descreveu sua relação com IA como: {relacao}
- Disse que pensa o seguinte sobre IA: "{opiniao}"
- Disse que aplicaria IA assim: "{aplicacao}"
- Usa gírias como: {', '.join(girias) if girias else 'nenhuma gíria específica'}

Use um tom adaptado à região da pessoa, com empatia e leveza. Nunca desrespeite cultura ou crenças. Use as gírias com naturalidade e mantenha um tom acolhedor.
""".strip()

# Processamento após envio
if enviar:
    if not nome or not idade or not local or not opiniao_ia or not aplicacao_ia:
        st.warning("⚠️ Por favor, preencha todos os campos obrigatórios.")
    else:
        regiao, girias = identificar_regiao(local)
        prompt = gerar_prompt(nome, idade, escolaridade, regiao, girias, opiniao_ia, aplicacao_ia, relacao_ia)

        with st.spinner("💬 Enviando para o ChatGPT..."):
            try:
                resposta = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": "Oi! Pode se apresentar :)"}
                    ]
                )
                conteudo = resposta.choices[0].message.content
                st.success("✅ Resposta recebida!")
                st.markdown("**Resposta da IA:**")
                st.write(conteudo)
            except Exception as e:
                st.error("❌ Erro ao conversar com a IA.")
                st.code(str(e))
