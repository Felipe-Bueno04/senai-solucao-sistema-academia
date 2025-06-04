import sqlite3
import streamlit as st
import pandas as pd

def conectar_banco():
    conn = sqlite3.connect("banco_academia.db", check_same_thread=False)
    cursor = conn.cursor()
    
    return conn, cursor

def cadastrar_treino():
    conn, cursor = conectar_banco()
    
    with st.form("form_cadastrar_cliente", clear_on_submit=True):
        df_clientes = pd.read_sql_query("SELECT nome_clientes FROM clientes ORDER BY nome_clientes", conn)
        nome_cliente = st.selectbox("Cliente", df_clientes['nome_clientes'])
        
        df_instrutores = pd.read_sql_query("SELECT nome_instrutores FROM instrutores ORDER BY nome_instrutores", conn)
        nome_instrutor = st.selectbox("Instrutor", df_instrutores['nome_instrutores'])
        
        data_inicio = st.date_input(label="Data Início", value="today", max_value=None, format="YYYY/MM/DD")
        data_fim = st.date_input(label="Data Fim ", value="today", max_value=None, format="YYYY/MM/DD")
        
        df_planos = pd.read_sql_query("SELECT nome_planos FROM planos", conn)
        
        enviar = st.form_submit_button("Cadastrar treino")
        
        if enviar:
            if nome_cliente and nome_instrutor and data_inicio and data_fim:
                id_cliente = int(pd.read_sql_query(f"SELECT id_cliente FROM clientes WHERE nome_clientes = '{nome_cliente}'", conn).iloc[0, 0])
                id_instrutor = int(pd.read_sql_query(f"SELECT id_instrutor FROM instrutores WHERE nome_instrutores = '{nome_instrutor}'", conn).iloc[0, 0])
                id_plano = int(pd.read_sql_query(f"""SELECT p.id_plano, p.nome_planos FROM clientes c
                                                 JOIN planos p ON c.fk_plano_id = p.id_plano
                                                 WHERE c.id_cliente = {id_cliente}""", conn).iloc[0, 0])
                
                cursor.execute("""
                INSERT INTO treinos (fk_cliente_id, fk_instrutor_id, data_inicio, data_fim, fk_plano_id)
                VALUES (?, ?, ?, ?, ?)               
                """, (id_cliente, id_instrutor, data_inicio, data_fim, id_plano))
                conn.commit()
                st.success("Treino cadastrado com sucesso!")
                st.rerun()
