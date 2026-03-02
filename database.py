import sqlite3

NOME_BANCO = "cadastros_biometria.db"

def inicializar_banco():
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
    conexao = sqlite3.connect(NOME_BANCO)
    cursor = conexao.cursor()
    query = """
        INSERT INTO cadastros (nome_completo, data_nascimento, numero_contato, data_biometria, horario_biometria)
        VALUES (?, ?, ?, ?, ?)
    """
    cursor.execute(query, (nome, data_nasc, contato, data_bio, hora_bio))
    conexao.commit()
    conexao.close()

def buscar_por_mes_ano(mes, ano):
    conexao = sqlite3.connect(NOME_BANCO)
    cursor = conexao.cursor()
    
    if mes == "Todos" and ano == "Todos":
        cursor.execute("SELECT * FROM cadastros")
    elif mes != "Todos" and ano != "Todos":
        termo = f"%/{mes}/{ano}"
        cursor.execute("SELECT * FROM cadastros WHERE data_biometria LIKE ?", (termo,))
    elif mes != "Todos" and ano == "Todos":
        termo = f"%/{mes}/%"
        cursor.execute("SELECT * FROM cadastros WHERE data_biometria LIKE ?", (termo,))
    elif mes == "Todos" and ano != "Todos":
        termo = f"%/%/{ano}"
        cursor.execute("SELECT * FROM cadastros WHERE data_biometria LIKE ?", (termo,))
        
    resultados = cursor.fetchall()
    conexao.close()
    return resultados

def buscar_por_data_exata(data):
    conexao = sqlite3.connect(NOME_BANCO)
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM cadastros WHERE data_biometria = ? ORDER BY horario_biometria ASC", (data,))
    resultados = cursor.fetchall()
    conexao.close()
    return resultados

# --- NOVA FUNÇÃO ---
def buscar_horarios_ocupados(data):
    """Retorna uma lista de horários já cadastrados para um dia específico."""
    conexao = sqlite3.connect(NOME_BANCO)
    cursor = conexao.cursor()
    cursor.execute("SELECT horario_biometria FROM cadastros WHERE data_biometria = ?", (data,))
    resultados = cursor.fetchall()
    conexao.close()
    # Pega apenas a coluna do horário e transforma numa lista simples
    return [linha[0] for linha in resultados]