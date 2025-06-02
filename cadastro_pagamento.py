import sqlite3
import streamlit as st
import pandas as pd
from datetime import datetime

def conectar_banco():
    conn = sqlite3.connect("banco_academia.db", check_same_thread=False)
    cursor = conn.cursor()

    return conn, cursor

import streamlit as st
import pandas as pd

def cadastar_pagamento():
    conn, cursor = conectar_banco()

    # Carrega os dados iniciais
    df_nomes_cliente = pd.read_sql_query(
        "SELECT id_cliente, nome_clientes FROM clientes ORDER BY nome_clientes", 
        conn
    )

    # Se ainda não estiver na sessão, inicializa
    if "cliente_selecionado" not in st.session_state:
        st.session_state.cliente_selecionado = df_nomes_cliente["nome_clientes"].iloc[0]

    with st.form("form_cadastrar_pagamento"):
        # Selectbox de clientes (reativo)
        cliente_escolhido = st.selectbox(
            "Cliente", 
            df_nomes_cliente["nome_clientes"],
            key="cliente_selectbox",
            index=df_nomes_cliente[df_nomes_cliente["nome_clientes"] == st.session_state.cliente_selecionado].index[0],
            on_change=lambda: atualizar_plano(conn, df_nomes_cliente)  # Atualiza o plano ao mudar
        )

        # Obtém o ID do cliente selecionado
        id_cliente = df_nomes_cliente.loc[
            df_nomes_cliente["nome_clientes"] == st.session_state.cliente_selecionado,
            "id_cliente"
        ].values[0]

        # Busca o plano do cliente
        df_plano = pd.read_sql_query(
            f"""
            SELECT p.nome_planos 
            FROM clientes c
            JOIN planos p ON p.id_plano = c.fk_plano_id
            WHERE c.id_cliente = {id_cliente}
            """,
            conn
        )

        # Exibe o plano (atualizado automaticamente)
        if not df_plano.empty:
            plano_escolhido = st.text_input(
                "Plano",
                value=df_plano["nome_planos"].iloc[0],
                disabled=True
            )
        else:
            st.warning("Cliente sem plano vinculado")

        data_pagamento = st.date_input("Data Pagamento").strftime("%Y/%m/%d")
        enviar = st.form_submit_button("Cadastrar")

def atualizar_plano(conn, df_nomes_cliente):
    """Atualiza o cliente selecionado na sessão."""
    st.session_state.cliente_selecionado = st.session_state.cliente_selectbox

if __name__ == "__main__":
    cadastar_pagamento()