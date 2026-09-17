import os
import sqlite3
from flask import Flask, render_template, request, redirect,jsonify
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY']=os.getenv('SECRET_KEY')
db_path=os.getenv('DATABASE_PATH','coffee_shop.db')
    
def init_db():
    conn=sqlite3.connect(db_path)
    cursor=conn.cursor()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Item TEXT NOT NULL,
            Quantity TEXT NOT NULL,
            Topping TEXT NOT NULL)''')
    conn.commit()
    conn.close()

init_db()
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/order', methods=['GET', 'POST'])
def order_page():
    if request.method == 'POST' :
        coffee_choice = request.form.get('coffee')
        size_choice = request.form.get('quantity')
        topping_choice = request.form.get('topping')
        
        conn=sqlite3.connect(db_path)
        cursor=conn.cursor()
        cursor.execute('''
            INSERT INTO orders (Item,Quantity,Topping) values(?,?,?)''',(coffee_choice,size_choice,topping_choice))
        Order_ID = cursor.lastrowid
        conn.commit()
        conn.close()
        

        print("\n--- NEW ORDER RECEIVED ---")
        print(f"Item: {coffee_choice}")
        print(f"Size: {size_choice}")
        print(f"Topping: {topping_choice}")
        print("--------------------------\n")
        

        return jsonify({
            "Status" : "success",
            "Massage" : "Order Placed",
            "Order ID" : Order_ID,
            "Item" : coffee_choice,
            "Quantity" : size_choice,
            "Toppings" : topping_choice})
            


    return render_template('index.html')


import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
