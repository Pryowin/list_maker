import unittest
from datetime import datetime, timedelta,date

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from users.methods import generate_confirmation_code, has_code_expired, is_user_old_enough,is_valid_date, is_valid_postal_code, is_invalid_email
from users.models import db,Token
from application.constants import MIN_AGE

import os


class TestUserMethods(unittest.TestCase):
            
    def test_confirmation_code(self):
        self.assertEqual(len(generate_confirmation_code()), 6)    
    
    
    def test_has_code_expired_yes(self):
        then = datetime.now() - timedelta(seconds=30)
        self.assertTrue(has_code_expired(then, 29))
    
    
    def test_has_code_expired_no(self):
        then = datetime.now() - timedelta(seconds=3)
        self.assertFalse(has_code_expired(then, 29))
        
    def test_user_is_underage(self):
        date_of_birth = date(datetime.now().year - MIN_AGE, datetime.now().month, datetime.now().day + 1)
        self.assertFalse(is_user_old_enough(date_of_birth))
        
    def test_user_is_old_enough(self):
        date_of_birth = date(datetime.now().year - MIN_AGE, datetime.now().month, datetime.now().day)
        self.assertTrue(is_user_old_enough(date_of_birth))
        
    def test_is_valid_date(self):
        self.assertTrue(is_valid_date('1965-01-12'))
        self.assertFalse(is_valid_date('1965-02-29'))
        
    def test_is_valid_zip_US(self):
        self.assertTrue(is_valid_postal_code('27376', "USA"))
        self.assertFalse(is_valid_postal_code('273761',"USA"))
        self.assertFalse(is_valid_postal_code('27A76', "USA"))
        
    def test_is_valid_zip_CAN(self):
        self.assertTrue(is_valid_postal_code('L1A 9L9', "CAN"))
        self.assertFalse(is_valid_postal_code('27376',"CAN"))
        self.assertFalse(is_valid_postal_code('W1A 9L9', "CAN"))
        self.assertFalse(is_valid_postal_code('L1A9L9', "CAN"))
        self.assertFalse(is_valid_postal_code('L1A 9I9', "CAN"))
    
        
    def test_is_invalid_email(self):
        self.assertTrue(is_invalid_email('david.co.uk'))
        self.assertTrue(is_invalid_email('david@co'))
        self.assertFalse(is_invalid_email('david@co.uk'))
        self.assertFalse(is_invalid_email('david+123@co.uk'))
            
if __name__ == '__main__':
    unittest.main()