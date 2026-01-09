num=int(input("Enter number: "))
a,b=0,1

print("Fibonacci Series upto ",num)
for n in range(num):
    print(a)
    a,b=b,a+b