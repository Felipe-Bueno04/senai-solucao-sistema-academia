# Sistema de Gerenciamento de Academia

Um sistema completo para gerenciamento de clientes, instrutores, treinos e pagamentos em academias, desenvolvido com Python, Streamlit e SQLite.

## 📌 Visão Geral

O sistema oferece:
- Autenticação de usuários com níveis de acesso (Admin, Funcionário, Cliente)
- Cadastro e gerenciamento de clientes, pagamentos, treinos e exercícios
- Análises de dados e visualizações personalizadas
- Painel administrativo com métricas chave

## 🛠️ Tecnologias Utilizadas

- **Frontend**: Streamlit
- **Backend**: Python
- **Banco de Dados**: SQLite
- **Autenticação**: Bcrypt para hash de senhas
- **Estilos**: CSS personalizado

## 🔐 Funcionalidades de Autenticação

- Registro de novos usuários
- Login seguro com verificação de credenciais
- Alteração de senha
- Níveis de acesso:
  - **Admin**: Acesso completo ao sistema
  - **Funcionário**: Cadastros e análises
  - **Cliente**: Visualização de dados pessoais

## 📊 Módulos Principais

1. **Dashboard Inicial**
   - Métricas de clientes ativos, pagamentos e treinos
   - Agenda diária de treinos
   - Área de notificações

2. **Análises de Dados**
   - Listagem de clientes e planos
   - Visualização de treinos e exercícios
   - Histórico de pagamentos
   - Relação instrutor-cliente

3. **Cadastros**
   - Clientes
   - Pagamentos
   - Treinos
   - Exercícios

4. **Administração**
   - Gerenciamento de cargos de usuários
   - Controle de acessos

## 🚀 Como Executar

1. Clone o repositório:
```bash
git clone https://github.com/leofukuyama/senai-solucao-sistema-academia
```
Instale as dependências:

```bash
pip install pandas streamlit bcrypt
```
Execute o aplicativo:

```bash
streamlit run main.py
```

📦 Estrutura de Arquivos:
<pre>
├── main.py               # Executável 
├── analise_dados/
│   └── functions.py      # Funções para análise de dados
├── formularios_cadastro/ # Formulários de cadastro
│   ├── cadastro_cliente.py
│   ├── cadastro_pagamento.py
│   ├── cadastro_treino.py
│   └── cadastro_exercicio.py
├── assets/
│   ├── style.css         # Estilos personalizados
│   └── logo_academia.png # Logo da aplicação
├── banco_academia.db     # Banco de dados principal
└── users.db              # Banco de dados de usuários
</pre>

📝 Licença
Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.

✉️ Contato
Para dúvidas ou sugestões, entre em contato com o desenvolvedor.