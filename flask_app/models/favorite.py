from sqlite3 import connect
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

db_name = 'undead_organizer_schema'

# model the class after the table from our database
class Favorite:
    def __init__( self , data ):
        self.id = data['id']
        self.title = data['title']
        self.year = data['year']
        self.director = data['director']
        self.movie_series = data['movie_series']
        self.rating = data['rating']
        self.imdb_link = data['imdb_link']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.ranking_list = []

    @classmethod
    def get_all_favorites(cls):
        query = "SELECT * FROM favorites JOIN users ON users.id = favorites.user_id"
        results = connectToMySQL(db_name).query_db(query)
        favorites = []
        for row in results:
            favorites.append(cls(row))
        return favorites

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM favorites ORDER BY rating DESC;"
        results = connectToMySQL(db_name).query_db(query)
        favorites = []
        for favorite in results:
            favorites.append( cls(favorite) )
        # favorites.sort(reverse=True)
        return favorites

    @classmethod
    def create(cls, data):
        query = "INSERT INTO favorites ( title , year , director , movie_series , rating , imdb_link , user_id) VALUES (%(title)s, %(year)s, %(director)s, %(movie_series)s, %(rating)s, %(imdb_link)s, %(user_id)s);"
        return connectToMySQL(db_name).query_db(query, data)

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM favorites WHERE id = %(id)s";
        result = connectToMySQL(db_name).query_db(query, data)
        return cls(result[0])

    @classmethod
    def update(cls, data):
        query = "UPDATE favorites SET title=%(title)s, year=%(year)s, director=%(director)s, movie_series=%(movie_series)s, rating=%(rating)s , rating=%(rating)s , updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(db_name).query_db(query, data)

    @classmethod
    def destroy(cls,data):
        query  = "DELETE FROM favorites WHERE id = %(id)s;"
        return connectToMySQL(db_name).query_db(query,data)

    #Function for validations
    @staticmethod
    def validate_title(x):
        is_valid = True
        if len(x['title']) < 1:
            flash("Title must be at least 1 characters.")
            is_valid = False
        if len(x['year']) < 4:
            flash("Year must be at least 4 numbers.")
        if len(x['director']) < 2:
            flash("Director name must be at least 2 characters.")
            is_valid = False
        if x['movie_series'] != "Series" and x['movie_series'] != "Movie":
            flash("Must select movie or series.")
            is_valid = False
        if x['rating'] == "":
            flash("Must select rating.")
            is_valid = False
        return is_valid

    # @classmethod
    # def rank_by_fav(cls , data):
    #     query = "SELECT * FROM favorites WHERE rating = %(rating)s";
    #     results = connectToMySQL(db_name).query_db(query,data)
    #     favorites = []
    #     print(results)
    #     for favorite in results:
    #         favorites.append( cls(favorite) )
    #     favorites.sort(reverse=True)
    #     return favorites