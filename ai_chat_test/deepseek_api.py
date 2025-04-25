import json
from traceback import print_tb

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
                    "X": {
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
]

client = OpenAI(
    api_key="sk-f0473cbc74c54482bb2c167a31af6c35",
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

    function_mapper = {
        "linear_regression": linear_regression
    }
    #
    function = function_mapper.get(function_name)
    if arguments == {}:
        function_output = "No arguments provided."
        print("No arguments")
    else:
        function_output = function(json.loads(arguments)["X"], json.loads(arguments)["y"])
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
            user_input = input("用户输入(输入exit离开):")

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
            print("\n再见！")
            break
        except Exception as e:
            print(f"发生错误: {str(e)}")
if __name__ == "__main__":
    main_loop()
