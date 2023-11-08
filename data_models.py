from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
Base = db.Model


class Author(Base):
    """
    Represents an author in the library database.

    Attributes:
        id (int): The unique identifier for the author.
        name (str): The name of the author.
        birth_date (date): The birthdate of the author.
        date_of_death (date): The date of death of the author, if applicable.
    """
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    birth_date = db.Column(db.Date)
    date_of_death = db.Column(db.Date)

    def __repr__(self):
        return f"Author(id={self.id}, name='{self.name}', birth_date={self.birth_date}, date_of_death={self.date_of_death})"


class Book(Base):
    """
    Represents a book in the library database.

    Attributes:
        id (int): The unique identifier for the book.
        isbn (str): The International Standard Book Number of the book.
        title (str): The title of the book.
        publication_year (int): The year when the book was published.
        author_id (int): The Foreign Key of the author's id number based on the authors' table.
        author (string): The list of authors  from the authors' table.
    """
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    publication_year = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)
    author = db.relationship('Author', backref='books')

    def __repr__(self):
        return f"Book(id={self.id}, isbn='{self.isbn}', title='{self.title}', publication_year={self.publication_year}, author_id={self.author_id})"
