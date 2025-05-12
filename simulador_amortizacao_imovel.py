# simulador_amortizacao_imovel.py

import streamlit as st
import pandas as pd

# -------------------------------
# Funções de cálculo (modularizadas)
# -------------------------------

def saldo_devedor_corrigido(saldo_devedor, incc_mensal, prazo):
    taxa = (1 + incc_mensal / 100) ** prazo
    return saldo_devedor * taxa

def itbi_registro(ap_vlr, itbi_reg_pct):
    return ap_vlr * itbi_reg_pct / 100

def saldo_corrigido_total(saldo_corrigido, itbi_reg):
    return saldo_corrigido + itbi_reg

def valor_investido_futuro(saldo_devedor, investimento_pct, prazo):
    taxa = (1 + investimento_pct / 100) ** prazo
    return saldo_devedor * taxa

def economia(saldo_total, investido_futuro):
    return saldo_total - investido_futuro

# -------------------------------
# Validação
# -------------------------------
def validar_positivo(valor, nome):
    if valor <= 0:
        st.warning(f"O campo '{nome}' deve ser maior que zero!")
        st.stop()

def validar_positivo_ou_zero(valor, nome):
    if valor < 0:
        st.warning(f"O campo '{nome}' não pode ser negativo!")
        st.stop()

# ----------------------------------------
# Interface - Streamlit Web App
# ----------------------------------------

st.set_page_config(page_title="Simulador Repasse", layout="centered")
st.title("Simulador de Amortização")

st.markdown("""
*Preencha os campos abaixo e visualize o impacto financeiro de amortizar o saldo devedor versus investir!*
""")

# -------------------------------
# Entradas (Usuário)
# -------------------------------

st.header("Parâmetros da simulação")

col1, col2 = st.columns(2)
with col1:
    avaliacao_imovel = st.number_input("Avaliação do imóvel (R$)", min_value=1.0, value=300000.00, step=1000.0, format="%.2f")
    saldo_devedor = st.number_input("Saldo devedor atual (R$)", min_value=1.0, value=100000.00, step=1000.0, format="%.2f")
    incc = st.number_input("INCC mensal (%)", min_value=0.01, value=0.63, step=0.01, format="%.2f")
with col2:
    rendimento = st.number_input("Rendimento do investimento (%)", min_value=0.01, value=0.8, step=0.01, format="%.2f")
    itbi_reg = st.number_input("ITBI + Registro (%)", min_value=0.01, value=3.00, step=0.1, format="%.2f")
    prazo = st.number_input("Prazo da simulação (meses)", min_value=1, value=1, step=1)

# Validação
validar_positivo(avaliacao_imovel, "Avaliação do imóvel")
validar_positivo(saldo_devedor, "Saldo devedor")
validar_positivo(incc, "INCC mensal")
validar_positivo(rendimento, "Rendimento investimento")
validar_positivo(itbi_reg, "ITBI + Registro")
validar_positivo(prazo, "Prazo (meses)")

# -------------------------------
# Processamento dos dados (Cálculo)
# -------------------------------

sd_corrigido = saldo_devedor_corrigido(saldo_devedor, incc, prazo)
itbi_reg_apx = itbi_registro(avaliacao_imovel, itbi_reg)
sd_total = saldo_corrigido_total(sd_corrigido, itbi_reg_apx)
vlr_inv_futuro = valor_investido_futuro(saldo_devedor, rendimento, prazo)
economia_cliente = economia(sd_total, vlr_inv_futuro)

# -------------------------------
# Saídas (Resultados Calculados)
# -------------------------------

st.subheader("Resultados da Simulação")
st.markdown("---")

def format_real(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

col1, col2 = st.columns(2)
with col1:
    st.markdown("**Saldo devedor corrigido:**")
    st.info(format_real(sd_corrigido))
    st.markdown("**ITBI + Registro (aprox):**")
    st.info(format_real(itbi_reg_apx))
    st.markdown("**Saldo corrigido + ITBI + reg.:**")
    st.success(format_real(sd_total))
with col2:
    st.markdown("**Valor investido futuro:**")
    st.info(format_real(vlr_inv_futuro))
    st.markdown("**Economia de:**")
    if economia_cliente > 0:
        st.success(format_real(economia_cliente))
    else:
        st.warning(format_real(economia_cliente) + " (Desfavorável: Avaliar a quitação)")

st.markdown("---")

# -------------------------------
# Comparação de múltiplos cenários (opcional)
# -------------------------------
st.header("Comparação de múltiplos cenários (opcional)")
n_sim = st.number_input("Número de simulações/comparações", min_value=1, max_value=5, value=1, step=1)
cenarios = []

if n_sim > 1:
    for i in range(int(n_sim)):
        st.markdown(f"### Cenário {i+1}")
        with st.expander(f"Editar Cenário {i+1}", expanded=(i==0)):
            col1, col2 = st.columns(2)
            with col1:
                av = st.number_input(f"Avaliação imóvel (R$) [{i+1}]", min_value=1.0, value=avaliacao_imovel, step=1000.0, format="%.2f", key=f"av{i}")
                sd = st.number_input(f"Saldo devedor (R$) [{i+1}]", min_value=1.0, value=saldo_devedor, step=1000.0, format="%.2f", key=f"sd{i}")
                inc = st.number_input(f"INCC mensal (%) [{i+1}]", min_value=0.01, value=incc, step=0.1, format="%.2f", key=f"inc{i}")
            with col2:
                rend = st.number_input(f"Rendimento Invest. (%) [{i+1}]", min_value=0.01, value=rendimento, step=0.1, format="%.2f", key=f"rend{i}")
                ir = st.number_input(f"ITBI+Reg. (%) [{i+1}]", min_value=0.01, value=itbi_reg, step=0.01, format="%.2f", key=f"ir{i}")
                pr = st.number_input(f"Prazo (meses) [{i+1}]", min_value=1, value=prazo, step=1, key=f"pr{i}")

        sdc = saldo_devedor_corrigido(sd, inc, pr)
        itbir = itbi_registro(av, ir)
        sdt = saldo_corrigido_total(sdc, itbir)
        vlfut = valor_investido_futuro(sd, rend, pr)
        econ = economia(sdt, vlfut)
        cenarios.append({
            "Saldo devedor final": sdc,
            "ITBI+Registro": itbir,
            "Saldo corrigido + taxas": sdt,
            "Valor investido futuro": vlfut,
            "Economia": econ
        })

    df = pd.DataFrame(cenarios)
    df.index = [f"Cenário {i+1}" for i in range(len(cenarios))]
    df = df.style.format(format_real)
    st.dataframe(df)

# -------------------------------
# Documentação breve de uso
# -------------------------------

st.markdown("---")
st.subheader("Documentação rápida de uso")
st.markdown("""
1. **Preencha os campos dos parâmetros da simulação (valores atuais, taxas e prazos).**
2. **Veja instantaneamente os resultados da simulação.**
3. **Para comparar cenários, aumente o número de simulações e edite cada cenário separadamente.**
4. **Todos os campos aceitam apenas valores positivos.**
5. **Use ponto para decimais na entrada; os resultados são exibidos no formato brasileiro (1.000.000,00).**
****
""")
