from rich.console import Console
from tools.weather import get_weather

console = Console()

def main():
    console.print("[bold green]Hello World![/bold green]")
    console.print("This is your AI Chatbot. Ready to call tools!")

    location = "Melbourne"
    weather_info = get_weather(location)
    console.print(f"[bold blue]Weather Info:[/bold blue] {weather_info}")


if __name__ == "__main__":
    main()
