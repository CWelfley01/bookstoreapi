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

    def __init__(self, name, price, author, description):
        self.name = name
        self.price = price
        self.author = author
        self.description = description

class BookSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "price", "author", "description")

book_schema = BookSchema()
books_schema = BookSchema(many=True)

@app.route("/book/add", methods=["POST"])
def add_book():
    name = request.json.get("name")
    author = request.json.get("author")
    description = request.json.get("description")
    price = request.json.get("price")

    record = Books(name, price, author, description)
    
    db.session.add(record)
    db.session.commit()

    return jsonify(book_schema.dump(record))

@app.route("/book/get", methods=["GET"])
def get_all_books():
    all_books = Books.query.all()
    return jsonify(books_schema.dump(all_books))




if __name__ == "__main__":
    app.run(debug=True)
