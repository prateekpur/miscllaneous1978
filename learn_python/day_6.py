"""
    Math utility functions, user selects operation and correct method gets invoked
"""
def add(num1 , num2):
    return num1 + num2

def subtract(num1, num2):
    return num1 - num2

def multiply(num1, num2):
    return num1 * num2

def divide(num1, num2):
    return num1 / num2

# Mapping operations to function objects
actions = {
    "+": add,
    "-": subtract,
    "*": multiply,
    "/": divide
}

operation = input("Choose an operation")
num1 = (int)(input("Number 1 : "))
num2 = (int)(input("Number 2 : "))
# Calling a function from the dictionary
result = actions[operation](num1, num2)
print(f"Result : ", result)
