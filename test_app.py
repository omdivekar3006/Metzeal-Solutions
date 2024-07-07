import json
import uuid  # Import uuid module

from app import app, db, Transaction

# Create an application context
with app.app_context():
    # Create a test transaction
    numbers = [1, 2, 3, 4]
    result = sum(numbers)
    hash_key = uuid.uuid4().hex  # Generate a unique hash key
    transaction = Transaction(numbers=json.dumps(numbers), result=result, hash_key=hash_key)

    # Add and commit the transaction to the database
    db.session.add(transaction)
    db.session.commit()

    # Query the database
    transactions = Transaction.query.all()
    for t in transactions:
        print(f'Transaction {t.id}: Numbers={t.numbers}, Sum={t.result}')
