from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///form.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class form(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    fname=db.Column(db.String(100), nullable=False)
    email=db.Column(db.String(100))
    phno=db.Column(db.Integer)
    date_created=db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self)->str:
        return f"{self.fname} - {self.email} - {self.phno}"

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/html",methods=['GET','POST'])
def learnhtml():
    if request.method=='POST':
        # print("post")
        title=request.form['fullname']
        emailid=request.form['email']
        pnum=request.form['phoneNo']
        form1=form(fname=title,email=emailid,phno=pnum)
        db.session.add(form1)
        db.session.commit()
    allform=form .query.all()

    return render_template('index.html',myans=allform)
@app.route("/show")
def show():
    # allform=form .query.all()
    return"hello"
if __name__== "__main__" :
    app.run(debug=True)