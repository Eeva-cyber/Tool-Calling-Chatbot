from .calculator import calculate
from .weather import get_weather

# Map tool names to functions
local_tools = {
    "get_weather": get_weather,
    "calculate": calculate
}