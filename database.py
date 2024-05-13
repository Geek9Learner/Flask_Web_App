import json
class Database:
    def __init__(self) -> None:
        pass
    def insert(self,name,email,password):
        with open('users.json','r') as rf:
            user = json.load(rf)
            if email in user:
                return 0
            else:
                user[email] = [name,password]
        with open('users.json','w') as rf:
            json.dump(user,rf,indent=4)
            return 1
    def search(self,email,password):
        with open('users.json','r') as rf:
            users = json.load(rf)
            if email in users:
                if users[email][1] == password:
                    return 1
                else:
                    return 0
            else:
                return 0