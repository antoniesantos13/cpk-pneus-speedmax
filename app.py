import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configurações da página
st.set_page_config(page_title="Comparador de CPK - Speedmax", layout="wide")
st.markdown("""
    <style>
    .main {background-color: #f8f4ff;}
    .stApp {font-family: 'Arial'; color: #2e1a47;}
    </style>
""", unsafe_allow_html=True)

# Logo e Título
st.image("https://uploaddeimagens.com.br/images/004/789/134/full/speedmax-logo.png", width=200)
st.title("🛞 Comparador de CPK - Speedmax")

st.markdown("Preencha os dados abaixo para comparar sua marca com concorrentes e mostrar o menor custo por km da frota.")

# Dados do Veículo
st.header("🚗 Tipo de Veículo")
tipos_veiculo = {
    "Caminhão Toco": 6,
    "Caminhão Truck": 10,
    "Carreta Toco": 18,
    "Carreta Traçada": 22,
    "Bitrem": 34,
    "Treminhão": 42
}
veiculo = st.selectbox("Selecione o tipo de veículo:", list(tipos_veiculo.keys()))
qtde_pneus = tipos_veiculo[veiculo]
st.write(f"Este veículo utiliza **{qtde_pneus} pneus**.")

# Dados da sua marca
st.header("💼 Sua Marca")
marca = st.text_input("Marca do seu pneu")
modelo = st.text_input("Modelo do pneu")
valor_unitario = st.number_input("Valor unitário (R$)", min_value=100.0, step=10.0)
km_rodado = st.number_input("Média de KM rodado", min_value=1000, step=1000)

# Concorrentes dinâmicos
st.header("🏋️ Concorrentes")
concorrentes = []
qtd = st.number_input("Quantos concorrentes deseja comparar?", min_value=1, max_value=5, step=1)

for i in range(int(qtd)):
    with st.expander(f"Concorrente {i+1}"):
        nome = st.text_input(f"Marca Concorrente {i+1}", key=f"marca_{i}")
        modelo_conc = st.text_input(f"Modelo Concorrente {i+1}", key=f"modelo_{i}")
        preco = st.number_input(f"Preço Concorrente {i+1} (R$)", key=f"preco_{i}", min_value=100.0)
        km = st.number_input(f"KM rodado Concorrente {i+1}", key=f"km_{i}", min_value=1000)

        if nome:
            concorrentes.append({
                "Marca": nome,
                "Modelo": modelo_conc,
                "Valor": preco,
                "KM": km
            })

# Cálculo do CPK
def calcular_cpk(valor, km):
    return valor / km if km > 0 else 0

if marca and modelo and valor_unitario > 0 and km_rodado > 0:
    st.subheader("📊 Resultados do CPK")
    dados = []
    cpk_sua_marca = calcular_cpk(valor_unitario, km_rodado)
    dados.append({"Marca": f"{marca} ({modelo})", "CPK": cpk_sua_marca})

    for c in concorrentes:
        cpk_conc = calcular_cpk(c["Valor"], c["KM"])
        dados.append({"Marca": f"{c['Marca']} ({c['Modelo']})", "CPK": cpk_conc})

    df = pd.DataFrame(dados)
    df = df.sort_values(by="CPK")
    st.dataframe(df, use_container_width=True)

    # Economia
    menor_cpk = df.iloc[0]
    if menor_cpk["Marca"] != f"{marca} ({modelo})":
        economia = ((cpk_sua_marca - menor_cpk["CPK"]) / menor_cpk["CPK"]) * 100
        st.warning(f"Seu CPK é **{economia:.1f}%** mais caro que o da marca {menor_cpk['Marca']}")
    else:
        st.success("Parabéns! Sua marca tem o menor CPK da comparação!")

    # Gráfico
    fig, ax = plt.subplots()
    ax.bar(df["Marca"], df["CPK"])
    ax.set_ylabel("CPK (R$/km)")
    ax.set_title("Comparativo de CPK por Marca")
    st.pyplot(fig)

# Rodapé personalizado
st.markdown("""
---
**Consultor de Vendas:** Antônio Dos Santos Souza  
**E-mail:** antonio.souza@cantustore.com.br  
""")
