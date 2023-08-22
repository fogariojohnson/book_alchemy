from flask import Flask, render_template, request, redirect, url_for
from data_models import db, Author, Book
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/myste/PycharmProjects/book-alchemy/data/library.sqlite'
db.init_app(app)


@app.route('/', methods=['GET'])
def home():
    """
    Allows user to view the list of books, sort books, and delete books.

    Returns:
        home.html(html file): Uses the home template.
    """
    sort_by = request.args.get('sort_by', default=None, type=str)
    search_term = request.args.get('search', default=None, type=str)

    if search_term:
        books = Book.query.filter(Book.title.like(f'%{search_term}%')).all()
    elif sort_by == 'title':
        books = Book.query.order_by(Book.title).all()
    elif sort_by == 'author':
        books = Book.query.join(Author, Book.author_id == Author.id).order_by(Author.name).all()
    else:
        books = Book.query.join(Author, Book.author_id == Author.id).all()
    success_message = request.args.get('success_message', default=None, type=str)
    return render_template('home.html', books=books, success_message=success_message)


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """
    Allows user to add an author, birthdate and date of death if available.
    It will automatically assign an author id.

    Returns:
        add_author.html(html file): Uses the add_author template.
    """
    if request.method == 'POST':
        name = request.form['name']
        birth_date = datetime.strptime(request.form['birth_date'], '%Y-%m-%d').date()
        date_of_death = datetime.strptime(request.form['date_of_death'], '%Y-%m-%d').date() if request.form['date_of_death'] else None
        new_author = Author(name=name, birth_date=birth_date, date_of_death=date_of_death)
        db.session.add(new_author)
        db.session.commit()
        success_message = "Author added successfully!"
        return render_template('add_author.html', success_message=success_message)
    return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """
    Allows user to add a book, its isbn, publication year and shows options of authors.

    Returns:
        add_book.html(html file): Uses the add_book template.
    """
    authors = Author.query.all()
    if request.method == 'POST':
        title = request.form['title']
        isbn = request.form['isbn']
        publication_year = int(request.form['publication_year'])
        author_id = request.form.get('author_id', type=int)
        new_book = Book(title=title, isbn=isbn, publication_year=publication_year, author_id=author_id)
        db.session.add(new_book)
        db.session.commit()
        success_message = "Book added successfully!"
        return render_template('add_book.html', success_message=success_message, authors=authors)
    return render_template('add_book.html', authors=authors)


@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    """
    Allows user to delete a book listed.

    Returns:
        home.html(html file): It gets redirected to the home.html url.
    """
    book = Book.query.get_or_404(book_id)
    author = book.author

    db.session.delete(book)
    if not author.books:
        db.session.delete(author)

    db.session.commit()

    success_message = "Book deleted successfully!"
    return redirect(url_for('home', success_message=success_message))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist

    app.run()
    app.run(host="0.0.0.0", port=5000, debug=True)
