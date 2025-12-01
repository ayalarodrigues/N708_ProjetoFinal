import unittest
import sys
import os

# Configuração para importar o app.py da pasta backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend/src')))

from app import app, init_db, get_db_connection

class BibliotecaTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        with app.app_context():
            init_db()

    def test_home_redirect(self):
        # Testa se quem não tá logado é jogado pro login
        response = self.app.get('/', follow_redirects=True)
        self.assertIn(b'Login', response.data)

    def test_page_load(self):
        # Testa se a página de login carrega (código 200)
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()