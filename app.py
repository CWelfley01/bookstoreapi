from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')

db = SQLAlchemy(app)
ma = Marshmallow(app)

CORS(app)


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String, nullable=False)
    img_url = db.Column(db.String, nullable=False)

    def __init__(self, name, price, author, description, img_url):
        self.name = name
        self.price = price
        self.author = author
        self.description = description
        self.img_url = img_url

class BookSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "price", "author", "description", "img_url")

book_schema = BookSchema()
books_schema = BookSchema(many=True)

@app.route("/book/add", methods=["POST"])
def add_book():
    name = request.json.get("name")
    author = request.json.get("author")
    description = request.json.get("description")
    price = request.json.get("price")
    img_url = request.json.get("img_url")

    record = Books(name, price, author, description, img_url)
    
    db.session.add(record)
    db.session.commit()

    return jsonify(book_schema.dump(record))

@app.route("/books", methods=["GET"])
def get_all_books():
    all_books = Books.query.all()
    return jsonify(books_schema.dump(all_books))

@app.route("/book/<id>", methods=["DELETE","GET","PUT"])
def book_id(id):
    book = Books.query.get(id)
    if request.method == "DELETE":
        db.session.delete(book)
        db.session.commit()
    
        return book_schema.jsonify(book)
    elif request.method == "PUT":
        name = request.json['name']
        author = request.json['author']
        price = request.json['price']
        description = request.json['description']
        img_url = request.json['img_url']

        book.name = name
        book.author = author
        book.price = price
        book.description = description
        book.img_url = img_url

        db.session.commit()
        return book_schema.jsonify(book)
    elif request.method == "GET":
        return book_schema.jsonify(book)



if __name__ == "__main__":
    app.run(debug=True)
