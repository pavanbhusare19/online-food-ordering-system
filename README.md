FoodieHub



FoodieHub is an online food ordering app I built with Flask and SQLite. You can browse the menu, add dishes to a cart, check out with your details, and look back at your past orders. There's also a simple admin dashboard for keeping an eye on the menu and incoming orders.



I made it as a full stack development project, mainly to get hands-on with connecting a Flask backend to a database and handling a real ordering flow from start to finish.



What it does

A home page that highlights featured dishes

A menu with 20 food items, each with an image and a price

Categories and a search bar to find what you're after

A cart where you can change quantities or remove items

Checkout where you enter your customer details

Order placement and an order history page

An admin dashboard for managing the menu and viewing customer orders

Built with



Python, Flask, SQLite, HTML5, CSS3, JavaScript, and Jinja2 for templating.



Project layout

online-food-ordering-system/

│

├── app.py

├── requirements.txt

├── database.db

│

├── templates/

│   ├── index.html

│   ├── menu.html

│   ├── cart.html

│   ├── checkout.html

│   ├── orders.html

│   └── admin.html

│

└── static/

&#x20;   ├── css/

&#x20;   │   └── style.css

&#x20;   ├── js/

&#x20;   └── images/

Running it locally

Clone the repo:

git clone https://github.com/pavanbhusare19/online-food-ordering-system.git

Go into the project folder:

cd online-food-ordering-system

Install the dependencies:

pip install -r requirements.txt

Start the app:

python app.py

Open your browser and head to:

http://127.0.0.1:5000

Admin dashboard



The dashboard gives you a quick overview of the store: how many food items are on the menu, how many orders customers have placed, and the total value of those orders. Below that, you'll find the full menu and a list of every customer order.



Why I built it



I wanted a straightforward ordering platform that shows how the pieces of a full stack app fit together: the front end, the backend, the database, and the order management behind it.



Author



Pavan Bhusare GitHub: pavanbhusare19

