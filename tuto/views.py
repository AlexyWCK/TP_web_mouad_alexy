from .app import *
from flask import render_template, flash, redirect, request, url_for
from .models import get_sample, get_author, AuthorForm, RegistrationForm, LoginForm
from .app import db
from .models import Author, Book, User
from flask import request
from flask_login import login_user, logout_user, login_required,current_user
from flask_wtf import FlaskForm
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


@app.route("/")
def home():
    return render_template("home.html", title="My Books !", books=get_sample(), bootstrap=bootstrap)

@app.route("/detail/<id>")
def detail(id):
    try:
        books = get_sample()  # ou `Book.query.all()` si tu utilises une base de données
        book = books[int(id) - 1]
        return render_template("detail.html", book=book)
    except IndexError:
        return render_template("404.html"), 404

@app.route("/edit/author/<int:id>")
def edit_author(id):
    a = get_author(id)
    if a is None:
        flash('Auteur non trouvé.', 'danger')
        return redirect(url_for('authors'))

    f = AuthorForm(id=a.id, name=a.name)
    return render_template("edit-author.html", author=a, form=f)

@app.route("/save/author/", methods=("POST",))
@login_required
def save_author():
    f = AuthorForm()
    if f.validate_on_submit():
        id = int(f.id.data)
        a = get_author(id)
        if a is None:
            flash('Auteur non trouvé.', 'danger')
            return redirect(url_for('authors'))

        a.name = f.name.data
        db.session.commit()
        flash('Auteur modifié avec succès.', 'success')
        return redirect(url_for('authors'))  # Redirection vers la liste des auteurs
    
    flash('Erreur lors de la validation du formulaire.', 'danger')
    return render_template("edit-author.html", form=f)

@app.route("/authors")
def authors():
    return render_template("authors.html", authors=Author.query.all())

@app.route("/add/author", methods=("GET", "POST"))
@login_required
def add_author():
    f = AuthorForm()
    if f.validate_on_submit():
        a = Author(name=f.name.data)
        db.session.add(a)
        db.session.commit()
        flash('Auteur ajouté avec succès.', 'success')
        return redirect(url_for('authors'))  # Redirection vers la liste des auteurs après ajout
    
    return render_template("ajouter_auteur.html", form=f)

@app.route("/delete/author", methods=["POST"])
@login_required
def delete_author():
    id = request.form.get('id')
    a = get_author(int(id))
    if a:
        db.session.delete(a)
        db.session.commit()
        flash('Auteur supprimé avec succès.', 'success')
    else:
        flash('Auteur non trouvé.', 'danger')  # Ajout d'un message d'erreur si l'auteur n'existe pas
    return redirect(url_for('authors'))  # Redirection vers la liste des auteurs

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get('query')
    authors = Author.query.filter(Author.name.like(f'%{query}%')).all()
    books = []
    for author in authors:
        author_books = Book.query.filter(Book.author_id == author.id).all()
        books.extend(author_books)
    
    return render_template("search_results.html", books=books, query=query)

@app.route("/login/", methods=("GET", "POST"))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()  

        if user is None:
            error_message = "Nom d'utilisateur incorrect."
            return render_template('login.html', error=error_message)
        else:
            if user.password == password:  # Simple comparaison sans sécurité
                login_user(user)
                return redirect(url_for('home'))  
            else:
                error_message = "Mot de passe incorrect."
                return render_template('login.html', error=error_message)

    return render_template('login.html')

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user_existant = User.query.filter_by(username=form.username.data).first()
        if user_existant:
            form.username.errors.append("Ce nom d'utilisateur est déjà utilisé.")
            return render_template('register.html', form=form)

        user = User(username=form.username.data, password=form.password.data)
        
        db.session.add(user)
        db.session.commit()  
        
        return render_template('login.html', form=form)
    return render_template('register.html', form=form)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) 

@app.route('/logout')
@login_required
def logout():
    logout_user()  
    return redirect(url_for('login'))

@app.route("/authors/sort")
def sort_authors():
    authors = Author.query.order_by(Author.name).all()
    return render_template("authors.html", authors=authors)
