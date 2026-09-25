from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books-collection.db"
db.init_app(app)

class Book(db.Model):
    __tablename__ = "books"


    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True, nullable=False)
    author: Mapped[str] = mapped_column(nullable=False)
    review: Mapped[float] = mapped_column(nullable=False)

with app.app_context():
    db.create_all()




with app.app_context():
    result = db.session.execute(db.select(Book).order_by(Book.title))
    all_books = result.scalars().all()



@app.route('/')
def home():
    with app.app_context():
        result = db.session.execute(db.select(Book).order_by(Book.title))
        all_books = result.scalars().all()

    return render_template("index.html",books = all_books)


@app.route("/add",methods=["GET","POST"])
def add():
    if request.method == 'POST':
        book_name = request.form.get('book_name')
        book_author = request.form.get('book_author')
        rating = request.form.get('rating')
        with app.app_context():
            new_book = Book(title=book_name, author=book_author, review=rating)
            db.session.add(new_book)
            db.session.commit()




    return render_template("add.html")


@app.route("/edit/<int:id>",methods=["GET","POST"])
def edit(id):
    if request.method == 'POST':
        new_review = request.form.get('rating')
        with app.app_context():
            book_to_update = db.session.execute(db.select(Book).where(Book.id == id)).scalar()

            book_to_update.review = new_review
            db.session.commit()
        with app.app_context():
            book = db.session.execute(db.select(Book).where(Book.id ==id)).scalar()

        return render_template("edit.html",book=book)
    else:
        with app.app_context():
            book = db.session.execute(db.select(Book).where(Book.id ==id)).scalar()
        return render_template("edit.html",book = book)

@app.route("/delete/")
def delete():
  book_id = request.args.get("id")  # Captura el ?id=3 de la URL
  with app.app_context():
    book_to_delete = db.get_or_404(Book, book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
  return redirect(url_for("home"))




if __name__ == "__main__":
    app.run(debug=True)
