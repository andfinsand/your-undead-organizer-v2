from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.favorite import Favorite
from flask_app.models.user import User

# Main favorites

@app.route('/main')
def favorites():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    favorites = Favorite.get_all()
    return render_template('main/main.html' , user=User.get_by_id(data) , favorites = favorites)

# Add new title

@app.route('/new_title')
def add_new_title():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
    "id":session['user_id']
    }
    return render_template('main/new_title.html' , user = User.get_by_id(data))

# Process new title form

@app.route('/process_new_title' , methods=['POST'])
def process_new_title():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Favorite.validate_title(request.form):
        return redirect ('/new_title')
    data = {
        "title":  request.form['title'],
        "year" : request.form['year'],
        "director": request.form['director'],
        "movie_series": request.form['movie_series'],
        "rating": request.form["rating"],
        "imdb_link": request.form["imdb_link"],
        "user_id": session["user_id"]
    }
    # id = Favorite.create(request.form)
    # return redirect(f'/main/{id}')
    Favorite.create(data)
    return redirect('/main')

# Edit favorite

@app.route('/main/edit/<int:id>')
def edit(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    return render_template('main/edit.html', edit = Favorite.get_by_id(data))

# Process edit form

@app.route('/main/process_edit', methods=['POST'])
def update():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Favorite.validate_title(request.form):
        page = request.form['id']
        return redirect (f'/main/edit/{page}')
    data = {
        "title":  request.form['title'],
        "year" : request.form['year'],
        "director": request.form['director'],
        "movie_series": request.form['movie_series'],
        "rating": request.form["rating"],
        "imdb_link": request.form["imdb_link"],
        "user_id": session["user_id"]
    }
    Favorite.update(data)
    return redirect('/main')

# Delete favorite

@app.route('/destroy/<int:id>')
def destroy(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': id
    }
    Favorite.destroy(data)
    return redirect('/main')