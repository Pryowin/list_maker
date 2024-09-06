from flask import Flask
from users.models import db, User
from password.methods import encrypt
from datetime import date
import os

def create_app():
    app = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'connections.db')
    db.init_app(app)

    @app.cli.command('db_create')
    def db_create():
        db.create_all()
        print('Database Created')

    @app.cli.command('db_drop')
    def db_drop():
        db.drop_all()
        print('Database dropped')
        
    
    @app.cli.command('db_seed')
    def db_seed():    
        test_user = User(user_name='Pyrowin',
                         password = encrypt('P@ssw0rd'),
                         first_name='David',
                         last_name='Burke',
                         date_of_birth= date(1965,1,12),
                         email='test@test.com',
                         phone='9106261234'
                        )

        db.session.add(test_user)
        db.session.commit()
        
        print('Database seeded')
    
    

    return app