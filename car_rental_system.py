import json
import os
from tkinter import *
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from PIL import Image, ImageTk
from tkinter import scrolledtext


class CarRentalSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Car Rental System")
        self.root.geometry("1024x720")

        self.image_dir = "car_images"
        self.receipts_dir = "payment_receipts"
        os.makedirs(self.image_dir, exist_ok=True)
        os.makedirs(self.receipts_dir, exist_ok=True)

        self.users_file = "users.json"
        self.cars_file = "cars.json"
        self.bookings_file = "bookings.json"
        self.payments_file = "payments.json"

        self.users = self.load_json(self.users_file, {
            "admin": {"password": "admin123", "is_admin": True},
            "user": {"password": "user123", "is_admin": False}
        })
        self.cars = self.load_json(self.cars_file, {
            "KBZ456W": {"model": "Mazda Demio", "available": True, "rate": 3500, "image": "demio.jpg"},
            "XYZ123A": {"model": "Toyota Corolla", "available": True, "rate": 4000, "image": "corolla.jpg"},
            "ABC789B": {"model": "Honda Civic", "available": True, "rate": 4500, "image": "civic.jpg"},
            "DEF456C": {"model": "Ford Focus", "available": True, "rate": 3800, "image": "focus.jpg"},
            "GHI123D": {"model": "Chevrolet Malibu", "available": True, "rate": 4200, "image": "malibu.jpg"},
            "JKL456E": {"model": "Hyundai Elantra", "available": True, "rate": 3900, "image": "elantra.jpg"},
            "MNO789F": {"model": "Nissan Sentra", "available": True, "rate": 3700, "image": "sentra.jpg"},
            "PQR123G": {"model": "Mazda 3", "available": True, "rate": 4300, "image": "mazda3.jpg"},
            "STU456H": {"model": "Kia Forte", "available": True, "rate": 3600, "image": "forte.jpg"},
            "VWX789I": {"model": "Subaru Impreza", "available": True, "rate": 4600, "image": "impreza.jpg"},
            "YZA123J": {"model": "BMW 3 Series", "available": True, "rate": 5500, "image": "bmw3.jpg"},
            "BCD456K": {"model": "Mercedes-Benz C-Class", "available": True, "rate": 7000, "image": "cclass.jpg"},
            "EFG789L": {"model": "Audi A4", "available": True, "rate": 6000, "image": "audi_a4.jpg"},
            "HJI123M": {"model": "Volkswagen Golf", "available": True, "rate": 3800, "image": "golf.jpg"},
            "KLM456N": {"model": "Jeep Wrangler", "available": True, "rate": 8000, "image": "wrangler.jpg"},
            "NOP789O": {"model": "Chevrolet Tahoe", "available": True, "rate": 7500, "image": "tahoe.jpg"},
            "QRS123P": {"model": "Ram 1500", "available": True, "rate": 8500, "image": "ram1500.jpg"},
            "TUV456Q": {"model": "Ford Mustang", "available": True, "rate": 5000, "image": "mustang.jpg"},
            "WXY789R": {"model": "Toyota Prius", "available": True, "rate": 4200, "image": "prius.jpg"},
            "ZAB123S": {"model": "Honda Accord", "available": True, "rate": 4700, "image": "accord.jpg"}
        })
        self.bookings = self.load_json(self.bookings_file, {})
        self.payments = self.load_json(self.payments_file, {})

        self.current_user = None
        self.photo_refs = []
        self.main_frame = None

        self.show_login()

    def load_json(self, filename, default_data):
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                return json.load(file)
        else:
            self.save_json(filename, default_data)
            return default_data

    def save_json(self, filename, data):
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)

    def clear_frame(self):
        if self.main_frame:
            self.main_frame.destroy()
        self.photo_refs = []

    def show_login(self):
        self.clear_frame()
        self.main_frame = Frame(self.root)
        self.main_frame.pack(expand=True)

        Label(self.main_frame, text="Car Rental Login", font=("Arial", 20)).pack(pady=20)
        Label(self.main_frame, text="Username").pack()
        self.username_entry = Entry(self.main_frame)
        self.username_entry.pack()
        Label(self.main_frame, text="Password").pack()
        self.password_entry = Entry(self.main_frame, show="*")
        self.password_entry.pack()
        Button(self.main_frame, text="Login", command=self.login).pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username in self.users and self.users[username]["password"] == password:
            self.current_user = username
            messagebox.showinfo("Success", f"Welcome {username}!")
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "Invalid credentials!")

    def logout(self):
        self.current_user = None
        self.show_login()

    def show_dashboard(self):
        self.clear_frame()
        self.main_frame = Frame(self.root)
        self.main_frame.pack(expand=True)

        Label(self.main_frame, text=f"Welcome {self.current_user}", font=("Arial", 18)).pack(pady=10)
        Button(self.main_frame, text="View Available Cars", width=25, command=self.show_available_cars).pack(pady=5)
        Button(self.main_frame, text="Book a Car", width=25, command=self.book_car_page).pack(pady=5)
        Button(self.main_frame, text="Return a Car", width=25, command=self.return_car_page).pack(pady=5)
        Button(self.main_frame, text="Payment Options", width=25, command=self.payment_options).pack(pady=5)
        if self.users[self.current_user]["is_admin"]:
            Button(self.main_frame, text="Manage Cars", width=25, command=self.manage_cars).pack(pady=5)
            Button(self.main_frame, text="Manage Users", width=25, command=self.manage_users).pack(pady=5)
            Button(self.main_frame, text="View Payments", width=25, command=self.view_payments).pack(pady=5)
        Button(self.main_frame, text="Logout", width=25, command=self.logout).pack(pady=5)

    def show_available_cars(self):
        self.clear_frame()
        self.main_frame = Frame(self.root)
        self.main_frame.pack(expand=True, fill=BOTH)

        # Create a canvas and scrollbar
        canvas = Canvas(self.main_frame)
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas)

        # Configure the canvas
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        # Mousewheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Pack the scrollbar and canvas
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Navigation buttons frame at the bottom
        nav_frame = Frame(self.main_frame)
        nav_frame.pack(side="bottom", fill=X, pady=10)

        # Add cars to the scrollable frame
        for plate, car in self.cars.items():
            if car["available"]:
                frame = Frame(scrollable_frame, bd=1, relief=SUNKEN, padx=10, pady=10)
                frame.pack(fill=X, pady=5)

                try:
                    img_path = os.path.join(self.image_dir, car.get("image", "default.jpg"))
                    if os.path.exists(img_path):
                        img = Image.open(img_path).resize((120, 90))
                        photo = ImageTk.PhotoImage(img)
                        self.photo_refs.append(photo)
                        Label(frame, image=photo).pack(side=LEFT)
                except:
                    pass

                info = f"{car['model']} ({plate}) - Ksh {car['rate']}/day"
                Label(frame, text=info, font=("Arial", 12)).pack(side=LEFT, padx=10)

        # Navigation buttons
        Button(nav_frame, text="Back", command=self.show_dashboard).pack(side="left", padx=20)
        Button(nav_frame, text="Top", command=lambda: canvas.yview_moveto(0)).pack(side="left", padx=20)
        Button(nav_frame, text="Bottom", command=lambda: canvas.yview_moveto(1)).pack(side="left", padx=20)

    def book_car_page(self):
        self.clear_frame()
        self.main_frame = Frame(self.root)
        self.main_frame.pack(expand=True)

        Label(self.main_frame, text="Book a Car", font=("Arial", 16)).pack(pady=10)

        available = [plate for plate, car in self.cars.items() if car["available"]]
        if not available:
            Label(self.main_frame, text="No available cars").pack()
            return

        Label(self.main_frame, text="Select Car").pack()
        self.car_combo = ttk.Combobox(self.main_frame, values=available, state="readonly")
        self.car_combo.pack()

        Label(self.main_frame, text="Booking Date (YYYY-MM-DD)").pack()
        self.booking_date_entry = Entry(self.main_frame)
        self.booking_date_entry.pack()

        Label(self.main_frame, text="Number of Days").pack()
        self.days_entry = Entry(self.main_frame)
        self.days_entry.pack()

        Button(self.main_frame, text="Book Now", command=self.book_car).pack(pady=10)
        Button(self.main_frame, text="Back", command=self.show_dashboard).pack()

    def book_car(self):
        plate = self.car_combo.get()
        date_str = self.booking_date_entry.get()
        days_str = self.days_entry.get()

        try:
            booking_date = datetime.strptime(date_str, "%Y-%m-%d")
            days = int(days_str)
            if days <= 0:
                raise ValueError("Days must be positive")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")
            return

        if plate in self.cars and self.cars[plate]["available"]:
            total_cost = self.cars[plate]["rate"] * days
            
            # Store booking information
            self.cars[plate]["available"] = False
            self.bookings[plate] = {
                "user": self.current_user,
                "date": date_str,
                "days": days,
                "total_cost": total_cost,
                "paid": False
            }
            
            self.save_json(self.cars_file, self.cars)
            self.save_json(self.bookings_file, self.bookings)
            
            messagebox.showinfo("Success", f"Booked {plate} on {date_str} for {days} days\nTotal cost: Ksh {total_cost}")
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "Car not available")

    def return_car_page(self):
        self.clear_frame()
        self.main_frame = Frame(self.root)
        self.main_frame.pack(expand=True)

        user_booked = [plate for plate, b in self.bookings.items() if b["user"] == self.current_user]

        Label(self.main_frame, text="Return a Car", font=("Arial", 16)).pack(pady=10)

        if not user_booked:
            Label(self.main_frame, text="You haven't booked any cars.").pack()
        else:
            self.return_combo = ttk.Combobox(self.main_frame, values=user_booked, state="readonly")
            self.return_combo.pack(pady=5)
            Button(self.main_frame, text="Return Car", command=self.return_car).pack(pady=5)

        Button(self.main_frame, text="Back", command=self.show_dashboard).pack(pady=10)

    def return_car(self):
        plate = self.return_combo.get()
        if plate in self.bookings and self.bookings[plate]["user"] == self.current_user:
            if not self.bookings[plate]["paid"]:
                messagebox.showwarning("Warning", "Payment not completed. Please make payment before returning.")
                self.payment_options(plate)
                return
                
            self.cars[plate]["available"] = True
            del self.bookings[plate]
            self.save_json(self.cars_file, self.cars)
            self.save_json(self.bookings_file, self.bookings)
            messagebox.showinfo("Success", "Car returned successfully!")
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "Unauthorized return")

    def payment_options(self, plate=None):
        self.clear_frame()
        self.main_frame = Frame(self.root)
        self.main_frame.pack(expand=True)

        Label(self.main_frame, text="Payment Options", font=("Arial", 16)).pack(pady=10)

        if plate is None:
            # Show bookings that need payment
            unpaid_bookings = [p for p, b in self.bookings.items() 
                             if b["user"] == self.current_user and not b["paid"]]
            
            if not unpaid_bookings:
                Label(self.main_frame, text="No pending payments").pack()
                Button(self.main_frame, text="Back", command=self.show_dashboard).pack(pady=10)
                return
                
            Label(self.main_frame, text="Select Booking to Pay").pack()
            self.payment_combo = ttk.Combobox(self.main_frame, values=unpaid_bookings, state="readonly")
            self.payment_combo.pack(pady=5)
            
            Button(self.main_frame, text="Select", command=lambda: self.show_payment_methods(self.payment_combo.get())).pack(pady=5)
        else:
            # Directly show payment methods for specific booking
            self.show_payment_methods(plate)
            
        Button(self.main_frame, text="Back", command=self.show_dashboard).pack(pady=10)

    def show_payment_methods(self, plate):
        if plate not in self.bookings or self.bookings[plate]["user"] != self.current_user:
            messagebox.showerror("Error", "Invalid booking")
            return
            
        booking = self.bookings[plate]
        total_cost = booking["total_cost"]
        
        self.clear_frame()
        self.main_frame = Frame(self.root)
        self.main_frame.pack(expand=True)

        Label(self.main_frame, text=f"Payment for {plate}", font=("Arial", 16)).pack(pady=10)
        Label(self.main_frame, text=f"Total Amount: Ksh {total_cost}", font=("Arial", 14)).pack(pady=5)
        
        # Payment method selection
        Label(self.main_frame, text="Select Payment Method:").pack(pady=5)
        
        self.payment_method = StringVar(value="M-Pesa")
        Radiobutton(self.main_frame, text="M-Pesa", variable=self.payment_method, value="M-Pesa").pack()
        Radiobutton(self.main_frame, text="Credit Card", variable=self.payment_method, value="Credit Card").pack()
        Radiobutton(self.main_frame, text="PayPal", variable=self.payment_method, value="PayPal").pack()
        Radiobutton(self.main_frame, text="Bank Transfer", variable=self.payment_method, value="Bank Transfer").pack()
        
        # Payment details frame
        self.details_frame = Frame(self.main_frame)
        self.details_frame.pack(pady=10)
        
        # Update details based on payment method
        self.payment_method.trace('w', self.update_payment_details)
        self.update_payment_details()
        
        Button(self.main_frame, text="Make Payment", command=lambda: self.process_payment(plate)).pack(pady=10)
        Button(self.main_frame, text="Back", command=self.show_dashboard).pack()

    def update_payment_details(self, *args):
        # Clear previous details
        for widget in self.details_frame.winfo_children():
            widget.destroy()
            
        method = self.payment_method.get()
        
        if method == "M-Pesa":
            Label(self.details_frame, text="M-Pesa Number:").pack()
            self.payment_details = Entry(self.details_frame)
            self.payment_details.pack()
        elif method == "Credit Card":
            Label(self.details_frame, text="Card Number:").pack()
            Entry(self.details_frame).pack()
            Label(self.details_frame, text="Expiry Date:").pack()
            Entry(self.details_frame).pack()
            Label(self.details_frame, text="CVV:").pack()
            Entry(self.details_frame).pack()
        elif method == "PayPal":
            Label(self.details_frame, text="PayPal Email:").pack()
            self.payment_details = Entry(self.details_frame)
            self.payment_details.pack()
        elif method == "Bank Transfer":
            Label(self.details_frame, text="Bank Name:").pack()
            Entry(self.details_frame).pack()
            Label(self.details_frame, text="Account Number:").pack()
            Entry(self.details_frame).pack()

    def process_payment(self, plate):
        method = self.payment_method.get()
        details = self.payment_details.get() if hasattr(self, 'payment_details') else ""
        
        if method in ["M-Pesa", "PayPal"] and not details:
            messagebox.showerror("Error", f"Please enter your {method} details")
            return
            
        payment_id = f"PAY-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        booking = self.bookings[plate]
        payment_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Create payment record
        self.payments[payment_id] = {
            "booking_plate": plate,
            "user": self.current_user,
            "amount": booking["total_cost"],
            "method": method,
            "date": payment_date,
            "status": "Completed",
            "details": details
        }
        
        # Mark booking as paid
        self.bookings[plate]["paid"] = True
        
        self.save_json(self.payments_file, self.payments)
        self.save_json(self.bookings_file, self.bookings)
        
        # Generate and show receipt
        receipt_content = self.generate_receipt(payment_id, plate, booking, method, details, payment_date)
        self.show_receipt(receipt_content, payment_id)
        
        messagebox.showinfo("Success", f"Payment of Ksh {booking['total_cost']} completed successfully!")
        self.show_dashboard()

    def generate_receipt(self, payment_id, plate, booking, method, details, payment_date):
        """Generate a text receipt for the payment"""
        car = self.cars[plate]
        receipt = f"""
        {'='*40}
        CAR RENTAL PAYMENT RECEIPT
        {'='*40}
        Receipt ID: {payment_id}
        Date: {payment_date}
        {'-'*40}
        Customer: {self.current_user}
        Car Model: {car['model']}
        Plate Number: {plate}
        Booking Date: {booking['date']}
        Rental Days: {booking['days']}
        {'-'*40}
        Payment Method: {method}
        Payment Details: {details}
        {'-'*40}
        Subtotal: Ksh {car['rate']}/day x {booking['days']} days
        Total Amount: Ksh {booking['total_cost']}
        {'='*40}
        Thank you for your business!
        """
        return receipt

    def show_receipt(self, receipt_content, payment_id):
        """Display the receipt in a new window with save option"""
        receipt_window = Toplevel(self.root)
        receipt_window.title("Payment Receipt")
        receipt_window.geometry("500x600")
        
        # Create scrolled text widget
        receipt_text = scrolledtext.ScrolledText(receipt_window, wrap=WORD, width=60, height=30)
        receipt_text.pack(padx=10, pady=10)
        receipt_text.insert(INSERT, receipt_content)
        receipt_text.config(state=DISABLED)  # Make it read-only
        
        # Save button
        def save_receipt():
            filename = f"receipt_{payment_id}.txt"
            filepath = os.path.join(self.receipts_dir, filename)
            try:
                with open(filepath, 'w') as f:
                    f.write(receipt_content)
                messagebox.showinfo("Success", f"Receipt saved as {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save receipt: {e}")
        
        Button(receipt_window, text="Save Receipt", command=save_receipt).pack(pady=10)
        Button(receipt_window, text="Close", command=receipt_window.destroy).pack(pady=5)

    def view_payments(self):
        self.clear_frame()
        self.main_frame = Frame(self.root)
        self.main_frame.pack(expand=True)

        Label(self.main_frame, text="Payment Records", font=("Arial", 16)).pack(pady=10)
        
        if not self.payments:
            Label(self.main_frame, text="No payment records found").pack()
        else:
            # Create a treeview to display payments
            tree = ttk.Treeview(self.main_frame, columns=("ID", "User", "Plate", "Amount", "Method", "Date"), show="headings")
            tree.heading("ID", text="Payment ID")
            tree.heading("User", text="User")
            tree.heading("Plate", text="Car Plate")
            tree.heading("Amount", text="Amount")
            tree.heading("Method", text="Method")
            tree.heading("Date", text="Date")
            
            for pid, payment in self.payments.items():
                tree.insert("", "end", values=(
                    pid,
                    payment["user"],
                    payment["booking_plate"],
                    f"Ksh {payment['amount']}",
                    payment["method"],
                    payment["date"]
                ))
            
            tree.pack(expand=True, fill=BOTH, padx=10, pady=10)

        Button(self.main_frame, text="Back", command=self.show_dashboard).pack(pady=10)

    def manage_cars(self):
        self.clear_frame()
        self.main_frame = Frame(self.root)
        self.main_frame.pack(expand=True)

        Label(self.main_frame, text="Manage Cars", font=("Arial", 16)).pack(pady=10)

        for plate, car in self.cars.items():
            status = "Available" if car["available"] else "Booked"
            Label(self.main_frame, text=f"{plate} - {car['model']} ({status}) - Ksh {car['rate']}").pack()

        Button(self.main_frame, text="Back", command=self.show_dashboard).pack(pady=10)

    def manage_users(self):
        self.clear_frame()
        self.main_frame = Frame(self.root)
        self.main_frame.pack(expand=True)

        Label(self.main_frame, text="Manage Users", font=("Arial", 16)).pack(pady=10)

        for user, info in self.users.items():
            role = "Admin" if info["is_admin"] else "User"
            Label(self.main_frame, text=f"{user} - {role}").pack()

        Button(self.main_frame, text="Back", command=self.show_dashboard).pack(pady=10)


if __name__ == "__main__":
    root = Tk()
    app = CarRentalSystem(root)
    root.mainloop()