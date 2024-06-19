import pymongo
from flask import Flask, request, jsonify
from bson import ObjectId
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# Enable CORS for all routes

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["bookstore"]

@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    result = db.books.insert_one(data)
    book_id = result.inserted_id
    return jsonify({'_id': str(book_id)}), 201

@app.route('/books', methods=['GET'])
def get_books():
    books = list(db.books.find())
    for book in books:
        book['_id'] = str(book['_id'])
    return jsonify(books), 200

@app.route('/book/<id>', methods=['GET'])
def get_book(id):
    book = db.books.find_one({'_id': ObjectId(id)})
    if book:
        book['_id'] = str(book['_id'])
        return jsonify(book), 200
    else:
        return jsonify({'message': 'Book not found'}), 404

@app.route('/book/<id>', methods=['PUT'])
def update_book(id):
    data = request.get_json()
    updated_book = db.books.update_one({'_id': ObjectId(id)}, {'$set': data})
    if updated_book.modified_count > 0:
        return jsonify({'_id': str(id), 'message': 'Book updated successfully'}), 200
    else:
        return jsonify({'message': 'Book not found'}), 404

@app.route('/book/<id>', methods=['DELETE'])
def delete_book(id):
    result = db.books.delete_one({'_id': ObjectId(id)})
    if result.deleted_count > 0:
        return jsonify({'_id': str(id), 'message': 'Book deleted successfully'}), 200
    else:
        return jsonify({'message': 'Book not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
