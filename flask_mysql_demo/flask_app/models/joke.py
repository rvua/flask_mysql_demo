from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User

class Joke:
    def __init__(self,data):
        self.id = data['id']
        self.comedian = data['comedian']
        self.joke = data['joke']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def insert_joke(cls,data):
        query="INSERT INTO jokes (comedian,joke,user_id) VALUES (%(comedian)s,%(joke)s,%(user_id)s)"  
        return connectToMySQL("joke_mill").query_db(query,data)

    @classmethod
    def get_users_jokes(cls):
        query="SELECT * FROM users JOIN jokes ON users.id = jokes.user_id ORDER BY jokes.created_at DESC"  
        users_jokes_db = connectToMySQL("joke_mill").query_db(query)
        users_jokes = []

        for uj in users_jokes_db:
            user_instance = User(uj)
            joke_data = {
                "id":uj["jokes.id"],
                "comedian":uj["comedian"],
                "joke":uj["joke"],
                "user_id":uj["user_id"],
                "created_at":uj["created_at"],
                "updated_at":uj["updated_at"]
            }
            user_instance.joke = Joke(joke_data)
            users_jokes.append(user_instance)            
        
        return users_jokes

    @classmethod
    def user_jokes(cls,data):
        query="SELECT * FROM users JOIN jokes ON users.id = jokes.user_id WHERE users.id = %(user_id)s"  
        user_jokes_db = connectToMySQL("joke_mill").query_db(query,data)
        user = User(user_jokes_db[0])

        for uj in user_jokes_db:
            joke_data = {
                "id":uj["jokes.id"],
                "comedian":uj["comedian"],
                "joke":uj["joke"],
                "user_id":uj["user_id"],
                "created_at":uj["created_at"],
                "updated_at":uj["updated_at"]
            }
            user.jokes.append(Joke(joke_data))
        
        return user

    @classmethod
    def delete_joke(cls,data):
        query="DELETE FROM jokes WHERE id=%(id)s"  
        return connectToMySQL("joke_mill").query_db(query,data)

    
    @staticmethod
    def validate_joke(joke):
        is_valid = True
        if len(joke["comedian"]) < 3:
            flash("Comedian name needs to be more than 3 characters")
            is_valid = False
        if len(joke["joke"]) < 5:
            flash("Joke needs to be more than 5 characters")
            is_valid = False
        
        return is_valid
