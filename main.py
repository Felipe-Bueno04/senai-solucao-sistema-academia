import sqlite3
import streamlit as st
import pandas as pd
import matplotlib as plt
import seaborn as sns

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
    st.write("Cadastro Cliente") # Excluir após implementação

elif opcoes_cadastro == "Pagamento":
    #TODO: Implementar Cadastro Pagamento
    st.write("Cadastro Pagamento") # Excluir após implementação

elif opcoes_cadastro == "Treinos":
    #TODO: Implementar Cadastro Treinos
    st.write("Cadastro Treinos") # Excluir após implementação

elif opcoes_cadastro == "Exercícios no Treino":
    #TODO: Implementar Cadastro Exercícios no Treino
    st.write("Cadastro Exercícios") # Excluir após implementação