import json
import pandas as pd
import requests
import streamlit as st

# Configurações
OLLAMA_URL = "htts://localhost:11434/api/generate"
MODELO = "gpt-oss" # Certifique-se que esse é o modelo instalado na sua máquina



# Carregando Dados
perfil = json.load(open('./data/perfil_investidor.json'))
transacoes = pd.read_csv('./data/transacoes.csv')
historico = pd.read_csv('./data/historico_atendimento.csv')
produtos = json.load(open('./data/produtos_financeiros.json'))

# Montando Contexto
contexto:f"""
CLIENTE: {perfil['nome']}, {perfil['idade']} anos, {perfil['perfil_investidor']}
OBJETIVO: {perfil['objetivo_principal']}
PATRIMÔNIO: R$ {perfil['patrimonio_total']}
RESERVA: R$ {perfil['reserva_emergencia_atual']}

TRANSAÇÕES RECENTES:
{transacoes.to_string(index=False)}

ATENDIMENTO ANTERIORES:
{historico.to_string(index=False)}

PRODUTOS DISPONÍVEIS:
{json.dumps(produtos, indent=2, ensure_ascii=False)}

"""

#Sysytem Prompt
SYSTEM_PROMPT = """Você é o Duca, um educador financeiro didático.

OBJETIVO:
Ensinar conceitos de finanças pessoais de forma simples, usando os dados do cliente como exemplos práticos para facilitar o aprendizado.

REGRAS:
1. NUNCA recomende investimentos específicos, apenas explique como os produtos funcionam.
2. JAMAIS responda a perguntas fora do tema de ensino de finanças pessoais. Quando ocorrer, responda lembrando seu papel de educaador fincanceiro
3. Use os dados fornecidos no contexto (perfil, transações e metas) para dar exemplos reais.
4. Linguagem simples, como se explicasse pra um amigo.
5. Se não houver dados suficientes, admita e explique o conceito teórico.
6. Responda de forma sucinta e direta, com no máximo 3 parágrafos 
"""

# Chamando Ollama
def perguntas(msg):
  prompt=f"""
  {SYSTEM_PROMPT}

  Contexto do Cliente:
  {contexto}

  Perguntas: {msg}
  """
  r = requests.post(OLLAMA_URL, json={'model': MODELO, 'prompt': prompt, 'stream': False})
  return r.json()['response']

# Interface
st.title("Duca, seu Educador Financeiro")

if pergunta := st.chat_input("Sua dúvida sobre finanças... "):
  st.chat_massage("user").write(pergunta)
  with st.spinner("Pensando..."):
    st.chat_massage("assistant").write(perguntar(pergunta))
