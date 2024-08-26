import unittest
from password.methods import encrypt, verify, is_password_valid


class TestPasswordMethods(unittest.TestCase):
    
    def test_pwd_encrypt(self):
        self.assertNotEqual(encrypt('password'), 'password')
        
    
    def test_pwd_verify_matches(self):
        stored_password = encrypt('password')
        self.assertTrue(verify('password', stored_password ))
    
    
    def test_pwd_verify_does_not_match(self):
        stored_password = encrypt('password')
        self.assertFalse(verify('Password', stored_password))
    
    
    def test_password_invalid(self):
        self.assertFalse(is_password_valid("ABCd1??"),msg="Length check failed with seven characters")
        self.assertFalse(is_password_valid("ABCd1??" + "m" * 26),msg="Length check failed with more than 32 characters")
        self.assertFalse(is_password_valid("ABCd1234"), msg= "Special character check failed")
        self.assertFalse(is_password_valid("ABCd????"), msg= "Number check failed")
        self.assertFalse(is_password_valid("abcd12???"), msg= "Upper case check failed")
        self.assertFalse(is_password_valid("ABCD12???"), msg= "Lower case check failed")
        
    
    def test_password_valid(self):
        self.assertTrue(is_password_valid("BaCd12=,"), msg="Valid password rejected")
    
if __name__ == '__main__':
    unittest.main()