from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database setup (SQLite for local, later you can switch to MySQL or PostgreSQL for production)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grocery_inventory.db'
db = SQLAlchemy(app)

# Database model for Grocery Inventory
class Grocery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    gst = db.Column(db.Float, nullable=False, default=18.0)  # Default GST is 18%
    total_price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Grocery {self.name}>'

@app.route('/')
def index():
    groceries = Grocery.query.all()  # Fetch all grocery items from the database
    return render_template('index.html', groceries=groceries)

@app.route('/add', methods=['POST'])
def add_grocery():
    if request.method == 'POST':
        name = request.form['name']
        quantity = int(request.form['quantity'])
        price = float(request.form['price'])
        gst = float(request.form['gst'])
        total_price = quantity * price * (1 + gst / 100)
        
        new_grocery = Grocery(name=name, quantity=quantity, price=price, gst=gst, total_price=total_price)
        db.session.add(new_grocery)
        db.session.commit()
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
