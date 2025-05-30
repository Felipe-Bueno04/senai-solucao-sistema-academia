import sqlite3
import pandas as pd

conn = sqlite3.connect("banco_academia.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS clientes (
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL,
    telefone TEXT NOT NULL,
    idade INTEGER NOT NULL,
    fk_plano_id INTEGER NOT NULL,
    FOREIGN KEY (fk_plano_id) REFERENCES planos(id_plano)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS instrutores (
    id_instrutor INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    especialidade TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS planos (
    id_plano INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    preco_mensal INTEGER NOT NULL,
    duracao_meses INTEGER NOT NULL   
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS exercicios (
    id_exercicio INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    grupo_muscular TEXT NOT NULL   
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS treinos (
    id_treino INTEGER PRIMARY KEY AUTOINCREMENT,
    fk_cliente_id INTEGER NOT NULL,
    fk_instrutor_id INTEGER NOT NULL,
    data_inicio DATE NOT NULL,
    data_fim DATE NOT NULL,
    fk_plano_id INTEGER NOT NULL,
    FOREIGN KEY (fk_cliente_id) REFERENCES clientes(id_cliente),
    FOREIGN KEY (fk_instrutor_id) REFERENCES instrutores(id_instrutor),
    FOREIGN KEY (fk_plano_id) REFERENCES planos(id_plano)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS treino_exercicios (
    id_treino_exercicio INTEGER PRIMARY KEY AUTOINCREMENT,
    fk_treino_id INTEGER NOT NULL,
    fk_exercicio_id INTEGER NOT NULL,
    series INTEGER NOT NULL,
    repeticoes INTEGER NOT NULL,
    FOREIGN KEY (fk_treino_id) REFERENCES treinos(id_treino),
    FOREIGN KEY (fk_exercicio_id) REFERENCES exercicios(id_exercicio)      
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS pagamentos (
    id_pagamento INTEGER PRIMARY KEY AUTOINCREMENT,
    fk_plano_id INTEGER NOT NULL,
    fk_cliente_id INTEGER NOT NULL,
    data_pagamento DATE NOT NULL,
    valor INTEGER NOT NULL,
    pago BIT,
    FOREIGN KEY (fk_cliente_id) REFERENCES clientes(id_cliente),
    FOREIGN KEY (fk_plano_id) REFERENCES planos(id_plano)
)
''')

#POUPLAR CLIENTES
df = pd.read_csv("arquivos_csv/clientes_academia.csv")
colunas_desejadas = ['nome', 'email', 'telefone', 'idade', 'plano_id']
df_novo = df[colunas_desejadas]

for _, linha in df_novo.iterrows():
    cursor.execute('SELECT COUNT(*) FROM clientes WHERE email = ?', (linha['email'],))
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO clientes (nome, email, telefone, idade, fk_plano_id) VALUES (?, ?, ?, ?, ?)
        ''', (linha['nome'], linha['email'], linha['telefone'], linha['idade'], linha['plano_id']))

#POPULAR INSTUTORES
df = pd.read_csv("arquivos_csv/instrutores.csv")
for _, linha in df.iterrows():
    cursor.execute('SELECT COUNT(*) FROM instrutores WHERE nome = ?', (linha['nome'],))
    if cursor.fetchone()[0] == 0:    
        cursor.execute('''
            INSERT INTO instrutores (nome, especialidade) VALUES (?, ?)
        ''', (linha['nome'], linha['especialidade']))

#POPULAR PLANOS
df = pd.read_csv("arquivos_csv/planos.csv")
for _, linha in df.iterrows():
    cursor.execute('SELECT COUNT(*) FROM planos WHERE nome = ?', (linha['nome'],))
    if cursor.fetchone()[0] == 0:    
        cursor.execute('''
            INSERT INTO planos (nome, preco_mensal, duracao_meses) VALUES (?, ?, ?)
        ''', (linha['nome'], linha['preco_mensal'], linha['duracao_meses']))

#POPULAR EXERCICIOS
df = pd.read_csv("arquivos_csv/exercicios.csv")
for _, linha in df.iterrows():
    cursor.execute('SELECT COUNT(*) FROM exercicios WHERE nome = ?', (linha['nome'],))
    if cursor.fetchone()[0] == 0:    
        cursor.execute('''
            INSERT INTO exercicios (nome, grupo_muscular) VALUES (?, ?)
        ''', (linha['nome'], linha['grupo_muscular']))

#POPULAR TREINOS
df = pd.read_csv("arquivos_csv/treinos.csv")
for _, linha in df.iterrows():
    cursor.execute('SELECT COUNT(*) FROM treinos WHERE fk_cliente_id = ?', (linha['cliente_id'],))
    if cursor.fetchone()[0] == 0:    
        cursor.execute('''
            INSERT INTO treinos (fk_cliente_id, fk_instrutor_id, data_inicio, data_fim, fk_plano_id) VALUES (?, ?, ?, ?, ?)
        ''', (linha['cliente_id'], linha['instrutor_id'], linha['data_inicio'], linha ['data_fim'], linha['plano_id']))

#POPULAR TREINOS-EXERCICIOS
df = pd.read_csv("arquivos_csv/treino_exercicios.csv")
for _, linha in df.iterrows():
    cursor.execute('''
        SELECT COUNT(*) FROM treino_exercicios WHERE fk_treino_id = ? AND fk_exercicio_id = ? AND series = ? AND repeticoes = ?
    ''', (linha['treino_id'], linha['exercicio_id'], linha['series'], linha['repeticoes']))
    
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO treino_exercicios (fk_treino_id, fk_exercicio_id, series, repeticoes) VALUES (?, ?, ?, ?)
        ''', (int(linha['treino_id']), int(linha['exercicio_id']), int(linha['series']), int(linha['repeticoes'])))

#POPULAR PAGAMENTOS
df = pd.read_csv("arquivos_csv/pagamento_clientes.csv")
caminho_csv = "arquivos_csv/pagamento_clientes.csv"

df = pd.read_csv(caminho_csv)

df["ativo"] = 1

df.to_csv(caminho_csv, index=False)
for _, linha in df.iterrows():
    cursor.execute('''
        SELECT COUNT(*) FROM pagamentos WHERE fk_cliente_id = ? AND fk_plano_id = ? AND valor = ? AND data_pagamento = ? AND pago = ?
    ''', (linha['cliente_id'], linha['plano_id'], linha['valor_pago'], linha['data_pagamento'], linha['ativo']))
    
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO pagamentos (fk_cliente_id, fk_plano_id, valor, data_pagamento, pago) VALUES (?, ?, ?, ?, ?)
        ''', (linha['cliente_id'], linha['plano_id'], linha['valor_pago'], linha['data_pagamento'], linha['ativo']))

conn.commit()
conn.close()