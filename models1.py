users=[]
class user:
    def __init__(self,username,password):
        self.username=username
        self.password=password

u1=user("gokul","gokul")
u2=user("santheri","santheri")
users.append(u1)
users.append(u2)
print(users)
for i in users:
    print(i.username)
    print(i.password)
