import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Comparador de CPK - Speedmax", layout="wide")
st.markdown(
    """
    <style>
        .main {background-color: #f8f4ff;}
        .stApp {font-family: 'Arial'; color: #2e1a47;}
    </style>
    """,
    unsafe_allow_html=True
)

# LOGO E TÍTULO
st.image("https://uploaddeimagens.com.br/images/004/789/134/full/speedmax-logo.png", width=200)
st.title("🪙 Comparador de CPK - Speedmax")
st.markdown("Preencha os dados para comparar a performance do pneu Speedmax com os concorrentes e visualizar a economia gerada.")

# CONTATO
st.markdown("""
**Consultor de Vendas:** Antônio Dos Santos Souza  
📧 antonio.souza@cantustore.com.br
""")

# SUA MARCA
st.header("🧾 Sua Marca")
marca = st.text_input("Marca do seu pneu", value="Speedmax")
modelo = st.text_input("Modelo do pneu", value="Venture Max S")
valor_unitario = st.number_input("Valor unitário (R$)", min_value=0.0, step=10.0)
km_rodado = st.number_input("Média de KM rodado", min_value=1000, step=1000)
qtd_pneus = st.number_input("Quantidade de pneus na frota", min_value=1, step=1)

# CONCORRENTES
st.header("🏎️ Concorrentes")
concorrentes = []
for i in range(1, 5):
    with st.expander(f"Concorrente {i}"):
        nome = st.text_input(f"Marca - Concorrente {i}", key=f"nome_{i}")
        modelo_conc = st.text_input(f"Modelo - Concorrente {i}", key=f"modelo_{i}")
        preco = st.number_input(f"Valor (R$) - Concorrente {i}", min_value=0.0, step=10.0, key=f"preco_{i}")
        km = st.number_input(f"KM rodado - Concorrente {i}", min_value=1000, step=1000, key=f"km_{i}")
        
        if nome and modelo_conc and preco > 0 and km > 0:
            concorrentes.append({
                "Marca": f"{nome} ({modelo_conc})",
                "Valor": preco,
                "KM": km
            })

# RESULTADOS
if marca and modelo and valor_unitario > 0 and km_rodado > 0 and qtd_pneus > 0:
    st.subheader("📊 Resultados do CPK")

    # Cálculo do CPK
    data = pd.DataFrame(concorrentes)
    cpk_base = valor_unitario / km_rodado
    data = data.append({"Marca": f"{marca} ({modelo})", "Valor": valor_unitario, "KM": km_rodado}, ignore_index=True)
    data["CPK"] = data["Valor"] / data["KM"]

    # Ordenar e destacar Speedmax
    data = data.sort_values(by="CPK")
    melhor_cpk = data["CPK"].min()
    cpk_marca = cpk_base
    economia_pneu = (cpk_marca - melhor_cpk) * -1
    economia_total = economia_pneu * qtd_pneus
    economia_anual = economia_total * 12
    economia_5anos = economia_total * 60
    economia_pct = (economia_pneu / cpk_marca) * 100 if cpk_marca != 0 else 0

    # Exibir economia
    st.markdown(f"### 💰 Economia estimada: R$ {economia_total:,.2f}/mês | R$ {economia_anual:,.2f}/ano | R$ {economia_5anos:,.2f} em 5 anos")
    st.markdown(f"🟪 Sua marca representa uma economia de **{economia_pct:.2f}%** comparado ao concorrente mais caro.")

    # Gráfico
    fig, ax = plt.subplots()
    cores = ["#4B0082" if marca.split()[0].lower() in m.lower() else "#ccc" for m in data["Marca"]]
    barras = ax.barh(data["Marca"], data["CPK"], color=cores)

    for i, v in enumerate(data["CPK"]):
        ax.text(v + 0.002, i, f"{v:.2f}", color='black', va='center', fontweight='bold')

    ax.set_xlabel("CPK (R$/km)")
    ax.set_title("Comparativo de CPK por Marca")
    st.pyplot(fig)
