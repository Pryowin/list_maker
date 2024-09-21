import unittest
from unittest.mock import patch, MagicMock

from app import app
from lists.headers.validations import is_list_definition_valid, is_category_valid, Category, ADMIN_USER

class TestListHeaderMethods(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()

    
    def tearDown(self):
        self.app_context.pop()
    
    
    def test_valid_definition(self):    
        definition = {"Title": "String", "Artist": "String", "year": "int", "price": "num"}
        self.assertTrue(is_list_definition_valid(definition))
    
    
    def test_invalid_definition(self):
        definition = {"Title": "String", "Artist": "String", "year": "int", "price": "dollars"}
        self.assertFalse(is_list_definition_valid(definition))
    
    
    def test_No_string_definition(self):
        definition = {"Number": "int"}
        self.assertFalse(is_list_definition_valid(definition))
        
        
    def test_empty_definition(self):
        definition = {}
        self.assertFalse(is_list_definition_valid(definition))
    
        
    @patch('lists.headers.validations.Category.query')
    def test_category_not_found(self, mock_query):
        mock_query.filter_by.return_value.first.return_value=None
        result = is_category_valid(user_id=1, category_id=999)
        self.assertFalse(result)
    
    
    @patch('lists.headers.validations.Category.query')
    def test_category_created_by_admin(self, mock_query):
        mock_category = MagicMock()
        mock_category.category_id = 2
        mock_category.created_by = 1
        mock_query.filter_by.return_value.first.return_value = mock_category

        result = is_category_valid(user_id=3, category_id=2)
        self.assertTrue(result)
    
    
    @patch('lists.headers.validations.Category.query')
    def test_category_created_by_user(self, mock_query):
        mock_category = MagicMock()
        mock_category.category_id = 9
        mock_category.created_by = 2
        mock_query.filter_by.return_value.first.return_value = mock_category

        result = is_category_valid(user_id=2, category_id=9)
        self.assertTrue(result)
    
    
    @patch('lists.headers.validations.Category.query')    
    def test_category_created_by_other_user(self, mock_query):
        mock_category = MagicMock()
        mock_category.category_id = 9
        mock_category.created_by = 3
        mock_query.filter_by.return_value.first.return_value = mock_category

        result = is_category_valid(user_id=2, category_id=9)
        self.assertFalse(result)
    
if __name__ == '__main__':
    unittest.main()