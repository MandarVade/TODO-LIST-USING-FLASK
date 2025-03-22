from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///form.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class form(db.Model):
    id  = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone_number = db.Column(db.BigInteger, nullable=False, unique=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.full_name} - {self.email} - {self.phone_number}"

@app.route("/")
def home():
    return "<p>Hello, World!</p>"

@app.route("/html", methods=['GET', 'POST'])
def form_page():
    if request.method == 'POST':
        full_name = request.form['fullname']
        email = request.form['email']
        phone_number = request.form['phoneNo']
        new_entry = form(full_name=full_name, email=email, phone_number=phone_number)
        db.session.add(new_entry)
        db.session.commit()
    entries = form.query.all()
    return render_template('index.html', entries=entries)

@app.route("/delete/<int:id>")
def delete_entry(id):
    entry = form.query.filter_by(id=id).first()
    if entry:
        db.session.delete(entry)
        db.session.commit()
    return redirect("/html")

@app.route("/update/<int:id>" ,methods=['GET', 'POST'])
def update(id):
    if request.method=='POST':
        full_name = request.form['fullname']
        email = request.form['email']
        phone_number = request.form['phoneNo']
        entry = form.query.filter_by(id=id).first()
        entry.full_name=full_name
        entry.email=email
        entry.phone_number=phone_number
        db.session.add(entry)
        db.session.commit()
        return redirect("/html")
    entry = form.query.filter_by(id=id).first()
    return render_template('update.html', entry=entry)
    
if __name__ == "__main__":
    app.run(debug=True)