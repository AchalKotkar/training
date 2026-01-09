import practice as p


while True:
    c=int(input((f"1.Add new user \n2.Get user info \n3.Show all \n4.Exit\n")))
    match c:
        case 1: 
            name=input("Enter user name: ")
            age=int(input("Enter user age: "))
            print(p.add_new_user(name,age))
            print(p.get_all_info())
        case 2:
            user_id=int(input("Enter user_id you want to get info: "))
            print(p.get_user_info(user_id))
        case 3:
            print(p.get_all_info())
        case 4: break
