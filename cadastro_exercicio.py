import sqlite3
import streamlit as st
import pandas as pd

def conectar_banco():
    conn = sqlite3.connect("banco_academia.db", check_same_thread=False)
    cursor = conn.cursor()

    return conn, cursor

def cadastrar_exercicio_no_treino():
    conn, cursor = conectar_banco()

    with st.form("form_cadastrar_exercicio_no_treino"):
        df_treinos = pd.read_sql_query("SELECT * FROM treinos", conn)
        treino = st.selectbox('Selecione o treino: ', df_treinos['id_treino'])

        df_exercicios = pd.read_sql_query("SELECT * FROM exercicios", conn)
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
