# Car Rental System - Web Application

A comprehensive web application for managing a car rental business, converted from a Tkinter desktop app to a Flask-based web app. It allows users to book, return, and pay for cars, while admins can manage cars, users, and view payments.

## 🚀 Features

* User authentication and admin access control
* View available cars with pricing
* Book a car for a specific duration
* Return a booked car
* Payment processing (M-Pesa, PayPal, Credit Card, Bank Transfer)
* Admin management of cars and users
* View all payments (admin only)

## 🛠️ Installation and Setup

1. **Clone the repository:**

```bash
git clone https://github.com/Warrenchris/python-car-rental-system.git
cd car-rental-system
```

2. **Install dependencies:**

```bash
pip install flask
```

(Optional: Install Pillow for image handling)

```bash
pip install pillow
```

3. **Setup the project structure:**
   Ensure the following structure:

```
car-rental-webapp/
│
├── app.py
├── users.json
├── cars.json
├── bookings.json
├── payments.json
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── available_cars.html
│   ├── book_car.html
│   ├── return_car.html
│   ├── payment_options.html
│   ├── manage_cars.html
│   ├── manage_users.html
│   └── view_payments.html
│
├── static/
│   ├── car_images/
│   └── styles.css (optional)
```

4. **Run the Application:**

```bash
python app.py
```

Visit [http://127.0.0.1:5000](http://127.0.0.1:5000) to access the application.

## 📦 Default Admin/User Accounts

* Admin:

  * Username: `admin`
  * Password: `admin123`
* User:

  * Username: `user`
  * Password: `user123`

## 🗂️ Directory Structure

```
car-rental-webapp/
│
├── app.py             # Main Flask application
├── users.json         # User data (admin/user accounts)
├── cars.json          # Car data
├── bookings.json      # Booking records
├── payments.json      # Payment records
│
├── templates/         # HTML templates
├── static/            # Static files (images, CSS)
│
└── README.md          # Project documentation
```

## 📌 Future Improvements

* User registration and profile management
* Payment gateway integration (Stripe, PayPal API)
* Enhanced admin dashboard with graphs
* Export payment reports as CSV/PDF
* Car image upload functionality

## 📝 License

This project is open-source and available under the MIT License.

Feel free to fork, modify, and contribute!
