import datetime
from flask import Flask,request,render_template
from flask_sqlalchemy import SQLAlchemy

# create the extension
db = SQLAlchemy()
# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# initialize the app with the extension
db.init_app(app)


class Post(db.Model):
    ID= db.Column(db.Integer, primary_key=True)
    Title=db.Column(db.String, unique=False, nullable=False)
    Caption=db.Column(db.String, unique=False, nullable=True)
    Image_url=db.Column(db.String, unique=False, nullable=True)
    Timestamp=db.Column(db.String, unique=True, nullable=False)
    user_Username = db.Column(db.String, db.ForeignKey('user.Username'),
        nullable=False)
  
class User(db.Model):
    Username=db.Column(db.String, primary_key=True)
    Password=db.Column(db.String, unique=False, nullable=False)
    No_of_followers=db.Column(db.Integer, unique=False, nullable=False,default=0)
    No_of_posts=db.Column(db.Integer, unique=False, nullable=False,default=0)
    user_posts = db.relationship('Post', backref='user', lazy=True) #hidden


with app.app_context():
    db.create_all()
    

posts=[] 
data={}
data["users"]=[]
user1={"username":"gokul","posts":[]}
@app.route("/")
def hello_world():
    return render_template("login.html")
@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]
        print(username,password)
        # if data["users"]
        return render_template("landing.html",data={"posts":[1234]})
    else:
        return render_template("signup.html")
from models import user
users=[]

@app.route("/signup",methods=["GET","POST"])
def signup():
    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]
        confirmpassword=request.form["confirm-password"]
        print(username)
        print(password)
        print(confirmpassword)
        if password==confirmpassword:
            u1=user(username,password)
            users.append(u1)
            print(users)
            return render_template("login.html")
        else:
            return render_template("signup.html",message="Passwords doesn't match")
        print(username,password)
    else:
        return render_template("signup.html")

@app.route("/addpost",methods=["POST"])
def addpost():
    # ID=request.form.get("ID")
    Title=request.form.get("Title")
    Caption=request.form.get("Caption")
    Image_url=request.form.get("IMAGE_URL")
    time=datetime.datetime.now()
    user_Username=request.form.get("user_Username")
    post=Post(Title=Title,Caption=Caption,Image_url=Image_url,Timestamp=time,user_Username=user_Username)

    db.session.add(post)
    db.session.commit()
    return "post added"

@app.route("/getallpost")
def getallpost():
  
    x=Post.query.all()
    print(x)
    posts=[]
    for i in x:
       
        print(i.__dict__.pop("_sa_instance_state"))
        posts.append(i.__dict__)
       
       # posts.append(i.__dict__.pop("_sa_instance_state"))
    return posts

@app.route("/adduser",methods=["POST"])
def adduser():
    Username=request.form.get("Username")
    Password=request.form.get("Password")
    user=User(Username=Username,Password=Password)
    
    db.session.add(user)
    db.session.commit()
    return "user added"
if __name__=="__main__":
    app.run(debug=True)