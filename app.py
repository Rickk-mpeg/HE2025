
import streamlit as st 
import requests
import pycountry

# --- CONFIG ---
st.set_page_config(page_title="Diagnóstico de IA - RH", layout="centered")

col1, col2 = st.columns([1, 6])
with col1:
    st.image("priai.png", width=70)
with col2:
    st.title("Priscila AI")

st.markdown("Olá, seja bem vindo ao Processo de Requalificação Industrial! bom saber que você se interessa pelo uso de inteligências artificiais; Responda o questionário a seguir, para sabermos o seu nível de afinidade com a inteligência artificial:")

# --- CHAVE DE API ---
api_key = st.secrets["huggingface"]["api_key"]

# --- IDIOMAS POR PAÍS ---
idiomas_por_pais = {
    "BR": "portuguese",
    "PT": "portuguese",
    "US": "english",
    "GB": "english",
    "ES": "spanish",
    "MX": "spanish",
    "FR": "french",
    "DE": "german",
}

# --- GERAR RESPOSTA ---
def gerar_resposta(prompt, idioma="portuguese"):
    url = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
    headers = {"Authorization": f"Bearer {api_key}"}
    prompt = f"<|system|>\nYou are an AI that replies in {idioma}.\n<|user|>\n{prompt}\n<|assistant|>"
    response = requests.post(url, headers=headers, json={"inputs": prompt}, timeout=30)

    if response.status_code == 200:
        try:
            texto = response.json()[0].get("generated_text", "")
            return texto.split("<|assistant|>")[-1].strip()
        except Exception as e:
            return f"Erro ao interpretar resposta: {e}"
    return f"Erro: {response.status_code} – {response.text}"

# --- AVALIAÇÃO ---
def avaliar_nivel_ia(relacao, ferramentas, uso, freq, autonomia, setores, escolaridade):
    nota = 0
    nota += {
        "Nunca usei": 0, "Tenho receio": 10, "Não sei muito": 20,
        "Gosto, mas não sei usar": 30, "Boa": 60, "Uso com frequência": 80
    }.get(relacao, 0)
    nota += min(len([f for f in ferramentas.lower().split(",") if len(f.strip()) >= 3]) * 5, 20)
    nota += 20 if len(uso) > 100 else 10 if len(uso) > 50 else 5 if len(uso) > 10 else 0
    nota += {
        "Nunca": 0, "Raramente": 5, "Mensalmente": 10, "Semanalmente": 15, "Diariamente": 20
    }.get(freq, 0)
    nota += {
        "Preciso de ajuda para tudo": 0, "Consigo usar com orientação": 10,
        "Aprendo com tutoriais": 20, "Sou autodidata e crio soluções": 30
    }.get(autonomia, 0)
    nota += min(len([s for s in setores.lower().split(",") if len(s) >= 3]) * 2, 10)
    nota += {"Ensino fundamental": 0, "Ensino médio": 10, "Faculdade ou outros": 20}.get(escolaridade, 0)
    return min(nota, 100)

# --- PAÍSES ---
paises = sorted([(c.name, c.alpha_2) for c in pycountry.countries], key=lambda x: x[0])

# --- FORMULÁRIO ---
with st.form("formulario"):
    nome = st.text_input("1. Nome completo:")
    idade = st.selectbox("2. Idade:", ["Menos de 18", "18 a 25", "26 a 35", "36 a 45", "46 a 60", "Acima de 60"])
    pais_nome, pais_codigo = st.selectbox("3. País:", paises)
    estado = st.text_input("3.1 Estado ou região:")
    cidade = st.text_input("3.2 Cidade:")
    escolaridade = st.selectbox("4. Escolaridade:", ["Ensino fundamental", "Ensino médio", "Faculdade ou outros"])
    relacao_ia = st.selectbox("5. Qual é a sua relação com IA:", ["Boa", "Não sei muito", "Gosto, mas não sei usar", "Tenho receio", "Nunca usei", "Uso com frequência"])
    opiniao_ia = st.text_area("6. O que você pensa sobre IA?")
    ferramentas_ia = st.text_area("7. Quais ferramentas de IA você já usou?(ChatGPT, Copilot, Gemini, Midjourney, Suno)")
    uso_ia = st.text_area("8. Em quais situações você já usou ou usaria uma IA?")
    frequencia_uso = st.selectbox("9. Com que frequência você faz o uso de IA:", ["Nunca", "Raramente", "Mensalmente", "Semanalmente", "Diariamente"])
    autonomia = st.selectbox("10. Como você se sente usando IA:", ["Preciso de ajuda para tudo", "Consigo usar com orientação", "Aprendo com tutoriais", "Sou autodidata e crio soluções"])
    setores = st.text_area("11. Áreas com potencial para aplicar IA?")
    aprendizado = st.text_area("12. Como Você aprende ou aprendeu a usar IA?")
    dificuldades = st.text_area("13. quais são as suas dificuldades ou receios ao usar IA?")
    submitted = st.form_submit_button("Enviar")

# --- PROCESSAMENTO ---
if submitted:
    if any(len(x.strip()) < 10 for x in [opiniao_ia, ferramentas_ia, uso_ia, setores]):
        st.error("Por favor, responda com pelo menos 10 caracteres nas perguntas 6 a 11.")
    else:
        prompt = (
            f"Olá {nome}, bom saber que você tem {idade}, e é de {cidade}, {estado}, {pais_nome}. "
            f"e que a sua escolaridade é do nível de: {escolaridade}. e que sua relação com IA: {relacao_ia}. "
            f"e que pensa assim: {opiniao_ia}. Importante saber que você já usou essas ferramentas: {ferramentas_ia} , muito interessante e impressionante, tenho que admitir. Uso: {uso_ia}. "
            f"Bom saber que você usa com essa frequência: {frequencia_uso}. e que se sente: {autonomia} usando ia. e que trabalha com esse(s) setor(es): {setores}. "
            f"Muito interessante saber que você aprende: {aprendizado} assim. Uma pena que tneha essas dificuldades: {dificuldades}."
        )

        nivel = avaliar_nivel_ia(relacao_ia, ferramentas_ia, uso_ia, frequencia_uso, autonomia, setores, escolaridade)
        st.info(f"Nível estimado de familiaridade com IA: **{nivel}%**")

        idioma = idiomas_por_pais.get(pais_codigo, "english")

        with st.spinner("Aguardando resposta da IA..."):
            resposta = gerar_resposta(prompt, idioma)
            st.success("Diagnóstico da IA:")
            st.write(resposta)

            st.markdown("---")
            st.markdown("### 📚 Recomendações de Cursos e Ferramentas")
            st.markdown("- **Cursos:** [IA no Google](https://cloudskillsboost.google/), [Microsoft IA](https://learn.microsoft.com/pt-br/training/paths/introduction-artificial-intelligence/), [Alura IA](https://www.alura.com.br/)")
            st.markdown("- **Ferramentas recomendadas:** ChatGPT, Copilot, Notion AI, Fireflies, Perplexity AI, Canva com IA")
