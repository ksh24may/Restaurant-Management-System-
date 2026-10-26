from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import mysql.connector

app = Flask(__name__, template_folder="templates")  # Ensure templates folder is set
CORS(app)

# ✅ Connect to MySQL Database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="jdbc2025",  # Make sure this is your correct DB password
    database="restaurant_db"
)
cursor = db.cursor(dictionary=True)

# ✅ Home Page Route (Render HTML)
@app.route('/')
def home():
    return render_template('index.html')

# ✅ User Authentication (Login)
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (data['username'], data['password']))
    user = cursor.fetchone()
    return jsonify({"success": bool(user), "user": user})

# ✅ Fetch Menu Items
@app.route('/menu', methods=['GET'])
def get_menu():
    return render_template('menu.html')

# ✅ Place Order
@app.route('/order', methods=['GET', 'POST'])
def place_order():
    if request.method == 'GET':
        return render_template('order.html')
    data = request.json
    cursor.execute("INSERT INTO orders (user_id, menu_item, quantity, total_price) VALUES (%s, %s, %s, %s)",
                   (data['user_id'], data['menu_item'], data['quantity'], data['total_price']))
    db.commit()
    return jsonify({"success": True, "message": "Order Placed!"})

# ✅ Get Orders for User
@app.route('/orders/<int:user_id>', methods=['GET'])
def get_orders(user_id):
    cursor.execute("SELECT * FROM orders WHERE user_id = %s", (user_id,))
    orders = cursor.fetchall()
    return jsonify(orders)

# ✅ Payment Processing
@app.route('/payment', methods=['GET', 'POST'])
def make_payment():
    if request.method == 'GET':
        return render_template('payment.html')
    data = request.json
    cursor.execute("INSERT INTO payments (user_id, order_id, amount, payment_method, transaction_status) VALUES (%s, %s, %s, %s, 'Completed')",
                   (data['user_id'], data['order_id'], data['amount'], data['payment_method']))
    db.commit()
    return jsonify({"success": True, "message": "Payment Successful!"})

# ✅ Table Reservation
@app.route('/reserve', methods=['POST'])
def reserve_table():
    data = request.json
    cursor.execute("INSERT INTO reservations (user_id, table_number, status) VALUES (%s, %s, 'Reserved')",
                   (data['user_id'], data['table_number']))
    db.commit()
    return jsonify({"success": True, "message": "Table Reserved!"})

# ✅ Live Order Tracking
@app.route('/track-order/<int:order_id>', methods=['GET'])
def track_order(order_id):
    cursor.execute("SELECT * FROM orders WHERE id = %s", (order_id,))
    order = cursor.fetchone()
    return jsonify(order)

# ✅ Delivery Tracking
@app.route('/delivery-status/<int:order_id>', methods=['GET'])
def delivery_status(order_id):
    cursor.execute("SELECT * FROM delivery WHERE order_id = %s", (order_id,))
    delivery = cursor.fetchone()
    return jsonify(delivery)

# ✅ Waiter Tip Tracking
@app.route('/add-tip', methods=['POST'])
def add_tip():
    data = request.json
    cursor.execute("UPDATE waiters SET total_tips = total_tips + %s WHERE id = %s", (data['tip'], data['waiter_id']))
    db.commit()
    return jsonify({"success": True, "message": "Tip Added!"})

# ✅ Admin Panel Route
@app.route('/admin')
def admin():
    return render_template('admin.html')

# ✅ Waiter Page
@app.route('/waiter')
def waiter():
    return render_template('waiter.html')

# ✅ Reservation Page
@app.route('/reservation')
def reservation():
    return render_template('reservation.html')

# ✅ Delivery Page
@app.route('/delivery')
def delivery():
    return render_template('delivery.html')

# ✅ Run the Flask App
if __name__ == '__main__':
    app.run(debug=True)
