import sqlite3
import os

# Caminho do banco
db_path = 'database/biblioteca.db'

def ler_tabela(nome_tabela):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row # Permite acessar colunas pelo nome
    cursor = conn.cursor()
    
    print(f"\n--- DADOS DA TABELA: {nome_tabela.upper()} ---")
    try:
        cursor.execute(f"SELECT * FROM {nome_tabela}")
        linhas = cursor.fetchall()
        
        if not linhas:
            print("(Tabela vazia)")
        
        for linha in linhas:
            # Converte a linha (Row) para dicionário para ficar legível
            print(dict(linha))
            
    except sqlite3.OperationalError:
        print(f"Erro: A tabela '{nome_tabela}' não existe.")
    
    conn.close()

if __name__ == "__main__":
    if os.path.exists(db_path):
        ler_tabela('usuarios')
        ler_tabela('livros')
        ler_tabela('eventos')
    else:
        print("Erro: O arquivo do banco de dados não foi encontrado na pasta 'database/'")