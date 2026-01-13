def add(a, b):
    print(a+b)
    return a + b


def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    print(a/b)
    return a / b
