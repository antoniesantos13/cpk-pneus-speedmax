import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Comparador de CPK", layout="wide")
st.title("🛞 Comparador de CPK - Custo por Km")

st.markdown("Preencha os dados abaixo para comparar sua marca com até 4 concorrentes e mostrar o menor custo por km da frota.")

st.header("🔍 Dados de Referência")

km_rodado = st.number_input("Média de km por pneu novo (sem recapagem)", min_value=1000, max_value=500000, step=1000)
valor_unitario = st.number_input("Valor do pneu novo (R$)", min_value=100.0, step=10.0)
num_recapagens = st.selectbox("Número de recapagens possíveis", [0, 1, 2, 3])
custo_recapagem = st.number_input("Custo médio da recapagem (R$)", min_value=0.0, step=10.0)
km_recapagem = st.number_input("Média de km por recapagem", min_value=1000, max_value=500000, step=1000)

st.header("🏁 Concorrentes")

concorrentes = []

for i in range(1, 5):
    with st.expander(f"Concorrente {i}"):
        nome = st.text_input(f"Nome do Concorrente {i}", key=f"nome_{i}")
        preco = st.number_input(f"Valor do pneu - Concorrente {i} (R$)", min_value=100.0, step=10.0, key=f"preco_{i}")
        km = st.number_input(f"Km rodado com pneu novo - Concorrente {i}", min_value=1000, step=1000, key=f"km_{i}")
        recap = st.selectbox(f"Nº de recapagens - Concorrente {i}", [0, 1, 2, 3], key=f"recap_{i}")
        custo_recap = st.number_input(f"Custo médio recapagem - Concorrente {i} (R$)", min_value=0.0, step=10.0, key=f"custo_recap_{i}")
        km_recap = st.number_input(f"Km médio por recapagem - Concorrente {i}", min_value=1000, step=1000, key=f"km_recap_{i}")

        if nome:
            concorrentes.append({
                "Marca": nome,
                "Valor": preco,
                "Km_Novo": km,
                "Recap": recap,
                "Custo_Recap": custo_recap,
                "Km_Recap": km_recap
            })
