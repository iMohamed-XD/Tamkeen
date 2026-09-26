OPERATIONS = ("+", "-", "*", "/", "%", "**")
while True:
    try:
        num1 = float(input("Enter the first number: "))
        operation = input("Enter an operation (+, -, *, /, %, **): ")
        if operation not in OPERATIONS:
            print("Invalid operation. Please choose from +, -, *, /, %, **.")
            continue
        num2 = float(input("Enter the second number: "))
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        continue
    if operation == "+":
        result = num1 + num2
    elif operation == "-":
        result = num1 - num2
    elif operation == "*":
        result = num1 * num2
    elif operation == "/":
        if num2 == 0:
            print("Error: Division by zero is not allowed.")
            continue
        result = num1 / num2
    elif operation == "%":
        if num2 == 0:
            print("Error: Division by zero is not allowed.")
            continue
        result = num1 % num2
    elif operation == "**":
        result = num1 ** num2
    print(f"The result of {num1} {operation} {num2} is {result}")
    choice = input("Do you want to perform another calculation? (y/n): ")
    if choice.lower() != "y":
        break