import datetime
from flask import Flask, flash, redirect,request,render_template,session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from sqlalchemy.ext.hybrid import hybrid_property
import os

# create the extension
db = SQLAlchemy()

UPLOAD_FOLDER = './static'

# SESSION_TYPE = 'memcache'

# create the app
PEOPLE_FOLDER = os.path.join('static', 'people_photo')
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project_santh.db"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# initialize the app with the extension
db.init_app(app)
Session(app)
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
class Post(db.Model):
    __tablename__="post"
    ID= db.Column(db.Integer, primary_key=True)
    Title=db.Column(db.String, unique=False, nullable=False)
    Caption=db.Column(db.String, unique=False, nullable=True)
    Image_url=db.Column(db.String, unique=False, nullable=True)
    post_timestamp=db.Column(DateTime,default=datetime.datetime.now)
    post_user = db.Column(db.String, ForeignKey('user.Username',ondelete="CASCADE"),nullable=False)
    # post_user_rel = db.relationship("User", backref="post")
    
    
user_follows = db.Table('user_follows',
    db.Column('follower_name', db.Integer, db.ForeignKey('user.Username')),
    db.Column('followed_name', db.Integer, db.ForeignKey('user.Username'))
)
# class User_follows(db.Model):
#     __tablename__="followers"
#     follower_name=db.Column(db.String, db.ForeignKey('user.Username'),primary_key=True),
#     followed_name=db.Column(db.String, db.ForeignKey('user.Username'),primary_key=True)


class User(db.Model):
    __tablename__="user"
    Username=db.Column(db.String, primary_key=True)
    Password=db.Column(db.String, unique=False, nullable=False)
    # No_of_followers=db.Column(db.Integer, unique=False, nullable=False,default=0)
    # No_of_posts=db.Column(db.Integer, unique=False, nullable=False,default=0)
    # user_follows=db.Column(db.String,db.ForeignKey('user.Username'),default="")
    # following_user=db.Column(db.String,db.ForeignKey('user.Username'),default="")
    # user_following = db.relationship('User_follows', backref='user', lazy=True) #hidden
    userpost = db.relationship("Post", backref="user",cascade="all, delete")
    followed = db.relationship(
        'User', secondary=user_follows,
        primaryjoin=(user_follows.c.follower_name == Username),
        secondaryjoin=(user_follows.c.followed_name == Username),
        backref=db.backref('user_follows', lazy='dynamic'), lazy='dynamic')
    @hybrid_property
    def No_of_followers(self):
        x=self.following_user
        return len(self.following_user)

with app.app_context():
    db.create_all()
    

posts=[] 
data={}
data["users"]=[]
user1={"username":"gokul","posts":[]}
@app.route("/")
def hello_world():
    return render_template("login.html")

@app.route("/confirm/delete/post/<user>/<post_ID>")
def deletepost(user,post_ID):
    data["username"]=user
    data["post_ID"]=post_ID
    return render_template("confirmdelete.html",data=data)

@app.route("/delete/post/confirmed/<user>/<post_id>")
def confirmed_delete_post(user,post_id):
    p1=Post.query.filter(Post.ID==post_id).first()
    db.session.delete(p1)
    db.session.commit()
    flash(f"post with id : {post_id} deleted successfully")
    return redirect(f"/profile/{user}")




@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]
        u1=User.query.filter(User.Username==username).first()
        if not u1:
            return render_template("login.html",message="user not found")
        else:

            data["username"]=u1.Username
            session["name"] = username
            return render_template("home.html",message="There are no posts in your feed.Connect with other users to see what they are posting",data=data)
    else:
        return render_template("signup.html")
    
@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")


@app.route("/signup",methods=["GET","POST"])
def signup():
    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]
        confirmpassword=request.form["confirm-password"]
        
        # print(username)
        # print(password)
        # print(confirmpassword)
        if password==confirmpassword:
            u1=User(Username=username,Password=password)
            db.session.add(u1)
            db.session.commit()
            # print(users)
            return render_template("login.html",message="user created successfully.Now you can login")
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

@app.route("/profile/<user>",methods=["GET","POST"])
def profile(user):
    print("inside path parameter")
    print("user",user)
    data["username"]=user
    u1=User.query.filter(User.Username==user).first()
    print(u1)
    # print(u1.Username)
    x=u1.userpost
    for i in x:
        print(i.ID)
        print(i.Title)
        print(i.Caption)
        print(i.Image_url)
    data["posts"]=x
    
    return render_template("posts.html",data=data)

@app.route("/add_a_post/<user>",methods=["GET","POST"])
def add_a_post(user):
    if request.method=="POST":
        title=request.form.get("title")
        caption=request.form.get("caption")
        file=request.files['img']
        count=User.query.filter(User.Username==user).first()
        count=count.userpost
        print(count)
        filename=user+title+file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        p1=Post(Title=title,Caption=caption,Image_url=filename,post_user=user)
        db.session.add(p1)
        db.session.commit()
        data["username"]=user
        return redirect(f"/profile/{user}")
        
    print(user)
    data["username"]=user
    return render_template("addpost.html",data=data)


@app.route("/edit/post/<user>/<post_id>",methods=["GET","POST"])
def edit_post(user,post_id):
    if request.method=="POST":
        print("inside edite post")
        p1=Post.query.filter(Post.ID==post_id).first()
        title=request.form.get("title")
        p1.Title=title
        file=request.files['img']
        p1.Caption=request.form.get("caption")
        filename=user+title+file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        p1.Image_url=filename
        db.session.commit()
        return redirect(f"/profile/{user}")
    p1=Post.query.filter(Post.ID==post_id).first()
    data["username"]=user
    data["post"]=p1
    print("in edit get request")
    return render_template("editpost.html",data=data,message=f"edit post id : {post_id}")

if __name__=="__main__":
    app.run(debug=True)