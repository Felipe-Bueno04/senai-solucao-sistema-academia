import sqlite3
import streamlit as st
import pandas as pd

def conectar_banco():
    conn = sqlite3.connect("banco_academia.db", check_same_thread=False)
    cursor = conn.cursor()

    return conn, cursor

def cadastrar_cliente():
    conn, cursor = conectar_banco()

    with st.form("form_cadastrar_cliente", clear_on_submit=True):
        nome_cliente = st.text_input("Nome Completo:", placeholder="Nome Sobrenome").strip()
        email_cliente = st.text_input("E-mail:", placeholder="email@dominio.com").strip()
        telefone_cliente = st.text_input("Telefone:", placeholder="+00 (DDD) 9 1234-5678").strip()
        idade = st.number_input("Idade:", min_value=12, step=1)

        df_planos = pd.read_sql_query("SELECT id_plano, nome_planos FROM planos ORDER BY nome_planos", conn)
        plano_escolhido = st.selectbox("Plano", df_planos["nome_planos"], index=2)

        enviar = st.form_submit_button("Cadastrar")

        if enviar:
            if nome_cliente and email_cliente and telefone_cliente and idade and plano_escolhido:
                id_plano_escolhido = int(pd.read_sql_query(f"SELECT id_plano FROM planos WHERE nome_planos = '{plano_escolhido}'", conn).iloc[0, 0])

                cursor.execute("""INSERT INTO clientes (nome_clientes, email, telefone, idade, fk_plano_id)
                               VALUES (?, ?, ?, ?, ?)""",
                               (nome_cliente, email_cliente, telefone_cliente, idade, id_plano_escolhido))
                conn.commit()
                st.success(f"Cliente Cadastrado com sucesso! {nome_cliente.capitalize()} - Plano {plano_escolhido}.")
                st.rerun()
