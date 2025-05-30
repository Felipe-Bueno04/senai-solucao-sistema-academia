import sqlite3
import streamlit as st
import pandas as pd

def conectar_banco():
    conn = sqlite3.connect("banco_academia.db", check_same_thread=False)
    cursor = conn.cursor()

    return conn, cursor

def cadastrar_cliente():
    conn, cursor = conectar_banco()

    with st.form("form_cadastrar_cliente"):
        nome_cliente = st.text_input("Nome Completo:", placeholder="Nome Sobrenome")
        email_cliente = st.text_input("E-mail:", placeholder="email@dominio.com")
        telefone = st.text_input("Telefone:", placeholder="+00 (DDD) 9 1234-5678")
        idade = st.number_input("Idade:", min_value=12, step=1)

        #TODO: Query para selecionar os nomes dos planos disponíveis
        # df_planos = pd.read_sql_query("", conn)
        #TODO: Selectbox para mostrar os planos disponíveis
        # plano_escolhido = st.selectbox("")

        enviar = st.form_submit_button("Cadastrar")

        if enviar:
            if nome_cliente and email_cliente and telefone and idade and plano_escolhido:
                cursor.execute("INSERT INTO clientes (nome, email, telefone, idade, fk_plano_id)")
                conn.commit()
                st.success(f"Cliente Cadastrado com sucesso! {nome_cliente.capitalize()} - Plano {plano_escolhido}.")
                st.rerun()
