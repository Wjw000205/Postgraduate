import json
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
    api_key="my_api_key",
    base_url="https://api.deepseek.com",
)

def send_messages(messages,tools = None):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        tools=tools
    )
    return response

messages = [
    {"role": "user","content": "Please perform a linear regression with the following data: X=[1,2,3], y=[2,4,6]."},
    {"role":"system","content":""}
]

response = send_messages(messages,tools)
if not response:
    print("No response")
# if response.choices[0].message.tool_calls:
#     function_name = response.choices[0].message.tool_calls[0].function.name
#     arguments_string = response.choices[0].message.tool_calls[0].function.arguments
#     arguments = json.loads(arguments_string)
if response:
    # print(response)
    json_data = json.dumps(response.to_dict())
    # print(json_data)
    function_name =json.loads(json_data)["choices"][0]["message"]["tool_calls"][0]["function"]["name"]
    arguments = json.loads(json_data)["choices"][0]["message"]["tool_calls"][0]["function"]["arguments"]

    # print(function_name)
    # print(arguments)
    function_mapper = {
        "linear_regression": linear_regression
    }
    # #
    function = function_mapper.get(function_name)
    if arguments == {}:
        function_output = function()
    else:
        function_output = function(json.loads(arguments)["X"],json.loads(arguments)["y"])
    print(f"AI:{function_output}\n")
    messages = [
        {"role": "user",
         "content": "Please summarize the process of my tool usage."+str(function_output)},
        {"role": "system", "content": ""}
    ]
    answer = send_messages(messages)
    answer_data =json.loads(json.dumps(answer.to_dict()))["choices"][0]["message"]["content"]
    print(f"AI:{answer_data}\n")

else:
    print(f"AI{response.choices[0].message.content}\n")
