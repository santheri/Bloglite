from main import User,Post,db,app

def delete_db():
    with app.app_context():
        db.drop_all()

def create_db():
    with app.app_context():
        db.create_all()
        
def add_data(data):
    for i in data:
        with app.app_context():
            db.session.add(i)
            db.session.commit()
            
def get_posts_user():
    with app.app_context():
        users=User.query.all()
        print("aaaaaaaaaaaa")
        print(users)
        for i in users:
            print("bbbbbbbbbbbbbb")
            print(i.userpost)
            print(i.user_following)


def create_users_and_posts():
    u1=User(Username="gokul",Password="pwd")
    u2=User(Username="santh",Password="pwd")
    u3=User(Username="myth",Password="pwd")
    p1=Post(Title="title1",Caption="caption1",Image_url="",post_user="gokul")
    p2=Post(Title="title2",Caption="caption2",Image_url="",post_user="santh")
    p3=Post(Title="title3",Caption="caption3",Image_url="",post_user="gokul")
    p4=Post(Title="title4",Caption="caption4",Image_url="",post_user="santh")
    p5=Post(Title="title5",Caption="caption5",Image_url="",post_user="gokul")
    p6=Post(Title="title6",Caption="caption6",Image_url="",post_user="mythi")
    
    # f1=followers()
    add_data([u1,u2,u3,p1,p2,p3,p4,p5,p6])
    
def add_followers():
    with app.app_context():
        u0=User.query.filter(User.Username=="santh").first()
        u1=User.query.filter(User.Username=="myth").first()
        u2=User.query.filter(User.Username=="gokul").first()
        u2.followed.append(u0)
        u2.followed.append(u1)
        # u1.No_of_followers="gokul"
        # u1.No_of_followers.append(User.query.filter(User.Username=="santh"))
        db.session.commit()

def get_no_of_followers():
    with app.app_context():
        u1=User.query.filter(User.Username=="gokul").first()
        print("cccccccccccccc")
        print(u1)
        print(u1.Username)
        print(u1.following_user)
        print(u1.No_of_followers)

def delete_user():
    with app.app_context():
        User.query.filter(User.Username=="gokul").delete(synchronize_session=False)
        db.session.commit()

#---------------
#--------------------------

        
delete_db()
create_db()
create_users_and_posts()
# get_posts_user()
# delete_user()


add_followers()
# get_no_of_followers()