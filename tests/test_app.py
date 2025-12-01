import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import sqlite3

# Adiciona o caminho do backend para importação
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend/src')))

# Importa o módulo app como um objeto para podermos modificar variáveis globais dele
import app as app_module 

class BaseTestCase(unittest.TestCase):
    """Classe base para configurar o ambiente de teste isolado"""
    def setUp(self):
        # Configurações do Flask para teste
        app_module.app.config['TESTING'] = True
        app_module.app.config['WTF_CSRF_ENABLED'] = False 
        app_module.app.secret_key = 'test_secret_key'
        self.app = app_module.app.test_client()
        
        # --- MÁGICA DO BANCO ISOLADO ---
        # 1. Salva o caminho do banco original para não estragar
        self.db_path_original = app_module.DB_PATH
        # 2. Define um nome para o banco temporário de teste
        self.test_db_path = os.path.join(os.path.dirname(self.db_path_original), 'test_biblioteca.db')
        
        # 3. Força o app a usar esse banco temporário
        app_module.DB_PATH = self.test_db_path
        
        # 4. Garante que o arquivo está limpo (se sobrou de um teste abortado)
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
            
        # 5. Cria as tabelas do zero nesse banco novo
        with app_module.app.app_context():
            app_module.init_db()

    def tearDown(self):
        """Limpa a sujeira depois de cada teste"""
        # 1. Restaura o caminho original do banco (para não quebrar o app normal)
        app_module.DB_PATH = self.db_path_original
        
        # 2. Apaga o arquivo do banco de teste do disco
        if os.path.exists(self.test_db_path):
            try:
                os.remove(self.test_db_path)
            except PermissionError:
                pass # as vezes o Windows segura o arquivo por alguns milissegundos

    def login(self, email, senha):
        """Helper para realizar login nos testes"""
        return self.app.post('/login', data=dict(
            email=email,
            senha=senha
        ), follow_redirects=True)

    def logout(self):
        """Helper para realizar logout"""
        return self.app.get('/logout', follow_redirects=True)

class TestesIntegracao(BaseTestCase):
    """Testes de Integração: Verificam o fluxo real com Banco de Dados"""

    def test_fluxo_login_logout(self):
        # 1. Login com admin (criado automaticamente no init_db)
        response = self.login('admin@email.com', 'admin123')
        html = response.data.decode('utf-8')
        self.assertIn('Administrador Chefe', html) 
        self.assertIn('Sair', html)

        # 2. Logout
        response = self.logout()
        html = response.data.decode('utf-8')
        self.assertIn('Login', html) 

    def test_acesso_negado_leitor(self):
        """Testa se um Leitor é bloqueado de acessar áreas de Admin"""
        self.login('leitor@email.com', '123456')
        
        response = self.app.get('/livros/adicionar', follow_redirects=True)
        html = response.data.decode('utf-8')
        
        self.assertIn('Acesso negado', html)

    def test_cadastro_novo_usuario(self):
        """Testa o cadastro de um novo usuário no banco"""
        # Como o banco é recriado a cada teste, este email nunca existirá antes
        response = self.app.post('/cadastro', data=dict(
            nome='Novo Usuario',
            email='novo@teste.com',
            senha='123',
            endereco='Rua Teste',
            termos='on' 
        ), follow_redirects=True)

        html = response.data.decode('utf-8')
        self.assertIn('Cadastro realizado', html)

        # Verifica se consegue logar com o novo usuário
        login_response = self.login('novo@teste.com', '123')
        html_login = login_response.data.decode('utf-8')
        self.assertIn('Novo Usuario', html_login)

class TestesUnitariosMocks(BaseTestCase):
    """Testes Unitários: Usam Mocks para simular erros de banco de dados"""

    @patch('app.get_db_connection')
    def test_erro_banco_dados_cadastro(self, mock_get_db):
        """Simula um erro de banco de dados (email duplicado)"""
        # Configura o Mock para lançar erro de Integridade
        mock_conn = MagicMock()
        mock_get_db.return_value = mock_conn
        mock_conn.execute.side_effect = sqlite3.IntegrityError("Email duplicado")

        response = self.app.post('/cadastro', data=dict(
            nome='Hacker',
            email='admin@email.com', 
            senha='123',
            termos='on'
        ), follow_redirects=True)

        html = response.data.decode('utf-8')
        # Verifica se a mensagem de erro aparece
        self.assertIn('Este email já', html)

    def test_validacao_termos_uso(self):
        """Testa a lógica de validação sem tocar no banco"""
        response = self.app.post('/cadastro', data=dict(
            nome='Sem Termos',
            email='semtermos@teste.com',
            senha='123'
            # Faltou o campo 'termos'
        ), follow_redirects=True)

        html = response.data.decode('utf-8')
        self.assertIn('precisa aceitar os termos', html)

if __name__ == '__main__':
    unittest.main()