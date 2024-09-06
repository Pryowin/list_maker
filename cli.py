import click
from flask.cli import with_appcontext
from users.models import db, User
from password.methods import encrypt
from datetime import date

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
    test_user = User(user_name='Pyrowin',
                     password=encrypt('P@ssw0rd'),
                     first_name='David',
                     last_name='Burke',
                     date_of_birth=date(1965, 1, 12),
                     email='test@test.com'
                     )
    db.session.add(test_user)
    db.session.commit()
    print('Database seeded')