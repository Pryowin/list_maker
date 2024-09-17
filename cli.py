import click
from flask.cli import with_appcontext
from datetime import date
from users.models import User
from lists.models import db,Category
from password.methods import encrypt

@click.command('db_create')
@with_appcontext
def db_create():
    db.create_all()
    print('Database Created')

@click.command('db_drop')
@with_appcontext
def db_drop():
    db.drop_all()
    print('Database dropped')

@click.command('db_seed')
@with_appcontext
def db_seed():
    test_user = User(user_name='admin',
                     password=encrypt('P@ssw0rd'),
                     first_name='David',
                     last_name='Burke',
                     date_of_birth=date(1965, 1, 12),
                     email='test@test.com'
                     )
    db.session.add(test_user)
    db.session.commit()
    
    categories = ['Books', 'Films', 'Music', 'Miscellaneous', 'Places','Sport', 'TV']
    for category in categories:
        init_category = Category(created_by=1, category_name = category)
        db.session.add(init_category)
        
    db.session.commit()
    print('Database seeded')
    
    