import sqlite3
from flask import Flask, render_template, request, jsonify, send_file
import qrcode
from io import BytesIO
from datetime import datetime
import os

app = Flask(__name__)

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS customers
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, phone TEXT, email TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS bills
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, customer_id INTEGER, items TEXT, payment_method TEXT, amount REAL, date TEXT)''')
    conn.commit()
    conn.close()

init_db()

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Generate bill
@app.route('/generate_bill', methods=['POST'])
def generate_bill():
    name = request.form['name']
    phone = request.form['phone']
    email = request.form['email']
    items = request.form.getlist('items[]')
    quantities = request.form.getlist('quantities[]')
    payment_method = request.form['payment_method']
    
    # Calculate total amount
    menu = {'Paneer Tikka': 250, 'Butter Chicken': 350, 'Dal Makhani': 200, 'Naan': 50, 'Biryani': 300}
    total = sum(menu[item] * int(qty) for item, qty in zip(items, quantities))
    
    # Save customer
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO customers (name, phone, email) VALUES (?, ?, ?)", (name, phone, email))
    customer_id = c.lastrowid
    
    # Save bill
    items_str = ', '.join([f"{item} (Qty: {qty})" for item, qty in zip(items, quantities)])
    c.execute("INSERT INTO bills (customer_id, items, payment_method, amount, date) VALUES (?, ?, ?, ?, ?)",
              (customer_id, items_str, payment_method, total, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    conn.close()
    
    return render_template('bill.html', name=name, phone=phone, email=email, items=zip(items, quantities, [menu[item] for item in items]), total=total, payment_method=payment_method)

# Generate UPI QR code
@app.route('/generate_qr')
def generate_qr():
    upi_id = "shrinathshrimnag30@oksbi"
    amount = request.args.get('amount', 100)
    upi_url = f"upi://pay?pa={upi_id}&pn=Shrinath%20Restaurant&am={amount}&cu=INR"
    
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(upi_url)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

# View customers
@app.route('/customers')
def customers():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM customers")
    customers = c.fetchall()
    conn.close()
    return render_template('customers.html', customers=customers)

if __name__ == '__main__':
    app.run(debug=True)