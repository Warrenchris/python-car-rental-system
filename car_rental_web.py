from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# File paths
data_dir = '.'
users_file = os.path.join(data_dir, 'users.json')
cars_file = os.path.join(data_dir, 'cars.json')
bookings_file = os.path.join(data_dir, 'bookings.json')
payments_file = os.path.join(data_dir, 'payments.json')

# Load and save functions
def load_json(filename, default_data):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    else:
        with open(filename, 'w') as file:
            json.dump(default_data, file, indent=4)
        return default_data

def save_json(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

# Load data
users = load_json(users_file, {
    "admin": {"password": "admin123", "is_admin": True},
    "user": {"password": "user123", "is_admin": False}
})
cars = load_json(cars_file, {})
bookings = load_json(bookings_file, {})
payments = load_json(payments_file, {})

# Routes
@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'], is_admin=users[session['username']]['is_admin'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            session['username'] = username
            flash(f"Welcome {username}!", 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials!', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

@app.route('/available_cars')
def available_cars():
    available = {plate: car for plate, car in cars.items() if car['available']}
    return render_template('available_cars.html', cars=available)

@app.route('/book', methods=['GET', 'POST'])
def book_car():
    available = {plate: car for plate, car in cars.items() if car['available']}
    if request.method == 'POST':
        plate = request.form['plate']
        booking_date = request.form['booking_date']
        days = int(request.form['days'])
        if plate in cars and cars[plate]['available']:
            total_cost = cars[plate]['rate'] * days
            bookings[plate] = {
                'user': session['username'],
                'date': booking_date,
                'days': days,
                'total_cost': total_cost,
                'paid': False
            }
            cars[plate]['available'] = False
            save_json(bookings_file, bookings)
            save_json(cars_file, cars)
            flash(f"Booked {plate} successfully!", 'success')
            return redirect(url_for('home'))
    return render_template('book_car.html', cars=available)

@app.route('/return', methods=['GET', 'POST'])
def return_car():
    user_booked = [plate for plate, b in bookings.items() if b['user'] == session['username']]
    if request.method == 'POST':
        plate = request.form['plate']
        if plate in bookings and bookings[plate]['user'] == session['username']:
            if not bookings[plate]['paid']:
                flash('Please complete payment before returning.', 'warning')
                return redirect(url_for('payment_options', plate=plate))
            cars[plate]['available'] = True
            bookings.pop(plate)
            save_json(cars_file, cars)
            save_json(bookings_file, bookings)
            flash('Car returned successfully!', 'success')
            return redirect(url_for('home'))
    return render_template('return_car.html', user_booked=user_booked)

@app.route('/payment_options', methods=['GET', 'POST'])
def payment_options():
    plate = request.args.get('plate')
    unpaid_bookings = [p for p, b in bookings.items() if b['user'] == session['username'] and not b['paid']]
    if plate and plate in bookings:
        unpaid_bookings = [plate]
    if request.method == 'POST':
        plate = request.form['plate']
        method = request.form['method']
        details = request.form.get('details', '')
        payment_id = f"PAY-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        payment_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        booking = bookings[plate]
        payments[payment_id] = {
            'booking_plate': plate,
            'user': session['username'],
            'amount': booking['total_cost'],
            'method': method,
            'date': payment_date,
            'status': 'Completed',
            'details': details
        }
        bookings[plate]['paid'] = True
        save_json(payments_file, payments)
        save_json(bookings_file, bookings)
        flash('Payment completed successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('payment_options.html', unpaid_bookings=unpaid_bookings)

@app.route('/manage_cars')
def manage_cars():
    if not users[session['username']]['is_admin']:
        return redirect(url_for('home'))
    return render_template('manage_cars.html', cars=cars)

@app.route('/manage_users')
def manage_users():
    if not users[session['username']]['is_admin']:
        return redirect(url_for('home'))
    return render_template('manage_users.html', users=users)

@app.route('/view_payments')
def view_payments():
    if not users[session['username']]['is_admin']:
        return redirect(url_for('home'))
    return render_template('view_payments.html', payments=payments)

if __name__ == '__main__':
    app.run(debug=True)
