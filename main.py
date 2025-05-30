import sqlite3
import streamlit as st
import pandas as pd
import matplotlib as plt
import seaborn as sns
from cadastro_cliente import cadastrar_cliente
from cadastro_pagamento import cadastar_pagamento
from cadastro_treino import cadastrar_treino
from cadastro_exercicio import cadastrar_exercicio_no_treino

st.title(":muscle: Sistema de Academia",)
st.write("O sistema é capaz de controlar os dados de **Clientes**, **Instrutores**, **Planos**, **Treinos** e **Exercícios**")

st.subheader(":clipboard: Listar Clientes e Planos:", divider="grey")

st.subheader(":ledger: Treinos e seus Exercícios:", divider="grey")

st.subheader(":dollar: Total Pagamentos e Último Pagamento Cliente:", divider="grey")

st.subheader(":teacher: Quantos Clientes um Instrutor atende: ", divider="grey")

st.subheader(":heavy_plus_sign: Formulário de Cadastro:", divider="grey")

opcoes_cadastro = st.radio("O que deseja cadastrar?", ["Cliente", "Pagamento", "Treinos", "Exercícios no Treino"])

if opcoes_cadastro == "Cliente":
    #TODO: Implementar Cadastro Cliente
    cadastrar_cliente()

elif opcoes_cadastro == "Pagamento":
    #TODO: Implementar Cadastro Pagamento
    cadastar_pagamento()

elif opcoes_cadastro == "Treinos":
    #TODO: Implementar Cadastro Treinos
    cadastrar_treino()

elif opcoes_cadastro == "Exercícios no Treino":
    #TODO: Implementar Cadastro Exercícios no Treino
    cadastrar_exercicio_no_treino()