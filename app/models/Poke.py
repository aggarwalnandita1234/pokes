""" 
    Sample Model File

    A Model should be in charge of communicating with the Database. 
    Define specific model method that query the database for information.
    Then call upon these model method in your controller.

    Create a model using this template.
"""
from system.core.model import Model
import re

class Poke(Model):
    def __init__(self):
        super(Poke, self).__init__()
    def create_user(self, info):
        # We write our validations in model functions.
        # They will look similar to those we wrote in Flask
        EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        errors = []
        # Some basic validation
        if not info['name']:
            errors.append('First Name cannot be blank')

        elif len(info['name']) < 2:
            errors.append('First Name must be at least 2 characters long')
        
        if not info['email']:
            errors.append('Email cannot be blank')
        elif not EMAIL_REGEX.match(info['email']):
            errors.append('Email format must be valid!')
        if not info['password']:
            errors.append('Password cannot be blank')
        elif len(info['password']) < 8:
            errors.append('Password must be at least 8 characters long')
        elif info['password'] != info['pw_confirmation']:
            errors.append('Password and confirmation must match!')
        # If we hit errors, return them, else return True.
        if errors:

            return {"status": False, "errors": errors}
        else:
            pw_hash = self.bcrypt.generate_password_hash(info['password'])
   
            query_insert="INSERT INTO users (name, alias, email, password) VALUES (:name, :alias, :email, :password)"
            data={'name':info['name'],'alias':info['alias'], 'email':info['email'],'password':pw_hash}
            self.db.query_db(query_insert, data)

            get_user_query = "SELECT * FROM users ORDER BY id DESC LIMIT 1"
            users = self.db.query_db(get_user_query)
    
            status = { "status": True, "user": users[0] }
            return status

    def login(self, info):

        errors = []

        query_login = "SELECT * FROM users WHERE email = :email LIMIT 1"
        data = { 'email': info['email'] }

        user = self.db.query_db(query_login, data)

        if user == []:
            print "no user"
            errors.append('Invalid login!')
            return{"status": False, "errors": errors}
        else:
            if self.bcrypt.check_password_hash(user[0]['password'], info['password']):
                print "password matched"
                return {"status": True, "user": user[0] }
            else:
                print "password not matched"
                errors.append('Invalid login!')
                return{"status": False, "errors": errors}

    def get_users(self, info):
        query="SELECT * FROM users where not users.id=:id"
        data={'id':info}
        return self.db.query_db(query, data)

    def update_poke(self, info):
        query="UPDATE users SET poke_history=:poke_history where users.id=:id"
        data={'id':info['id'],
        'poke_history':info['pokes']}

        return self.db.query_db(query, data)
    def add_poke(self, info):
        query="INSERT INTO pokes (user_id, poked_by, num_pokes)VALUES(:id, :poked_by, :poke_history)"
        data={'id':info['id'],
        'poke_history':info['pokes'],
        'poked_by':info['poked_by']}
        return self.db.query_db(query, data)

    def get_pokes(self, info):
        query="SELECT count(pokes.poked_by) as n, users.name as name FROM pokes JOIN users ON pokes.poked_by= users.id where pokes.user_id=:id group by poked_by"
        data={'id':info}
        return self.db.query_db(query, data)

    def get_total_pokes(self, info):
        query="select count(*) as n1 from (select poked_by from pokes where pokes.user_id=:id group by poked_by) as s"
        data={'id':info}
        return self.db.query_db(query, data)












