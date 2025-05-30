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
        #TODO: Query para selecionar os nomes dos clientes no banco
        # df_nomes_cliente = pd.read_sql_query("", conn)
        #TODO: Selectbox para escolher o cliente que fez o pagamento
        # cliente_escolhido = st.selectbox("")

        data_pagamento = st.date_input("Data Pagamento").strftime("%Y/%m/%d")
        
        
        enviar = st.form_submit_button("Cadastrar")