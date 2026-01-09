users=[]

def add_new_user(name:str, age:int):
    user={"id":len(users)+1, "Name":name, "Age":age}
    users.append(user)
    return user,"is added"

def get_all_info():
    return users

def get_user_info(user_id:int):
    for user in users:
        if user["id"]== user_id:
            return user
    return "No user with this id"
