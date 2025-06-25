
import streamlit as st
import openai

openai.api_key = "sk-SUA_CHAVE_AQUI"  # Substitua pela sua chave real da OpenAI

st.set_page_config(page_title="Chat Personalizado", layout="centered")

st.title("🤖 Chat Amigável e Respeitoso")
st.markdown("Preencha suas informações para iniciar a conversa com a IA:")

# Formulário
with st.form(key="formulario"):
    idade = st.text_input("1. Quantos anos você tem?")
    local = st.text_input("2. De onde você é? (cidade, estado ou região)")
    escolaridade = st.selectbox(
        "3. Qual seu nível de escolaridade?",
        ["Ensino fundamental", "Ensino médio", "Faculdade", "Mestrado", "Doutorado", "Pós-doutorado"]
    )
    religiao = st.text_input("4. Qual é sua religião?")
    enviar = st.form_submit_button("🔁 Enviar para IA")

# Função de análise
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

# Gera o prompt com base nas respostas
def gerar_prompt(idade, escolaridade, regiao, girias, nacionalidade, religiao):
    return f"""
Haja como uma IA amigável e respeitosa, como se estivesse falando com um amigo usando as formas de falar do {nacionalidade}.

Você está conversando com uma pessoa que:
- Tem {idade} anos
- Tem o nível de escolaridade: {escolaridade}
- É da região: {regiao}
- Professa a religião: {religiao}
- Usa gírias como: {', '.join(girias) if girias else 'nenhuma gíria específica'}

Adapte sua linguagem para refletir a forma de se comunicar da região, com empatia e leveza. Use as gírias de forma natural.

**Nunca desrespeite crenças, cultura ou costumes da pessoa.** Mantenha um tom positivo, inclusivo e acolhedor.
""".strip()

# Ação ao enviar o formulário
if enviar:
    if not idade or not local or not religiao:
        st.warning("⚠️ Por favor, preencha todos os campos.")
    else:
        regiao, girias = identificar_regiao(local)
        nacionalidade = "Brasil"
        prompt = gerar_prompt(idade, escolaridade, regiao, girias, nacionalidade, religiao)

        with st.spinner("💬 Enviando para o ChatGPT..."):
            try:
                resposta = openai.ChatCompletion.create(
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
