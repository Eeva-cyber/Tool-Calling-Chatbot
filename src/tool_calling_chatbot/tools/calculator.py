def calculate(operation: str, x: float, y: float) -> str:
    if operation == "add":
        return str(x + y)
    elif operation == "subtract":
        return str(x - y)
    elif operation == "multiply":
        return str(x * y)
    elif operation == "divide":
        if y == 0:
            return "Error: Division by zero"
        return str(x / y)
    else:
        return "Error: Invalid operation"
