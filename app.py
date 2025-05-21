import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Comparador de CPK - Speedmax", layout="wide")
st.markdown("""
    <style>
    .main {background-color: #f8f4ff;}
    .stApp {font-family: 'Arial'; color: #2e1a47;}
    </style>
""", unsafe_allow_html=True)

# LOGO
st.image("https://uploaddeimagens.com.br/images/004/789/134/full/speedmax-logo.png", width=180)

# TÍTULO
st.title("🧮 Comparador de CPK - Speedmax")
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
        nome = st.text_input(f"Marca - Concorrente {i}", key=f"nome_{i}")
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
if marca and modelo and valor_unitario > 0 and km_rodado > 0:
    st.subheader("📊 Resultados do CPK")
    cpk_base = valor_unitario / km_rodado

    data = pd.DataFrame()
    data = data.append(
        {"Marca": f"{marca} ({modelo})", "Valor": valor_unitario, "KM": km_rodado, "CPK": cpk_base},
        ignore_index=True
    )

    for c in concorrentes:
        cpk = c["Valor"] / c["KM"]
        data = data.append(
            {"Marca": c["Marca"], "Valor": c["Valor"], "KM": c["KM"], "CPK": cpk},
            ignore_index=True
        )

    data = data.sort_values("CPK")
    menor_cpk = data.iloc[0]["CPK"]
    economia_anual = []
    economia_5anos = []

    for _, row in data.iterrows():
        cpk = row["CPK"]
        total_ano = cpk * 12 * quantidade_pneus
        total_5anos = cpk * 12 * 5 * quantidade_pneus
        economia_anual.append(total_ano)
        economia_5anos.append(total_5anos)

    data["Economia em 12 meses (R$)"] = economia_anual
    data["Economia em 5 anos (R$)"] = economia_5anos

    # GRÁFICO DE BARRAS COM PORCENTAGEM
    st.markdown("### 📈 Gráfico Comparativo de CPK")
    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.bar(data["Marca"], data["CPK"], color=["purple"] + ["gray"]*(len(data)-1))

    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + 0.002, f'{yval:.4f}', ha='center', va='bottom')

    ax.set_ylabel("CPK (R$/km)")
    ax.set_title("Comparativo de CPK entre marcas")
    st.pyplot(fig)

    # TABELA FINAL
    st.markdown("### 📋 Tabela de Resultados")
    st.dataframe(data.reset_index(drop=True), use_container_width=True)
