import pandas as pd
import sqlite3
from datetime import date, datetime
import streamlit as st

# Consultas para visualização

def whole_df(option):
    conn = sqlite3.connect('banco_academia.db', check_same_thread=False)

    match option.lower():
        case 'clientes':
            df = pd.read_sql_query("SELECT * FROM clientes", conn)
        case 'treinos':
            df = pd.read_sql_query("SELECT * FROM treinos", conn)
        case 'exercicios':
            df = pd.read_sql_query("SELECT * FROM exercicios", conn)
        case 'instrutores':
            df = pd.read_sql_query("SELECT * FROM instrutores", conn)
        case 'planos':
            df = pd.read_sql_query("SELECT * FROM planos", conn)
        case 'pagamentos':
            df = pd.read_sql_query("SELECT * FROM pagamentos", conn)
        case 'treino_exercicios':
            df = pd.read_sql_query("SELECT * FROM treino_exercicios", conn)

    conn.close()

    return df # Retorna tabelas do banco puras

def clients():
    conn = sqlite3.connect('banco_academia.db', check_same_thread=False)

    df = pd.read_sql_query(""" 
        SELECT  c.id_cliente, c.nome_clientes AS nome, p.nome_planos AS plano, p.preco_mensal AS mensalidade, p.duracao_meses
        FROM clientes c
        JOIN planos p ON c.fk_plano_id = p.id_plano
        ORDER BY c.nome_clientes
     """, conn)

    conn.close()

    st.dataframe(df)

def filter_by_workout(workout):
    conn = sqlite3.connect('banco_academia.db', check_same_thread=False)
    
    workout = int(workout)

    df = pd.read_sql_query(""" 
        SELECT
            te.fk_treino_id AS treino,
            c.nome_clientes AS nome_cliente,
            i.nome_instrutores AS nome_instrutor,
            p.nome_planos AS plano,
            e.nome_exercicios AS exercicio,
            e.grupo_muscular AS tipo,
            te.series,
            te.repeticoes
        FROM treino_exercicios te
        JOIN treinos t ON te.fk_treino_id = t.id_treino
        JOIN exercicios e ON te.fk_exercicio_id = e.id_exercicio
        JOIN clientes c ON t.fk_cliente_id = c.id_cliente
        JOIN planos p ON t.fk_plano_id = p.id_plano
        JOIN instrutores i ON t.fk_instrutor_id = i.id_instrutor
        WHERE fk_treino_id = ?
    """, conn, params=(workout,))

    conn.close()

    st.dataframe(df) # Retorna dataframe pronto para visualização dos treinos e informações relevantes

def count_payments():
    conn = sqlite3.connect('banco_academia.db', check_same_thread=False)

    df = pd.read_sql_query(""" 
        SELECT COUNT(*) AS pagamentos
        FROM pagamentos
     """, conn)

    payments = df['pagamentos'].iloc[0]

    conn.close()

    st.write(f'Total de pagamentos: {payments}')

def last_payment():
    conn = sqlite3.connect('banco_academia.db', check_same_thread=False)

    df = pd.read_sql_query(""" 
        SELECT
            c.id_cliente,
            c.nome_clientes, 
            p.nome_planos, 
            pg.valor, MAX(pg.data_pagamento) AS ultimo_pagamento,
            CASE pg.pago
                WHEN 1 THEN 'Pago'
                ELSE 'Não pago'
            END
        FROM pagamentos pg
        JOIN clientes c ON pg.fk_cliente_id = c.id_cliente
        JOIN planos p ON pg.fk_plano_id = p.id_plano
        GROUP BY c.nome_clientes, p.nome_planos, pg.valor
     """, conn)
    
    conn.close()

    st.dataframe(df)

def instructor_clients():
    conn = sqlite3.connect('banco_academia.db', check_same_thread=False)

    df = pd.read_sql_query(""" 
        SELECT i.nome_instrutores AS instrutor, COUNT(DISTINCT t.fk_cliente_id) AS clientes
        FROM treinos t
        JOIN instrutores i ON t.fk_instrutor_id = i.id_instrutor
        GROUP BY i.nome_instrutores
     """, conn)
    
    conn.close()

    st.dataframe(df)