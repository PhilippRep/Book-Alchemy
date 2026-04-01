from flask import Flask, render_template, request, redirect, url_for
import os
from data_models import db, Author, Book

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"
db.init_app(app)

with app.app_context():
  db.create_all()

@app.route('/')
def home():
    return render_template('home.html'), 200

@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method== 'POST':
        name = request.form.get('name')
        birthdate = request.form.get('birthdate')
        date_of_death = request.form.get('date_of_death')
        new_author = Author(name = name,
               birth_of_date = birthdate,
               date_of_death = date_of_death)
        db.session.add(new_author)
        db.session.commit()
        print(f"Author:{name} successfully created")
        return redirect(url_for('home'))

    return render_template('add_author.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)