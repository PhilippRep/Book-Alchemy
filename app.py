
from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime
from data_models import db, Author, Book


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"
db.init_app(app)

with app.app_context():
  db.create_all()


@app.route('/')
def home():
    search = request.args.get('search')
    sort_by = request.args.get('sort_by')
    query = Book.query
    if search:
        query = query.filter(Book.title.ilike(f"%{search}%"))
    if sort_by == 'author':
        query = query.join(Author).order_by(Author.name)
    else:
        query = query.order_by(Book.title)
    books = query.all()
    message = None
    if search and not books:
        message = "No Books found!"
    api_url = "https://openlibrary.org/api/books?bibkeys=ISBN:9780451526538&format=json&jscmd=data"

    return render_template('home.html', books=books, message=message)

@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method== 'POST':
        name = request.form.get('name')
        birth_date = request.form.get('birthdate')
        date_birth_obj = datetime.strptime(birth_date, "%Y-%m-%d").date()
        date_of_death = request.form.get('date_of_death')
        date_death_obj = datetime.strptime(date_of_death, "%Y-%m-%d").date()
        new_author = Author(name = name,
               birth_date = date_birth_obj,
               date_of_death = date_death_obj)
        db.session.add(new_author)
        db.session.commit()
        print(f"Author:{name} successfully created")
        return redirect(url_for('home'))

    return render_template('add_author.html')

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method== 'POST':
        isbn = request.form.get('isbn')
        title = request.form.get('title')
        publication_year = request.form.get('publication_year')
        author_id = int(request.form.get('author_id'))
        new_book = Book(title = title,
               isbn = isbn,
               publication_year = int(publication_year),
               author_id = author_id
        )
        db.session.add(new_book)
        db.session.commit()
        print(f"Book:{title} successfully created")
        redirect(url_for('home'))
    authors = Author.query.all()
    return render_template('add_book.html', authors=authors)

@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()

    print(f"Book: {book.title} is deleted")
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)