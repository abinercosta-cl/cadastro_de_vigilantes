import sqlite3

NOME_BANCO = "cadastros_biometria.db"

def inicializar_banco():
    """Cria o arquivo do banco de dados e a tabela se não existirem."""
    conexao = sqlite3.connect(NOME_BANCO)
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cadastros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_completo TEXT NOT NULL,
            data_nascimento TEXT NOT NULL,
            numero_contato TEXT,
            data_biometria TEXT,
            horario_biometria TEXT
        )
    ''')
    conexao.commit()
    conexao.close()

def salvar_cadastro(nome, data_nasc, contato, data_bio, hora_bio):
    """Insere um novo registro no banco de dados."""
    conexao = sqlite3.connect(NOME_BANCO)
    cursor = conexao.cursor()
    query = """
        INSERT INTO cadastros (nome_completo, data_nascimento, numero_contato, data_biometria, horario_biometria)
        VALUES (?, ?, ?, ?, ?)
    """
    cursor.execute(query, (nome, data_nasc, contato, data_bio, hora_bio))
    conexao.commit()
    conexao.close()

def buscar_por_data_biometria(data):
    """Busca cadastros no banco filtrando pela data da biometria."""
    conexao = sqlite3.connect(NOME_BANCO)
    cursor = conexao.cursor()
    
    # Se a data for fornecida, filtra. Se estiver vazia, traz todos.
    if data:
        cursor.execute("SELECT * FROM cadastros WHERE data_biometria = ?", (data,))
    else:
        cursor.execute("SELECT * FROM cadastros")
        
    resultados = cursor.fetchall()
    conexao.close()
    return resultados