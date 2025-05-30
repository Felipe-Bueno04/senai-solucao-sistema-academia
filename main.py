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

