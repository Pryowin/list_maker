import unittest

from config.methods import is_valid_country, is_valid_region

class TestConfigMethods(unittest.TestCase):

    def test_valid_country(self):
        self.assertTrue(is_valid_country('USA'))
        self.assertTrue(is_valid_country('CAN'))
        
    def test_invalid_country(self):
        self.assertFalse(is_valid_country('GBR'))
        
    def test_valid_region(self):
        self.assertTrue(is_valid_region('USA', 'NC'))
        self.assertTrue(is_valid_region('CAN', 'ON'))
        
    def test_invalid_region(self):
        self.assertFalse(is_valid_region('USA', 'ON'))
        self.assertFalse(is_valid_region('CAN', 'AL'))
        self.assertFalse(is_valid_region('GBR', 'CT'))

if __name__ == '__main__':
    unittest.main()