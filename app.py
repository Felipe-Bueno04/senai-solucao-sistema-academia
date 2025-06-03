import streamlit as st
import sqlite3
import bcrypt
from analise_dados.functions import whole_df, filter_by_workout, last_payment, count_payments, instructor_clients, clients, current_workout
from formularios_cadastro.cadastro_cliente import cadastrar_cliente
from formularios_cadastro.cadastro_pagamento import cadastar_pagamento
from formularios_cadastro.cadastro_treino import cadastrar_treino
from formularios_cadastro.cadastro_exercicio import cadastrar_exercicio_no_treino

def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL,
        email TEXT
    )""")
    conn.commit()
    conn.close()

init_db()

def register_user(username, password, email=None):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return False
    
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    cursor.execute("INSERT INTO users VALUES (?, ?, ?)", (username, hashed, email))
    conn.commit()
    conn.close()
    return True

def verify_login(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    if result := cursor.fetchone():
        return bcrypt.checkpw(password.encode('utf-8'), result[0])
    return False

def update_password(username, new_password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
    cursor.execute("UPDATE users SET password = ? WHERE username = ?", (hashed, username))
    conn.commit()
    conn.close()
    return True

def main():
    
    with open("css/login.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    st.image("img/logo_FFLR.png", width=700)
    # Estado da sessão
    if 'auth' not in st.session_state:
        st.session_state.update({
            'auth': False,
            'page': 'login',
            'current_user': None,
            'selected_option': None
        })

    if not st.session_state.auth and st.session_state.page == 'login':
            
        st.title("🔒 Área de Login")
        
        with st.form("login_form"):    
            username = st.text_input("Usuário")
            password = st.text_input("Senha", type="password")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("Entrar"):
                    if verify_login(username, password):
                        st.session_state.update({
                            'auth': True,
                            'current_user': username,
                            'page': 'main'
                        })
                        st.rerun()
                    else:
                        st.error("Credenciais inválidas")
            with col2:
                if st.form_submit_button("Criar Conta"):
                    st.session_state.page = 'register'
                    st.rerun()

    elif not st.session_state.auth and st.session_state.page == 'register':
        st.title("📝 Registrar Nova Conta")
        
        with st.form("register_form"):
            new_user = st.text_input("Novo Usuário")
            new_pass = st.text_input("Nova Senha", type="password")
            confirm_pass = st.text_input("Confirmar Senha", type="password")
            email = st.text_input("Email (opcional)")
            
            if st.form_submit_button("Criar Conta"):
                if new_pass != confirm_pass:
                    st.error("As senhas não coincidem!")
                elif register_user(new_user, new_pass, email):
                    st.success("Conta criada com sucesso!")
                    st.session_state.page = 'login'
                    st.rerun()
                else:
                    st.error("Usuário já existe")
            
            if st.form_submit_button("Voltar"):
                st.session_state.page = 'login'
                st.rerun()

    elif st.session_state.auth:
        st.session_state.selected_option = st.sidebar.selectbox(
            "Menu de Opções",
            options=[
                "🏠 Início",
                "📊 Análises",
                "💾 Cadastros",
                "🔐 Alterar Senha",
                "🚪 Sair"
            ],
            index=0
        )

        if st.session_state.selected_option == "🏠 Início":
            st.title(f"👋 Bem-vindo, {st.session_state.current_user}!")
            st.write("Selecione as opções no menu ao lado para navegar no sistema!")

        elif st.session_state.selected_option == "📊 Análises":
            st.title("💻 Gerenciar Clientes")
            st.write("O sistema é capaz de controlar os dados de **Clientes**, **Instrutores**, **Planos**, **Treinos** e **Exercícios**")

            st.subheader(":clipboard: Listar Clientes e Planos:", divider="grey")
            clients()

            st.subheader(":ledger: Treinos recentes de clientes e seus Exercícios:", divider="grey")
            treinos = current_workout()
            cliente = st.selectbox('Selecione um cliente:', treinos['cliente'])
            id_treino = treinos['id_treino_atual'].loc[treinos['cliente'] == cliente].iloc[0]
            filter_by_workout(id_treino)

            st.subheader(":dollar: Total Pagamentos e Último Pagamento Cliente:", divider="grey")
            count_payments()
            last_payment()

            st.subheader(":teacher: Quantos Clientes um Instrutor atende: ", divider="grey")
            instructor_clients()

        elif st.session_state.selected_option == "💾 Cadastros":
            st.subheader(":heavy_plus_sign: Formulário de Cadastro:", divider="grey")

            opcoes_cadastro = st.radio("O que deseja cadastrar?", ["Cliente", "Pagamento", "Treinos", "Exercícios no Treino"])

            if opcoes_cadastro == "Cliente":
                cadastrar_cliente()

            elif opcoes_cadastro == "Pagamento":
                cadastar_pagamento()

            elif opcoes_cadastro == "Treinos":
                cadastrar_treino()

            elif opcoes_cadastro == "Exercícios no Treino":
                cadastrar_exercicio_no_treino()

        elif st.session_state.selected_option == "🔐 Alterar Senha":
            st.subheader("Alteração de Senha")
            with st.form("change_pass_form"):
                current_pass = st.text_input("Senha Atual", type="password")
                new_pass = st.text_input("Nova Senha", type="password")
                confirm_pass = st.text_input("Confirmar Nova Senha", type="password")
                
                if st.form_submit_button("Confirmar"):
                    if new_pass != confirm_pass:
                        st.error("As senhas não coincidem!")
                    elif not verify_login(st.session_state.current_user, current_pass):
                        st.error("Senha atual incorreta!")
                    else:
                        update_password(st.session_state.current_user, new_pass)
                        st.success("Senha alterada com sucesso!")

        elif st.session_state.selected_option == "🚪 Sair":
            st.session_state.auth = False
            st.session_state.page = 'login'
            st.rerun()

        st.sidebar.markdown("---")
        st.sidebar.markdown(f"Usuário: `{st.session_state.current_user}`")

    if not st.session_state.auth:
        st.stop()

if __name__ == "__main__":
    main()