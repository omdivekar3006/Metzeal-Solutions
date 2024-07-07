from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from hashlib import md5
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///transactions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numbers = db.Column(db.String(500), nullable=False)
    result = db.Column(db.Float, nullable=False)
    hash_key = db.Column(db.String(64), unique=True, nullable=False)

    def __repr__(self):
        return f'<Transaction {self.id}>'

# Create the tables if they don't exist
with app.app_context():
    db.create_all()

@app.route('/sum', methods=['POST'])
def compute_sum():
    data = request.get_json()
    numbers = data.get('numbers')

    if not isinstance(numbers, list) or not all(isinstance(n, (int, float)) for n in numbers):
        return jsonify({'error': 'Invalid input, must be a list of numbers'}), 400

    numbers_str = json.dumps(numbers, sort_keys=True)
    hash_key = md5(numbers_str.encode()).hexdigest()

    existing_transaction = Transaction.query.filter_by(hash_key=hash_key).first()

    if existing_transaction:
        result = existing_transaction.result
    else:
        result = sum(numbers)
        new_transaction = Transaction(numbers=numbers_str, result=result, hash_key=hash_key)
        db.session.add(new_transaction)
        db.session.commit()

    return jsonify({'numbers': numbers, 'sum': result})

if __name__ == '__main__':
    app.run(debug=True)
