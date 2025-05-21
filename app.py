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

# LOGO E TÍTULO
st.image("https://uploaddeimagens.com.br/images/004/789/134/full/speedmax-logo.png", width=200)
st.title("📊 Comparador de CPK - Speedmax")

st.markdown("Preencha os dados para comparar a performance do pneu Speedmax com os concorrentes e visualizar a economia gerada.")

# CONTATO
st.markdown("""
**Consultor de Vendas:** Antônio Dos Santos Souza
📧 antonio.souza@cantustore.com.br
""")

# DADOS DA SUA MARCA
st.header("📋 Sua Marca")
marca = st.text_input("Marca do seu pneu")
modelo = st.text_input("Modelo do pneu")
valor_unitario = st.number_input("Valor unitário (R$)", min_value=100.0, step=10.0)
km_rodado = st.number_input("Média de KM rodado", min_value=1000, step=1000)
quantidade_pneus = st.number_input("Quantidade de pneus na frota", min_value=1, step=1)

# DADOS DOS CONCORRENTES
st.header("🏎️ Concorrentes")
concorrentes = []
for i in range(1, 5):
    with st.expander(f"Concorrente {i}"):
        nome = st.text_input(f"Marca - Concorrente {i}", key=f"marca_{i}")
        modelo_conc = st.text_input(f"Modelo - Concorrente {i}", key=f"modelo_{i}")
        preco = st.number_input(f"Valor (R$) - Concorrente {i}", min_value=100.0, step=10.0, key=f"preco_{i}")
        km = st.number_input(f"KM rodado - Concorrente {i}", min_value=1000, step=1000, key=f"km_{i}")

        if nome and modelo_conc and preco > 0 and km > 0:
            concorrentes.append({
                "Marca": f"{nome} ({modelo_conc})",
                "Valor": preco,
                "KM": km
            })

# RESULTADOS
st.header("📊 Resultados do CPK")
if marca and modelo and valor_unitario > 0 and km_rodado > 0:
    cpk_base = valor_unitario / km_rodado
    data = pd.DataFrame()
    data = pd.concat([
        data,
        pd.DataFrame([{
            "Marca": f"{marca} ({modelo})",
            "Valor": valor_unitario,
            "KM": km_rodado,
            "CPK": cpk_base
        }])
    ], ignore_index=True)

    for c in concorrentes:
        data = pd.concat([
            data,
            pd.DataFrame([{
                "Marca": c["Marca"],
                "Valor": c["Valor"],
                "KM": c["KM"],
                "CPK": c["Valor"] / c["KM"]
            }])
        ], ignore_index=True)

    data = data.sort_values("CPK")

    # Gráfico de barras com porcentagem
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(data["Marca"], data["CPK"], color=["#6A0DAD"] + ["#FFBB33"]*(len(data)-1))
    ax.set_ylabel("CPK (R$/km)")
    ax.set_title("Comparativo de CPK entre marcas")
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f"{height:.2f}",
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom')
    st.pyplot(fig)

    # Economia
    melhor_cpk = data["CPK"].min()
    economia = (data["CPK"] - melhor_cpk) * quantidade_pneus * 12
    economia_5anos = economia * 5
    data["Economia (12 meses)"] = economia.apply(lambda x: f"R$ {x:,.2f}")
    data["Economia (5 anos)"] = economia_5anos.apply(lambda x: f"R$ {x:,.2f}")

    st.dataframe(data.reset_index(drop=True))
