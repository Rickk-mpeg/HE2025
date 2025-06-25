def identificar_perfil(respostas):
    idade = respostas[0].strip()
    local = respostas[1].strip()
    linguagem = respostas[2].strip()
    escolaridade = respostas[3].strip().capitalize()
    religiao = respostas[4].strip().capitalize()

    texto = " ".join(respostas).lower()
    nacionalidade = "Brasil"

    # Definir região + gírias
    if "rio" in local.lower():
        regiao = "Sudeste"
        girias = ["bater um rango", "rolê", "zueira", "trem", "rolê", "rolê"]
    elif any(p in texto for p in ["abestado","amofinado","azuretado","arretado","migué","fuzuê","cafuringa"]):
        regiao = "Nordeste"
        girias = ["abestado","amofinado","azuretado","arretado","migué","fuzuê"]
    elif any(p in texto for p in ["bah","guri","tchê","tri","tchê"]):
        regiao = "Sul"
        girias = ["tri","tchê","guri","bah","lagartear","cacetinho"]
    elif any(p in texto for p in ["uai","sô","trem"]):
        regiao = "Centro-Oeste / Minas"
        girias = ["uai","sô","perrengue","pé-de-boi","bitelo"]
    else:
        regiao = "Indefinida"
        girias = []

    estilo = f"Estilo local: use gírias como {', '.join(girias[:5])}..." if girias else "Sem gírias específicas detectadas."
    return idade, escolaridade, regiao, estilo, girias, nacionalidade, religiao


def gerar_prompt(idade, escolaridade, regiao, girias, nacionalidade, religiao):
    prompt = f"""
Haja como uma IA amigável e respeitosa, como se estivesse falando com um amigo usando as formas de falar do {nacionalidade}.
Você está conversando com uma pessoa que:
- Tem {idade} anos.
- Tem o nível de escolaridade: {escolaridade}.
- É da região: {regiao}.
- Professa a religião: {religiao}.
- Usa gírias como: {', '.join(girias) if girias else 'nenhuma gíria específica'}.
Adapte sua linguagem para refletir a forma de se comunicar da região, com empatia e leveza. Use as gírias de forma natural.
**Nunca desrespeite crenças, cultura ou costumes da pessoa.** Mantenha um tom positivo, inclusivo e acolhedor. Evite termos técnicos ou linguagem difícil, a não ser que a pessoa solicite.
Fale como um amigo dessa região, iniciando um papo descontraído com respeito à idade, escolaridade e crenças.
"""
    return prompt.strip()


# Questionário e execução
respostas = []
perguntas = [
    "1. Quantos anos você tem?",
    "2. De onde você é? (cidade/região)",
    "3. Como você costuma falar? (gírias, expressões)",
    "4. Qual seu nível de escolaridade? (ex: ensino médio, faculdade, mestrado...)",
    "5. Qual é sua religião?"
]
print("Responda com sinceridade:\n")
for q in perguntas:
    respostas.append(input(q + "\n> "))

idade, escolaridade, regiao, estilo, girias, nacionalidade, religiao = identificar_perfil(respostas)

print(f"\n🔍 Perfil detectado:\nIdade: {idade}\nEscolaridade: {escolaridade}\nRegião: {regiao}\nReligião: {religiao}\n{estilo}")

prompt = gerar_prompt(idade, escolaridade, regiao, girias, nacionalidade, religiao)
print("\n📋 Prompt final gerado:\n")
print(prompt)
