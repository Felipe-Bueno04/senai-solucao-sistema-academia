import sqlite3
import streamlit as st
import pandas as pd

def conectar_banco():
    conn = sqlite3.connect("banco_academia.db", check_same_thread=False)
    cursor = conn.cursor()

    return conn, cursor

def cadastrar_exercicio_no_treino():
    conn, cursor = conectar_banco()

    df_treinos = pd.read_sql_query(""" 
        SELECT c.nome_clientes as cliente, MAX(t.id_treino) AS id_treino_atual
        FROM treinos t
        JOIN clientes c ON t.fk_cliente_id = c.id_cliente
        GROUP BY c.nome_clientes
     """, conn)
    
    with st.form("form_cadastrar_exercicio_no_treino", clear_on_submit=True):
        cliente = st.selectbox('Selecione o cliente: ', df_treinos['cliente'])
        treino = int(df_treinos['id_treino_atual'].loc[df_treinos['cliente'] == cliente].iloc[0])

        treino_exercicios = pd.read_sql_query("SELECT fk_exercicio_id FROM treino_exercicios WHERE fk_treino_id = ?", conn, params=(treino,))
        exercicios_repetidos = list(treino_exercicios['fk_exercicio_id'])
        prm_list = ", ".join("?" for _ in exercicios_repetidos)
        sql_string = f"SELECT * FROM exercicios WHERE id_exercicio NOT IN({prm_list})"
        df_exercicios = pd.read_sql_query(sql_string, conn, params=(exercicios_repetidos))
        if df_exercicios['id_exercicio'].shape[0] != 0:            
                exercicio = st.selectbox('Selecione o exercício:', df_exercicios['nome_exercicios'])
                id_exercicio = int(df_exercicios['id_exercicio'].loc[df_exercicios['nome_exercicios'] == exercicio].iloc[0])

                series = int(st.number_input("Número de séries:", min_value=1, step=1))
                repeticoes = int(st.number_input("Número de repetições:", min_value=1, step=1))

                enviar = st.form_submit_button("Cadastrar")

                if enviar:
                    if treino and exercicio and series and repeticoes:
                        cursor.execute("INSERT INTO treino_exercicios (fk_treino_id, fk_exercicio_id, series, repeticoes) VALUES (?, ?, ?, ?)",(treino, id_exercicio, series, repeticoes))
                        conn.commit()
                        st.success(f"Exercício adicionado com sucesso ao treino! {exercicio.capitalize()} - Treino {treino}.")
                        st.rerun()
        else:
            st.write('Não há exercícios novos')
    conn.close()
