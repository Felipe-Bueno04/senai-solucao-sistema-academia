import sqlite3
import streamlit as st
import pandas as pd
from datetime import datetime

def conectar_banco():
    conn = sqlite3.connect("banco_academia.db", check_same_thread=False)
    cursor = conn.cursor()

    return conn, cursor

def cadastar_pagamento():
    conn, cursor = conectar_banco()

    with st.form("form_cadastrar_pagamento"):
        df_nomes_cliente = pd.read_sql_query("SELECT id_cliente, nome_clientes FROM clientes ORDER BY nome_clientes", conn)

        cliente_escolhido = st.selectbox("Cliente", df_nomes_cliente["nome_clientes"])

        cliente_dict = dict(zip(df_nomes_cliente["nome_clientes"], df_nomes_cliente["id_cliente"]))
        
        id_cliente_escolhido = cliente_dict[cliente_escolhido]

        df_plano_cliente = pd.read_sql_query(f"""SELECT p.nome_planos
                                      FROM clientes c
                                      JOIN planos p ON p.id_plano = c.fk_plano_id
                                      WHERE c.id_cliente = {id_cliente_escolhido}""", conn)
        
        if not df_plano_cliente.empty:
            plano_escolhido = st.selectbox("Plano",
                                           df_plano_cliente["nome_planos"],
                                           disabled=True)


        
        data_pagamento = st.date_input("Data Pagamento").strftime("%Y/%m/%d")
        
        
        enviar = st.form_submit_button("Cadastrar")