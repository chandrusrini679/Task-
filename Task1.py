
from flask import Flask,render_template,request

pip install mysql-connector-python

import mysql.connector


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='USER_NAME'


# Connect to the MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="your_username",
    password="your_password",
    database="your_database"
)

cursor = conn.cursor()

# Create Product table
cursor.execute('''CREATE TABLE IF NOT EXISTS Product (
    product_id VARCHAR(255) PRIMARY KEY
)''')

# Create Location table
cursor.execute('''CREATE TABLE IF NOT EXISTS Location (
    location_id VARCHAR(255) PRIMARY KEY
)''')

# Create ProductMovement table
cursor.execute('''CREATE TABLE IF NOT EXISTS ProductMovement (
    movement_id VARCHAR(255) PRIMARY KEY,
    timestamp DATETIME,
    from_location VARCHAR(255),
    to_location VARCHAR(255),
    product_id VARCHAR(255),
    qty INT,
    FOREIGN KEY (product_id) REFERENCES Product (product_id),
    FOREIGN KEY (from_location) REFERENCES Location (location_id),
    FOREIGN KEY (to_location) REFERENCES Location (location_id)
)''')

import mysql.connector

def add_product(product_id):
    # Connect to the MySQL database
    conn1 = mysql.connector.connect(
        host="localhost",
        user="your_username",
        password="your_password",
        database="your_database"
    )

    cursor1 = conn.cursor()

    cursor1.execute("INSERT INTO Product (product_id) VALUES (%s)", (product_id,))

    conn1.commit()
    conn1.close()

@app.route('/edit', method=['GET', 'POST'])
def edit_product(old_product_id, new_product_id):
    if request.method == 'POST':
        return render_template('index.html')


@app.route('/view', method=['GET', 'POST'])
def view_products():
    if request.method == 'POST':
        return render_template('movement.html')

# Define similar functions for Location and ProductMovement


@app.route('/add', method=['GET', 'POST'])
def add_location(location_id):
    if request.method == 'POST':
        return render_template('index.html')

@app.route('/edit', method=['GET', 'POST'])
def edit_location(old_location_id, new_location_id):
    if request.method == 'POST':
        return render_template('movement.html')


@app.route('/view', method=['GET', 'POST'])
def view_locations():
    if request.method == 'POST':
        return render_template('report.html')


@app.route('/add', method=['GET', 'POST'])
def add_product_movement(movement_id, timestamp, from_location, to_location, product_id, qty):
    if request.method == 'POST':
        return render_template('prod.html')


@app.route('/edit', method=['GET', 'POST'])
def edit_product_movement(movement_id, new_timestamp, new_from_location, new_to_location, new_qty):
    if request.method == 'POST':
        return render_template('movement.html')

@app.route('/view', method=['GET', 'POST'])
def view_product_movements(product_balance=None):
    if request.method == 'POST':
        return render_template('report.html')

    # Create 3/4 Products

    add_product("Product A")
    add_product("Product B")
    add_product("Product C")

    # Create 3/4 Locations

    add_location("Location X")
    add_location("Location Y")
    add_location("Location Z")

    # Make ProductMovements
    add_product_movement("1", "2023-05-29 10:00:00", "", "Location X", "Product A", 10)
    add_product_movement("2", "2023-05-29 11:00:00", "", "Location X", "Product B", 5)
    add_product_movement("3", "2023-05-29 12:00:00", "Location X", "Location Y", "Product A", 3)



    def get_product_balance():
        if request.method == 'POST':
            return render_template('report.html')

    get_product_balance()
    for row in product_balance:
        print(f"Product: {row[0]}, Warehouse: {row[1]}, Qty: {row[2]}")


@app.route('/add')

def add_product():
   return  "<p><Products</p>"
if __name__ == '__main__':
app.run(debug=True)