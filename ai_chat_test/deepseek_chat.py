import json
from add import add
from openai import OpenAI
from linear_regression import linear_regression

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
                    "y":{
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "The y-axis parameter list",
                    }
                },
                "required": ["X","y"]
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
                "x":{
                    "type": "number",
                    "description": "The first number to be added.",
                },
                "y":{
                    "type": "number",
                    "description": "The second number to be added.", }
            },
            "required": ["X","y"]
        }
    }
]

client = OpenAI(
    api_key="my_api_key",
    base_url="https://api.deepseek.com",
)

def send_messages(messages,tools = None):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        tools=tools,
        # response_format={
        #     'type': 'json_object'
        # }
    )
    return response

def use_tools(json_data):
    function_name = json.loads(json_data)["choices"][0]["message"]["tool_calls"][0]["function"]["name"]
    arguments = json.loads(json_data)["choices"][0]["message"]["tool_calls"][0]["function"]["arguments"]

    if function_name == "linear_regression":
        function_mapper = {
            "linear_regression": linear_regression
        }

    elif function_name == "add":
        function_mapper = {
            "add": add
        }
    function = function_mapper.get(function_name)
    if arguments == {}:
        function_output = "No arguments provided."
        print("No arguments")
    else:
        function_output = function(json.loads(arguments)["x"], json.loads(arguments)["y"])
        print(f"AI:{function_output}\n")
        messages = [
            {"role": "user",
                "content": "Please summarize the process of my tool usage." + str(function_output)},
            {"role": "system", "content": ""}
        ]
        answer = send_messages(messages, tools)
        print(json.dumps(answer.to_dict()))
        answer_data = json.loads(json.dumps(answer.to_dict()))["choices"][0]["message"]["content"]
        print(f"AI:{answer_data}\n")

def main_loop():
    print("Welcome to DeepSeek")
    while True:
        try:
            #获取用户输入
            user_input = input("user input:(input 'exit' to quit):")

            if user_input == "exit":
                break

            messages = [
                {"role": "user",
                 "content": user_input},
                {"role": "system", "content": ""}
            ]

            response = send_messages(messages, tools)
            if not response:
                print("No response")

            if response:
                # print(response)
                json_data = json.dumps(response.to_dict())
                if(json.loads(json_data)["choices"][0]["finish_reason"]=="tool_calls"):
                    use_tools(json_data)
                else:
                    answer_data = json.loads(json.dumps(response.to_dict()))["choices"][0]["message"]["content"]
                    print(f"AI:{answer_data}")
            else:
                print(f"AI{response.choices[0].message.content}")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {str(e)}")
if __name__ == "__main__":
    main_loop()
