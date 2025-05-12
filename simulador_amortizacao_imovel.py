# simulador_amortizacao_imovel.py

import streamlit as st

# -------------------------------
# Funções de cálculo (modularizadas)
# -------------------------------

def saldo_devedor_corrigido(saldo_devedor, incc_anual, prazo):
    """
    Calcula o saldo devedor corrigido pelo INCC anual no período desejado.
    saldo_devedor: float, valor atual do saldo devedor
    incc_anual: float, percentual do INCC para os últimos 12 meses
    prazo: int, prazo em meses
    """
    taxa = (1 + incc_anual / 100) ** prazo
    return saldo_devedor * taxa

def itbi_registro(ap_vlr, itbi_reg_pct):
    """
    Calcula o valor aproximado do ITBI + Registro.
    ap_vlr: float, avaliação do imóvel
    itbi_reg_pct: float, percentagem de ITBI + Registro
    """
    return ap_vlr * itbi_reg_pct / 100

def saldo_corrigido_total(saldo_corrigido, itbi_reg):
    """
    Soma saldo devedor corrigido + ITBI e Registro.
    """
    return saldo_corrigido + itbi_reg

def valor_investido_futuro(saldo_devedor, investimento_pct, prazo):
    """
    Apura quanto renderia o saldo devedor, investido dia 1 pelo prazo definido.
    """
    taxa = (1 + investimento_pct / 100) ** prazo
    return saldo_devedor * taxa

def economia(saldo_total, investido_futuro):
    """
    Calcula a diferença favorável para o cliente.
    """
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

st.set_page_config(page_title="Simulador de Amortização de Saldo Devedor", layout="centered")
st.title("Simulador de Negociação de Amortização — Imóveis")

st.markdown(
    """
    *Preencha os campos abaixo com os dados do cliente e visualize o impacto financeiro de amortizar o saldo devedor versus investir!*
    """
)

# -------------------------------
# Entradas (Usuário)
# -------------------------------

st.header("Parâmetros da simulação")

col1, col2 = st.columns(2)
with col1:
    avaliacao_imovel = st.number_input("Avaliação do imóvel (R$)", min_value=1.0, value=500000.00, step=1000.0, format="%.2f")
    saldo_devedor = st.number_input("Saldo devedor atual (R$)", min_value=1.0, value=300000.00, step=1000.0, format="%.2f")
    incc = st.number_input("INCC anual (%)", min_value=0.01, value=4.5, step=0.1, format="%.2f")
with col2:
    rendimento = st.number_input("Rendimento do investimento (%)", min_value=0.01, value=9.0, step=0.1, format="%.2f")
    itbi_reg = st.number_input("ITBI + Registro (%)", min_value=0.01, value=3.50, step=0.01, format="%.2f")
    prazo = st.number_input("Prazo da simulação (meses)", min_value=1, value=24, step=1)

# Validação
validar_positivo(avaliacao_imovel, "Avaliação do imóvel")
validar_positivo(saldo_devedor, "Saldo devedor")
validar_positivo(incc, "INCC anual")
validar_positivo(rendimento, "Rendimento investimento")
validar_positivo(itbi_reg, "ITBI + Registro")
validar_positivo(prazo, "Prazo (meses)")

# -------------------------------
# Processamento dos dados (Cálculo)
# -------------------------------

# Campos calculados
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

col1, col2 = st.columns(2)
with col1:
    st.markdown("**Saldo devedor corrigido:**")
    st.info(f"R$ {sd_corrigido:,.2f}")
    st.markdown("**ITBI + Registro (aprox):**")
    st.info(f"R$ {itbi_reg_apx:,.2f}")
    st.markdown("**Saldo corrigido + ITBI + reg.:**")
    st.success(f"R$ {sd_total:,.2f}")
with col2:
    st.markdown("**Valor investido futuro:**")
    st.info(f"R$ {vlr_inv_futuro:,.2f}")
    st.markdown("**Economia de:**")
    if economia_cliente > 0:
        st.success(f"R$ {economia_cliente:,.2f}")
    else:
        st.warning(f"R$ {economia_cliente:,.2f} (Desfavorável: manter saldo devedor pode ser melhor!)")

st.markdown("---")

# -------------------------------
# Comparação de cenários simultâneos (Opcional)
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
                inc = st.number_input(f"INCC anual (%) [{i+1}]", min_value=0.01, value=incc, step=0.1, format="%.2f", key=f"inc{i}")
            with col2:
                rend = st.number_input(f"Rendimento Invest. (%) [{i+1}]", min_value=0.01, value=rendimento, step=0.1, format="%.2f", key=f"rend{i}")
                ir = st.number_input(f"ITBI+Reg. (%) [{i+1}]", min_value=0.01, value=itbi_reg, step=0.01, format="%.2f", key=f"ir{i}")
                pr = st.number_input(f"Prazo (meses) [{i+1}]", min_value=1, value=prazo, step=1, key=f"pr{i}")

        # Calcular cenário
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

    # Tabela comparativa
    import pandas as pd
    df = pd.DataFrame(cenarios)
    df.index = [f"Cenário {i+1}" for i in range(len(cenarios))]
    st.dataframe(df.style.format("R$ {:.2f}"))

# -------------------------------
# Exemplificação do uso/teste prático
# -------------------------------

st.header("Exemplo prático pré-preenchido")
st.markdown("""
**Simulação com os seguintes parâmetros:**
- Avaliação: R$ 500.000,00
- Saldo devedor: R$ 300.000,00
- INCC anual: 4,5%
- Rendimento investimento: 9%
- ITBI + Registro: 3,5%
- Prazo: 24 meses

**Resultado esperado:**
""")
ex_avaliacao = 500000
ex_saldo_dev = 300000
ex_incc = 4.5
ex_rendimento = 9.0
ex_itbi_reg = 3.5
ex_prazo = 24

ex_sd_corrigido = saldo_devedor_corrigido(ex_saldo_dev, ex_incc, ex_prazo)
ex_itbi_reg_apx = itbi_registro(ex_avaliacao, ex_itbi_reg)
ex_sd_total = saldo_corrigido_total(ex_sd_corrigido, ex_itbi_reg_apx)
ex_vlr_investido_futuro = valor_investido_futuro(ex_saldo_dev, ex_rendimento, ex_prazo)
ex_economia = economia(ex_sd_total, ex_vlr_investido_futuro)

st.markdown(f"""
- **Saldo devedor corrigido:** R$ {ex_sd_corrigido:,.2f}
- **ITBI + Registro (aprox):** R$ {ex_itbi_reg_apx:,.2f}
- **Saldo corrigido + ITBI + reg.:** R$ {ex_sd_total:,.2f}
- **Valor investido futuro:** R$ {ex_vlr_investido_futuro:,.2f}
- **Economia de:** R$ {ex_economia:,.2f}
""")

# -------------------------------
# Documentação breve de uso
# -------------------------------

st.markdown("---")
st.subheader("Documentação rápida de uso")
st.markdown("""
1. **Preencha os campos à esquerda (valores atuais, taxas e prazos).**
2. **Veja instantaneamente os resultados à direita, com destaque para eventuais economias ou desvantagens.**
3. **Para comparar cenários, aumente o número de simulações e edite cada cenário separadamente.**
4. **Todos os campos aceitam apenas valores positivos.**
5. **Suporte a vírgula ou ponto decimal (use ponto para decimais).**

**Necessita de suporte? Entre em contato com o time de TI.**
""")# Escreva o seu código aqui :-)
