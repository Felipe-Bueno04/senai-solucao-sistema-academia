import sqlite3
import streamlit as st
import pandas as pd

def conectar_banco():
    conn = sqlite3.connect("banco_academia.db", check_same_thread=False)
    cursor = conn.cursor()

    return conn, cursor

def cadastar_pagamento():
    conn, cursor = conectar_banco()

    with st.form("form_cadastrar_pagamento", clear_on_submit=True):
        df_nomes_cliente = pd.read_sql_query("SELECT id_cliente, nome_clientes FROM clientes ORDER BY nome_clientes", conn)
        clientes_dict = dict(zip(df_nomes_cliente["nome_clientes"], df_nomes_cliente["id_cliente"]))
        
        cliente_escolhido = st.selectbox("Cliente", df_nomes_cliente["nome_clientes"])
        id_cliente_escolhido = clientes_dict[cliente_escolhido]

        df_plano_cliente = pd.read_sql_query(f"""SELECT p.id_plano, p.nome_planos
                                      FROM clientes c
                                      JOIN planos p ON p.id_plano = c.fk_plano_id
                                      WHERE c.id_cliente = {id_cliente_escolhido}""", conn)
        id_plano_cliente = int(df_plano_cliente.iloc[0, 0])

        data_pagamento = st.date_input("Data Pagamento").strftime("%Y-%m-%d")
        
        valor_pagamento = st.number_input("Valor", min_value=80, step=10)

        foi_pago = st.radio("Foi pago?", ["Sim", "Não"])
        booleano_foi_pago = int(foi_pago == "Sim")

        enviar = st.form_submit_button("Cadastrar")

        if enviar and cliente_escolhido and data_pagamento and valor_pagamento:
            cursor.execute("""INSERT INTO pagamentos (fk_plano_id, fk_cliente_id, data_pagamento, valor, pago)
                               VALUES (?, ?, ?, ?, ?)""",
                               (id_plano_cliente, id_cliente_escolhido, data_pagamento, valor_pagamento, booleano_foi_pago))

            conn.commit()
            st.success(f"Pagamento Cadastrado! {cliente_escolhido} - R$ {valor_pagamento:.2f}")
            st.rerun()
