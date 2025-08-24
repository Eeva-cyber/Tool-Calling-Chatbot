from rich.console import Console
from rich.panel import Panel
from tools.weather import get_weather
from tools.calculator import calculate

console = Console()

# the tools we have (get weather and calculator)
tools = {
    "weather": {
        "function": get_weather,
        "description": "Get the current weather for a specific location."
    },
    "calculator": {
        "function": calculate,
        "description": "Perform basic arithmetic operations."
    }
}

# messages
messages = [
    {"role": "assistant", "content": "You are a helpful assistant that can answer questions and call tools."},
]

# choose tool, kwargs allow the parameters to be more flexible
def run_tool(tool_name, **kwargs):
    if tool_name == "weather":
        return tools[tool_name]["function"](kwargs["location"])
    elif tool_name == "calculator":
        return tools[tool_name]["function"](kwargs["operation"], kwargs["x"], kwargs["y"])
    else:
        return "Unknown tool"
    

# main function - ask for user response
def main():
    console.print(Panel("[bold green]Welcome to your AI chatbot![/bold green]", expand=False))

    while True:
        console.print("\nAvailable tools: [bold blue]weather[/bold blue], [bold blue]calculator[/bold blue]")
        user_input = console.input("Which tool do you want to run? (or 'exit'): ").strip().lower()

        if user_input.lower() in ["exit", "quit"]:
            console.print(Panel("[bold red]Goodbye![/bold red]", expand=False))
            break

        # add user message to memory
        messages.append({"role": "user", "content": user_input})

        # manually choose tool based on keyword first
        response = ""
        if "weather" in user_input.lower():
            location = console.input("Enter the location: ")
            result = run_tool("weather", location=location)   
            response = f"[bold cyan]{result}[/bold cyan]"
        elif "calculator" in user_input.lower():
            operation = console.input("Operation: ")
            x = float(console.input("First number: "))
            y = float(console.input("Second number: "))
            result = run_tool("calculator", operation=operation, x=x, y=y)
            response = f"[bold cyan]{result}[/bold cyan]"
        else:
            response = "[bold red]I do not know which tool to use yet[/bold red]"


        # add the assistant's response into the chat memory
        messages.append({"role": "assistant", "content": response})
        console.print(Panel(response, title="[bold green]Assistant[/bold green]", expand=False))

if __name__ == "__main__":
    main()
