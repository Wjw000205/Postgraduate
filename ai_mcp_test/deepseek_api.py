import json
import sys

from lxml.etree import tostring
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
    api_key="sk-cf46ee3bc9954e0ab809f4aec1800071",
    base_url="https://api.deepseek.com",
)

def send_messages(messages,tools):
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
elif response:
    # print(response)
    json_data = json.dumps(response.to_dict())
    # print(json_data)
    function_name =json.loads(json_data)["choices"][0]["message"]["tool_calls"][0]["function"]["name"]
    arguments = json.loads(json_data)["choices"][0]["message"]["tool_calls"][0]["function"]["arguments"]

    # print(function_name)
    # print(arguments)
    # arguments = json.loads(arguments_string)
    #
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
else:
    print(f"AI{response.choices[0].message.content}\n")
# message = send_messages(messages)
# print(f"User>\t {messages[0]['content']}")
#
# tool = message.tool_calls[0]
# messages.append(message)
#
# messages.append({"role": "tool", "tool_call_id": tool.id, "content": "Linear regression completed. θ0: 0, θ1: 2."})
# message = send_messages(messages)
# print(f"Model>\t {message.content}")