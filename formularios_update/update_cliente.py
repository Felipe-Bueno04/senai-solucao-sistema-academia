import sqlite3
import streamlit as st
import pandas as pd

def conectar_banco():
    conn = sqlite3.connect("banco_academia.db", check_same_thread=False)
    cursor = conn.cursor()

    return conn, cursor

def update_cliente():
    conn, cursor = conectar_banco()

    df_clientes = pd.read_sql_query("SELECT * FROM clientes", conn)
    cliente = st.selectbox('Selecione o cliente', df_clientes['nome_clientes'])
    with st.form("form_update_cliente", clear_on_submit=True):
        nome_cliente = st.text_input("Nome Completo:", placeholder="Nome Sobrenome")
        email_cliente = st.text_input("E-mail:", placeholder="email@dominio.com")
        telefone_cliente = st.text_input("Telefone:", placeholder="+00 (DDD) 9 1234-5678")
        idade = st.number_input("Idade:", min_value=12, step=1)
        id_cliente = int(df_clientes['id_cliente'].loc[df_clientes['nome_clientes'] == cliente].iloc[0])

        df_planos = pd.read_sql_query("SELECT id_plano, nome_planos FROM planos ORDER BY nome_planos", conn)
        plano_escolhido = st.selectbox("Plano", df_planos["nome_planos"], index=2)

        enviar = st.form_submit_button("Atualizar")

        if enviar:
            if nome_cliente and email_cliente and telefone_cliente and idade and plano_escolhido:
                id_plano_escolhido = int(pd.read_sql_query(f"SELECT id_plano FROM planos WHERE nome_planos = ?", conn, params=(plano_escolhido,)).iloc[0, 0])

                cursor.execute("""UPDATE clientes SET nome_clientes = ?, email = ?, telefone = ?, idade = ?, fk_plano_id = ? WHERE id_cliente = ?""",
                               (nome_cliente, email_cliente, telefone_cliente, idade, id_plano_escolhido, id_cliente))
                conn.commit()
                st.success(f"Cliente atualizado com sucesso! {nome_cliente.capitalize()} - Plano {plano_escolhido}.")
                st.rerun()
                conn.close()
