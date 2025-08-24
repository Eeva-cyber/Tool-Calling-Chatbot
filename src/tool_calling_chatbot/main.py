import os
import json
import re
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from openai import OpenAI

# local tool imports
from tools import local_tools

# Load API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

console = Console()

# ----------------------
# Define available tools
# ----------------------
tools = [
    {
        "name": "get_weather",
        "description": "Get the current weather for a specific location.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "The location to get the weather for."}
            },
            "required": ["location"]
        }
    },
    {
        "name": "calculate",
        "description": "Perform basic arithmetic operations.",
        "parameters": {
            "type": "object",
            "properties": {
                "operation": {"type": "string", "enum": ["add","subtract","multiply","divide"], "description": "The operation to perform."},
                "x": {"type": "number", "description": "First number."},
                "y": {"type": "number", "description": "Second number."}
            },
            "required": ["operation","x","y"]
        }
    }
]

# ----------------------
# Conversation memory
# ----------------------
messages = [
    {"role": "system", "content": "You are a helpful assistant. Always use the provided tools for calculations and weather queries. Do not answer directly."}
]

# ----------------------
# Run local tool
# ----------------------
def run_tool(function_name, **arguments):
    if function_name in local_tools:
        return local_tools[function_name](**arguments)
    return f"Unknown tool: {function_name}"

# ----------------------
# Preprocess simple arithmetic input
# ----------------------
def preprocess_input(user_input: str) -> str:
    match = re.match(r"^\s*(\d+(?:\.\d+)?)\s*([\+\-\*/])\s*(\d+(?:\.\d+)?)\s*$", user_input)
    if match:
        x, op, y = match.groups()
        ops_map = {"+":"add", "-":"subtract", "*":"multiply", "/":"divide"}
        return f"calculate x={x} y={y} operation={ops_map[op]}"
    return user_input

# ----------------------
# Chat with function calling
# ----------------------
def chat_with_functions(user_input: str) -> str:
    user_input = preprocess_input(user_input)
    messages.append({"role": "user", "content": user_input})

    # 1️⃣ First call to model
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        functions=tools,
        function_call="auto"
    )
    assistant_message = response.choices[0].message

    # 2️⃣ Check if a function call is requested
    func_call = getattr(assistant_message, "function_call", None)
    if func_call:
        function_name = func_call.name
        arguments = json.loads(func_call.arguments)

        console.print(f"[bold yellow]Calling function:[/bold yellow] {function_name} with arguments {arguments}")
        try:
            result = run_tool(function_name, **arguments)
        except Exception as e:
            console.print(f"[bold red]Error calling function {function_name}:[/bold red] {e}")
            result = None

        # 3️⃣ Send function result back to model for final response
        # Append assistant message first to keep the chain
        messages.append(assistant_message.model_dump())

        # The SDK handles function results via a "message from assistant with role 'assistant'"
        messages.append({
            "role": "function",
            "name": function_name,
            "content": str(result)
        })

        final_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        final_message = final_response.choices[0].message
        messages.append(final_message.model_dump())
        return final_message.content or "[bold red]No response from assistant[/bold red]"

    # 4️⃣ If no function call, just return content
    messages.append(assistant_message.model_dump())
    return assistant_message.content or "[bold red]No response from assistant[/bold red]"

# ----------------------
# Main loop
# ----------------------
def main():
    console.print(Panel("[bold green]Welcome to your AI chatbot![/bold green]", expand=False))

    while True:
        user_input = console.input("What do you need me to do today?\n")

        if user_input.lower() in ["exit", "quit"]:
            console.print(Panel("[bold red]Goodbye![/bold red]", expand=False))
            break

        response = chat_with_functions(user_input)
        console.print(Panel(response, title="[bold green]Assistant[/bold green]", expand=False))

# ----------------------
# Entry point
# ----------------------
if __name__ == "__main__":
    main()