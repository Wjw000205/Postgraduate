tools = [
    {
        "type": "function",
        "function": {
            "name": "linear_regression",
            "description": "Perform linear regression on the given data.",
            "parameters": {
                "type": "object",
                "properties": {
                    "x": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "The x-axis parameter list",
                    },
                    "y": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "The y-axis parameter list",
                    }
                },
                "required": ["x", "y"]
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "add",
            "description": "Add two numbers.",
            "parameters": {
                "type": "object",
                "x": {
                    "type": "number",
                    "description": "The first number to be added.",
                },
                "y": {
                    "type": "number",
                    "description": "The second number to be added.",
                }
            },
            "required": ["x", "y"]
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the weather based on the province and city",
            "parameters": {
                "type": "object",
                "province": {
                    "type": "string",
                    "description": "The province"
                },
                "city": {
                    "type": "string",
                    "description": "The city"
                },
            "required": ["province", "city"]
            }
        }
    }
]
