def math_operation():
    """
    Day 1
    Perform basic arithmetic operations on two numbers.
    
    Prompts user for two numbers and an operator, then calculates and displays
    the result. Supports addition, subtraction, multiplication, and division.
    Handles division by zero and invalid operators.
    """
    num1 = input("Enter first number: ")
    num2 = input("Enter first number: ")
    num1 = float(num1)
    num2 = float(num2)
    operator = input("Enter operator (+, -, *, /): ")
    if operator == "+":
        result = num1 + num2
    elif operator == "-":
        result = num1 - num2
    elif operator == "*":
        result = num1 * num2
    elif operator == "/":
        if num2 != 0:
            result = num1 / num2
        else:
            result = "Error: Division by zero"
    else:
        result = "Error: Invalid operator"
    print("Result:", result)

def convert_temp():
    """
    Day 2
    Convert temperature between Celsius and Fahrenheit.
    
    Prompts user for a temperature value and unit (C or F), then converts
    to the opposite unit and displays the result. Validates the unit input.
    """
    temp = input("Enter temperature: ")
    temp = float(temp)
    unit = input("Enter unit (C for Celsius, F for Fahrenheit): ")
    if unit.upper() == "C":
        temp_converted = (temp - 32) * 5/9
    elif unit.upper() == "F":
        temp_converted = (temp * 9/5) + 32
    else:        
        print("Error: Invalid unit")
        return
    print("Temperature is :", temp_converted , " ", unit.upper())

def student_grades():
    """
    Day 3
    Calculate average grade and determine letter grade.
    
    Prompts user for grades in multiple subjects, calculates the average,
    and assigns a letter grade based on the average. Handles invalid input.
    """
    grades = {}
    num_students = int(input("Enter number of students: "))
    for i in range(num_students):
        name = input(f"Enter name of student {i+1}: ")
        grade = float(input(f"Enter grade for {name}: "))
        grades[name] = grade
    average = sum(grades.values()) / num_students
    maximum = max(grades.values())
    minimum = min(grades.values())
    for name, grade in grades.items():
        print(f"{name}: Grade = {grade}, Letter Grade = {grade}")   
    print(f"Average Grade: {average}")
    print(f"Highest Grade: {maximum}")
    print(f"Lowest Grade: {minimum}")


def main():
    """Main entry point of the program.
    
    Executes the temperature conversion function.
    """
    student_grades()


if __name__ == "__main__":
    main()
