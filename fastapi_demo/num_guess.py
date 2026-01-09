import random

num=random.randint(1,50)
while True:
    x=int(input("Enter the number:"))
    if x==num:
        print("Correct guess")
        break
    else:
        print("Sorry!! Try again")