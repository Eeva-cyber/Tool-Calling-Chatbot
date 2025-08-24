def calculate(operation: str, x: float, y: float) -> str:
    try:
        if operation == "add":
            return str(x + y)
        elif operation == "subtract":
            return str(x - y)
        elif operation == "multiply":
            return str(x * y)
        elif operation == "divide":
            return str(x / y)
        else:
            return "Unknown operation"
    except Exception as e:
        return f"Error: {e}"