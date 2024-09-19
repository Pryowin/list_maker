import unittest

from lists.headers.validations import is_list_definition_valid

class TestListHeaderMethods(unittest.TestCase):
    
    def test_valid_definition(self):
        
        definition = {"Title": "String", "Artist": "String", "year": "int", "price": "num"}
        self.assertTrue(is_list_definition_valid(definition))
    
    def test_invalid_definition(self):
        definition = {"Title": "String", "Artist": "String", "year": "int", "price": "dollars"}
        self.assertFalse(is_list_definition_valid(definition))
        
    def test_empty_definition(self):
        definition = {}
        self.assertFalse(is_list_definition_valid(definition))
        
if __name__ == '__main__':
    unittest.main()