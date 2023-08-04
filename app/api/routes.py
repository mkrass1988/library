from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Library, book_schema, books_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/books', methods = ['POST'])
@token_required
def add_book(current_user_token):
    isbn = request.json['isbn']
    author = request.json['author']
    title = request.json['title']
    length = request.json['length']
    cover = request.json['cover']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    book = Library(isbn, author, title, length, cover, user_token = user_token )

    db.session.add(book)
    db.session.commit()

    response = book_schema.dump(book)
    return jsonify(response)

@api.route('/library', methods = ['GET'])
@token_required
def get_library(current_user_token):
    a_user = current_user_token.token
    library = Library.query.filter_by(user_token = a_user).all()
    response = books_schema.dump(library)
    return jsonify(response)

@api.route('/library/<id>', methods = ['GET'])
@token_required
def get__single_book(current_user_token, id):
    book = Library.query.get(id)
    response = book_schema.dump(book)
    return jsonify(response)

@api.route('/library/<id>', methods = ['POST','PUT'])
@token_required
def update_book(current_user_token,id):
    book = Library.query.get(id) 
    book.isbn = request.json['isbn']
    book.author = request.json['author']
    book.title = request.json['title']
    book.length = request.json['length']
    book.cover = request.json['cover']
    book.user_token = current_user_token.token

    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)

@api.route('/library/<id>', methods = ['DELETE'])
@token_required
def delete_book(current_user_token, id):
    book = Library.query.get(id)
    db.session.delete(book)
    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)