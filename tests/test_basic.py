import unittest, sys

sys.path.append('../GlobalLingo') # imports python file from parent directory
from app import app # imports flask app object

class BasicTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        self.app = app.test_client()

    def test_home_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_translator_page(self):
        response = self.app.get('/translator', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
