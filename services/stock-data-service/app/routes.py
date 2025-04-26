from flask import Blueprint, jsonify, request
from app.database import get_db_connection

routes = Blueprint('routes', __name__)

@routes.route('/stocks', methods=['GET'])
def get_stocks():
    """
    Fetches all stocks from the database.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT * FROM stocks")
        stocks = cursor.fetchall()
        return jsonify(stocks), 200
    finally:
        cursor.close()
        conn.close()

@routes.route('/stocks', methods=['POST'])
def add_stock():
    """
    Adds a new stock entry to the database.
    """
    data = request.json
    symbol = data.get('symbol')
    name = data.get('name')
    price = data.get('price', 0.0)

    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("INSERT INTO stocks (symbol, name, price) VALUES (%s, %s, %s)", (symbol, name, price))
        conn.commit()
        return jsonify({"message": "Stock added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()
