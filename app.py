import streamlit as st
import requests

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="Diagnóstico de IA - RH", layout="centered")
st.title("📊 PRISCILA AI")
st.markdown("Preencha o formulário abaixo para avaliar seu nível de conhecimento e uso de IA:")

# --- CHAVE DE API ---
api_key = st.secrets["huggingface"]["api_key"]

# --- FUNÇÃO DE REQUISIÇÃO A IA ---
def gerar_resposta(prompt):
    url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.post(url, headers=headers, json={"inputs": prompt}, timeout=30)
    if response.status_code == 200:
        try:
            texto = response.json()[0].get("generated_text", "")
            resposta_final = texto.split("<|assistant|>")[-1].strip()
            return resposta_final
        except Exception as e:
            return f"Erro ao interpretar resposta: {e}"
    return f"Erro: {response.status_code} – {response.text}"

# --- FUNÇÃO DE AVALIAÇÃO DE NÍVEL ---
def avaliar_nivel_ia(relacao, ferramentas, uso, freq, autonomia, setores, escolaridade):
    nota = 0

    pesos_relacao = {
        "Nunca usei": 0,
        "Tenho receio": 10,
        "Não sei muito": 20,
        "Gosto, mas não sei usar": 30,
        "Boa": 60,
        "Uso com frequência": 80
    }
    nota += pesos_relacao.get(relacao, 0)

    ferramentas = [f.strip() for f in ferramentas.lower().split(",") if len(f.strip()) >= 3]
    nota += min(len(ferramentas) * 5, 20)

    if len(uso.strip()) > 100:
        nota += 20
    elif len(uso.strip()) > 50:
        nota += 10
    elif len(uso.strip()) > 10:
        nota += 5

    pesos_freq = {"Nunca": 0, "Raramente": 5, "Mensalmente": 10, "Semanalmente": 15, "Diariamente": 20}
    nota += pesos_freq.get(freq, 0)

    pesos_auto = {
        "Preciso de ajuda para tudo": 0,
        "Consigo usar com orientação": 10,
        "Aprendo com tutoriais": 20,
        "Sou autodidata e crio soluções": 30
    }
    nota += pesos_auto.get(autonomia, 0)

    setores_usados = [s.strip() for s in setores.lower().split(",") if len(s) >= 3]
    nota += min(len(setores_usados) * 2, 10)

    pesos_escolaridade = {
        "Ensino fundamental": 0,
        "Ensino médio": 10,
        "Faculdade ou outros": 20
    }
    nota += pesos_escolaridade.get(escolaridade, 0)

    return min(nota, 100)

# --- FORMULÁRIO ---
with st.form(key="formulario"):
    nome = st.text_input("1. Qual o seu nome completo?")
    idade = st.selectbox("2. Qual a sua idade?", ["Menos de 18", "18 a 25", "26 a 35", "36 a 45", "46 a 60", "Acima de 60"])
    local = st.text_input("3. De onde você é? (Cidade, estado ou região)")

    escolaridade = st.selectbox("4. Qual seu nível de escolaridade?", ["Ensino fundamental", "Ensino médio", "Faculdade ou outros"])

    relacao_ia = st.selectbox("5. Qual sua relação com as Inteligências Artificiais?",
                               ["Boa", "Não sei muito", "Gosto, mas não sei usar", "Tenho receio", "Nunca usei", "Uso com frequência"])

    opiniao_ia = st.text_area("6. O que você pensa sobre as Inteligências Artificiais?")
    ferramentas_ia = st.text_area("7. Quais ferramentas de IA você já usou? (ex: ChatGPT, Midjourney, Copilot, etc.)")
    uso_ia = st.text_area("8. Em que situações você já utilizou ou usaria uma IA?")

    frequencia_uso = st.selectbox("9. Com que frequência você utiliza ferramentas de IA?",
                                  ["Nunca", "Raramente", "Mensalmente", "Semanalmente", "Diariamente"])

    autonomia = st.selectbox("10. Como você descreveria sua autonomia com ferramentas de IA?",
                             ["Preciso de ajuda para tudo", "Consigo usar com orientação", "Aprendo com tutoriais", "Sou autodidata e crio soluções"])

    setores = st.text_area("11. Em quais áreas do seu trabalho você vê potencial para aplicar IA? (ex: atendimento, marketing, etc.)")
    aprendizado = st.text_area("12. Gostaria de aprender mais sobre IA? Como gostaria que fosse esse aprendizado?")
    dificuldades = st.text_area("13. Quais são as principais dificuldades que você enfrenta ou imagina ao usar IA?")

    submitted = st.form_submit_button("Enviar")

# --- PROCESSAMENTO ---
if submitted:
    campos = [opiniao_ia, ferramentas_ia, uso_ia, setores]
    erros = [i for i, campo in enumerate(campos, 6) if len(campo.strip()) < 10]

    if erros:
        for e in erros:
            st.error(f"A resposta da pergunta {e} deve ter pelo menos 10 caracteres.")
    else:
        prompt = (
            "<|system|>\nVocê é uma IA que ajuda pessoas a entender seu nível de familiaridade com inteligência artificial e recomenda formas de evoluir.\n"
            "<|user|>\n"
            f"Meu nome é {nome}, tenho {idade}, sou de {local}. Tenho escolaridade: {escolaridade}, relação com IA: {relacao_ia}. "
            f"Opinião sobre IA: {opiniao_ia}. Ferramentas usadas: {ferramentas_ia}. Uso de IA: {uso_ia}. "
            f"Frequência: {frequencia_uso}, autonomia: {autonomia}. Setores com potencial: {setores}. "
            f"Interesse em aprender: {aprendizado}. Dificuldades: {dificuldades}.\n"
            "<|assistant|>"
        )

        nivel = avaliar_nivel_ia(relacao_ia, ferramentas_ia, uso_ia, frequencia_uso, autonomia, setores, escolaridade)
        st.info(f"Nível estimado de familiaridade com IA: **{nivel}%**")

        with st.spinner("Aguardando resposta da IA..."):
            resposta = gerar_resposta(prompt)
            st.success("Diagnóstico da IA:")
            st.write(resposta)

            st.markdown("---")
            st.markdown("### 📚 Recomendações de Cursos e Ferramentas")
            st.markdown("- **Cursos:** [IA no Google](https://cloudskillsboost.google/), [Fundamentos de IA - Microsoft](https://learn.microsoft.com/pt-br/training/paths/introduction-artificial-intelligence/), [IA na Prática - Alura](https://www.alura.com.br/)")
            st.markdown("- **Ferramentas recomendadas:** ChatGPT, Copilot, Notion AI, Fireflies, Perplexity AI, Canva com IA")
