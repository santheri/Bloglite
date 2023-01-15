from main import app,User,Post

with app.app_context():
    x=User.query.first()
    print(x.userpost)