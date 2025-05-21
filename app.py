import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Comparador de CPK - Speedmax", layout="wide")

# ESTILO PERSONALIZADO
st.markdown("""
    <style>
        .main { background-color: #f8f4ff; }
        .stApp { font-family: 'Arial'; color: #2e1a47; }
    </style>
""", unsafe_allow_html=True)

# LOGO
st.image("https://uploaddeimagens.com.br/images/004/789/134/full/speedmax-logo.png", width=200)
st.title("🛞 Comparador de CPK - Speedmax")

st.markdown("Preencha os dados para comparar a performance do pneu Speedmax com os concorrentes e visualizar a economia gerada.")

# CONTATO
st.markdown("""
**Consultor de Vendas:** Antônio Dos Santos Souza  
📧 antonio.souza@cantustore.com.br  
""")

# TIPO DE VEÍCULO
st.header("🚚 Tipo de Veículo")
veiculo = st.selectbox("Selecione o tipo de veículo:", [
    "Toco (6 pneus)", "Truck (10 pneus)", "Carreta 3 eixos (22 pneus)",
    "Bitrem (34 pneus)", "Rodotrem (38 pneus)", "Outro"
])
qtde_pneus = {
    "Toco (6 pneus)": 6,
    "Truck (10 pneus)": 10,
    "Carreta 3 eixos (22 pneus)": 22,
    "Bitrem (34 pneus)": 34,
    "Rodotrem (38 pneus)": 38,
    "Outro": st.number_input("Informe manualmente a quantidade de pneus:", min_value=1, value=6)
}[veiculo]

# DADOS DO PNEU SPEEDMAX
st.header("🔧 Dados do Pneu Speedmax")
marca_modelo = st.text_input("Marca/Modelo", value="Speedmax Prime")
valor = st.number_input("Valor do pneu (R$)", min_value=100.0, step=10.0)
km = st.number_input("Média de km rodado", min_value=1000, max_value=500000, step=1000)
cpk_base = valor / km

# DADOS DOS CONCORRENTES
st.header("🏁 Concorrentes")
concorrentes = []

for i in range(1, 5):
    with st.expander(f"Concorrente {i}"):
        nome = st.text_input(f"Marca/Modelo concorrente {i}", key=f"nome_{i}")
        preco = st.number_input(f"Valor do pneu concorrente {i} (R$)", min_value=100.0, step=10.0, key=f"preco_{i}")
        km_rodado = st.number_input(f"Km médio concorrente {i}", min_value=1000, step=1000, key=f"km_{i}")
        if nome:
            cpk = preco / km_rodado
            concorrentes.append({"Marca": nome, "CPK": cpk})

# CALCULAR ECONOMIA
if concorrentes:
    data = pd.DataFrame(concorrentes)
    data = data.append({"Marca": marca_modelo, "CPK": cpk_base}, ignore_index=True)
    data = data.sort_values("CPK")
    melhor_cpk = data.iloc[0]["CPK"]
    economia_percent = ((max(data["CPK"]) - melhor_cpk) / max(data["CPK"])) * 100
    economia_mensal = (max(data["CPK"]) - melhor_cpk) * qtde_pneus * 10000
    economia_anual = economia_mensal * 12
    economia_5_anos = economia_anual * 5

    st.subheader("📊 Comparativo de CPK (R$/km)")
    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.bar(data["Marca"], data["CPK"], color=[
        '#6A0DAD' if marca == marca_modelo else 'gray' for marca in data["Marca"]
    ])
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height, f'{height:.2f}', ha='center', va='bottom')
    ax.set_ylabel("Custo por Km (R$)")
    st.pyplot(fig)

    st.success(f"✅ Economia de até **{economia_percent:.1f}%** ao escolher o pneu com menor CPK.")
    st.info(f"""
    💰 **Economia estimada:**
    - Mensal: R$ {economia_mensal:,.2f}
    - Anual: R$ {economia_anual:,.2f}
    - Em 5 anos: R$ {economia_5_anos:,.2f}
    """)

else:
    st.warning("Adicione ao menos 1 concorrente para visualizar o gráfico e os resultados.")
