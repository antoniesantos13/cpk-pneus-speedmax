# Novo app.py com todas as melhorias + quantidade de pneus e economia

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Comparador de CPK - Speedmax", layout="wide")

# ESTILO PERSONALIZADO
st.markdown("""
    <style>
        .main {background-color: #f8f4ff;}
        .stApp {font-family: 'Arial'; color: #2e1a47;}
    </style>
""", unsafe_allow_html=True)

# LOGO
st.image("https://uploaddeimagens.com.br/images/004/789/134/full/speedmax-logo.png", width=200)
st.title("🚾 Comparador de CPK - Speedmax")

st.markdown("Preencha os dados para comparar a performance do pneu Speedmax com os concorrentes e visualizar a economia gerada.")

# CONTATO
st.markdown("""
**Consultor de Vendas:** Antônio Dos Santos Souza  
📧 antonio.souza@cantustore.com.br
""")

# SUA MARCA
st.header("🧾 Sua Marca")
marca = st.text_input("Marca do seu pneu")
modelo = st.text_input("Modelo do pneu")
valor_unitario = st.number_input("Valor unitário (R$)", min_value=100.0, step=10.0)
km_rodado = st.number_input("Média de KM rodado", min_value=1000, step=1000)
qtd_pneus = st.number_input("Quantidade de pneus na frota", min_value=1, step=1)

# CONCORRENTES
st.header("🏎️ Concorrentes")
concorrentes = []
for i in range(1, 5):
    with st.expander(f"Concorrente {i}"):
        nome = st.text_input(f"Marca - Concorrente {i}", key=f"nome_{i}")
        modelo_conc = st.text_input(f"Modelo - Concorrente {i}", key=f"modelo_{i}")
        preco = st.number_input(f"Valor (R$) - Concorrente {i}", min_value=100.0, step=10.0, key=f"preco_{i}")
        km = st.number_input(f"KM rodado - Concorrente {i}", min_value=1000, step=1000, key=f"km_{i}")
        if nome:
            cpk = preco / km if km > 0 else 0
            concorrentes.append({"Marca": f"{nome} ({modelo_conc})", "CPK": cpk})

# CALCULAR CPK
if marca and modelo and valor_unitario > 0 and km_rodado > 0:
    st.subheader("📊 Resultados do CPK")
    cpk_base = valor_unitario / km_rodado
    data = pd.DataFrame(concorrentes)
    data = data.append({"Marca": f"{marca} ({modelo})", "CPK": cpk_base}, ignore_index=True)
    data = data.sort_values("CPK")

    # Gráfico
    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.barh(data["Marca"], data["CPK"], color=["#800080" if m.startswith(marca) else None for m in data["Marca"]])
    for bar in bars:
        ax.text(bar.get_width(), bar.get_y() + bar.get_height()/2, f'{bar.get_width():.3f}', va='center')
    ax.set_xlabel("CPK (R$/km)")
    ax.set_title("Comparativo de CPK")
    st.pyplot(fig)

    # Economia
    melhor_cpk = data["CPK"].min()
    economia_unitaria = (cpk_base - melhor_cpk) * km_rodado
    economia_total_12m = economia_unitaria * qtd_pneus * 12
    economia_total_5a = economia_total_12m * 5
    st.success(f"💰 Economia por pneu em 12 meses: R$ {economia_unitaria*12:,.2f}")
    st.success(f"💰 Economia total em 12 meses para {qtd_pneus} pneus: R$ {economia_total_12m:,.2f}")
    st.success(f"💰 Economia total em 5 anos: R$ {economia_total_5a:,.2f}")
