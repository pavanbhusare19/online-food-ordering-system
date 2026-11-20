
from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "foodiehub_secret_key"

DATABASE = "database.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn



def initialize_database():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS foods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            image TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL,
            total REAL NOT NULL,
            items TEXT NOT NULL,
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    foods = [
        ("Margherita Pizza", "Pizza", "Classic cheese pizza", 199,
         "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=600"),
        ("Veg Burger", "Burger", "Fresh vegetable burger", 99,
         "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=600"),
        ("Paneer Pizza", "Pizza", "Delicious paneer pizza", 249,
         "https://images.unsplash.com/photo-1571407970349-bc81e7e96d47?w=600"),
        ("French Fries", "Snacks", "Crispy golden fries", 89,
         "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=600"),
        ("Veg Biryani", "Indian", "Authentic Indian biryani", 159,
         "https://images.unsplash.com/photo-1563379091339-03246963d96c?w=600"),
        ("Masala Dosa", "Indian", "South Indian crispy dosa", 79,
         "https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=600"),
        ("Cold Coffee", "Drinks", "Chilled creamy coffee", 89,
         "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=600"),
        ("Chocolate Cake", "Dessert", "Rich chocolate cake", 129,
         "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=600"),
        ("Italian Pasta", "Pasta", "Creamy Italian pasta", 179,
         "https://images.unsplash.com/photo-1473093295043-cdd812d0e601?w=600"),
        ("Fresh Salad", "Healthy", "Fresh vegetable salad", 119,
         "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=600"),
        ("Cheese Sandwich", "Snacks", "Grilled cheese sandwich", 109,
         "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?w=600"),
        ("Chocolate Ice Cream", "Dessert", "Creamy chocolate ice cream", 79,
         "https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=600"),
        ("Veg Samosa", "Snacks", "Crispy potato samosa", 30,
         "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=600"),
        ("Hakka Noodles", "Chinese", "Delicious vegetable noodles", 149,
         "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=600"),
        ("Veg Tacos", "Mexican", "Fresh Mexican tacos", 169,
         "https://images.unsplash.com/photo-1551504734-5ee1c4a1479b?w=600"),
        ("Paneer Wrap", "Snacks", "Spicy paneer wrap", 139,
         "https://images.unsplash.com/photo-1626700051175-6818013e1d4f?w=600"),
        ("Cheese Pizza", "Pizza", "Loaded cheese pizza", 279,
         "https://images.unsplash.com/photo-1571407970349-bc81e7e96d47?w=600"),
        ("Veg Momos", "Chinese", "Steamed vegetable momos", 99,
         "https://images.unsplash.com/photo-1563245372-f21724e3856d?w=600"),
        ("Pancakes", "Dessert", "Soft fluffy pancakes", 149,
         "https://images.unsplash.com/photo-1528207776546-365bb710ee93?w=600"),
        ("Fresh Orange Juice", "Drinks", "Freshly squeezed orange juice", 69,
         "https://images.unsplash.com/photo-1600271886742-f049cd451bba?w=600")
    ]

    for food in foods:
        existing = cursor.execute(
            "SELECT id FROM foods WHERE name = ?", (food[0],)
        ).fetchone()

        if existing:
            cursor.execute("""
                UPDATE foods
                SET category=?, description=?, price=?, image=?
                WHERE name=?
            """, (food[1], food[2], food[3], food[4], food[0]))
        else:
            cursor.execute("""
                INSERT INTO foods (name, category, description, price, image)
                VALUES (?, ?, ?, ?, ?)
            """, food)

    conn.commit()
    conn.close()
    print("Food database initialized successfully!")
    print("20 food items with image URLs are ready!")

@app.route("/")
def index():
    conn = get_db()
    foods = conn.execute("SELECT * FROM foods LIMIT 6").fetchall()
    conn.close()
    return render_template("index.html", foods=foods)


@app.route("/menu")
def menu():
    search = request.args.get("search", "").strip()
    category = request.args.get("category", "").strip()

    conn = get_db()
    query = "SELECT * FROM foods WHERE 1=1"
    params = []

    if search:
        query += " AND (name LIKE ? OR description LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])

    if category:
        query += " AND category = ?"
        params.append(category)

    foods = conn.execute(query, params).fetchall()
    conn.close()

    return render_template("menu.html", foods=foods)


@app.route("/add-to-cart/<int:food_id>")
def add_to_cart(food_id):
    conn = get_db()
    food = conn.execute(
        "SELECT id FROM foods WHERE id = ?", (food_id,)
    ).fetchone()
    conn.close()

    if not food:
        flash("Food item not found!")
        return redirect(url_for("menu"))

    cart = session.get("cart", {})
    key = str(food_id)
    cart[key] = int(cart.get(key, 0)) + 1
    session["cart"] = cart

    flash("Food added to cart successfully!")
    return redirect(url_for("menu"))


@app.route("/cart")
def cart():
    cart_data = session.get("cart", {})
    items = []
    total = 0

    conn = get_db()

    for food_id, quantity in cart_data.items():
        food = conn.execute(
            "SELECT * FROM foods WHERE id = ?", (food_id,)
        ).fetchone()

        if food:
            quantity = int(quantity)
            subtotal = food["price"] * quantity
            total += subtotal

            items.append({
                "food": food,
                "quantity": quantity,
                "subtotal": subtotal
            })

    conn.close()

    return render_template(
        "cart.html", items=items, total=total
    )


@app.route("/update-cart/<int:food_id>", methods=["POST"])
def update_cart(food_id):
    quantity = request.form.get("quantity", "1")

    try:
        quantity = int(quantity)
    except ValueError:
        flash("Invalid quantity!")
        return redirect(url_for("cart"))

    cart_data = session.get("cart", {})
    key = str(food_id)

    if quantity <= 0:
        cart_data.pop(key, None)
    elif quantity <= 20 and key in cart_data:
        cart_data[key] = quantity
    else:
        flash("Quantity must be between 1 and 20.")

    session["cart"] = cart_data
    return redirect(url_for("cart"))


@app.route("/remove-from-cart/<int:food_id>")
def remove_from_cart(food_id):
    cart_data = session.get("cart", {})
    cart_data.pop(str(food_id), None)
    session["cart"] = cart_data

    flash("Food removed from cart.")
    return redirect(url_for("cart"))


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    cart_data = session.get("cart", {})

    if not cart_data:
        flash("Your cart is empty!")
        return redirect(url_for("menu"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        phone = request.form.get("phone", "").strip()
        address = request.form.get("address", "").strip()

        if not name or not address or not phone.isdigit() or len(phone) != 10:
            flash("Please enter valid delivery details.")
            return redirect(url_for("checkout"))

        conn = get_db()
        order_items = []
        total = 0

        for food_id, quantity in cart_data.items():
            food = conn.execute(
                "SELECT * FROM foods WHERE id = ?", (food_id,)
            ).fetchone()

            if food:
                quantity = int(quantity)
                total += food["price"] * quantity
                order_items.append(
                    f"{food['name']} x {quantity}"
                )

        if not order_items:
            conn.close()
            session["cart"] = {}
            flash("Your cart is empty!")
            return redirect(url_for("menu"))

        conn.execute("""
            INSERT INTO orders
            (customer_name, phone, address, total, items)
            VALUES (?, ?, ?, ?, ?)
        """, (
            name, phone, address, total,
            ", ".join(order_items)
        ))

        conn.commit()
        conn.close()

        session["cart"] = {}
        flash("Order placed successfully!")
        return redirect(url_for("orders"))

    return render_template("checkout.html")


@app.route("/orders")
def orders():
    conn = get_db()
    orders = conn.execute(
        "SELECT * FROM orders ORDER BY id DESC"
    ).fetchall()
    conn.close()

    return render_template("orders.html", orders=orders)


@app.route("/admin")
def admin():
    conn = get_db()

    foods = conn.execute(
        "SELECT * FROM foods ORDER BY id"
    ).fetchall()

    orders = conn.execute(
        "SELECT * FROM orders ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return render_template(
        "admin.html", foods=foods, orders=orders
    )
initialize_database()

if __name__ == "__main__":
    print("FoodieHub Online Food Ordering System starting...")
    app.run(debug=True)