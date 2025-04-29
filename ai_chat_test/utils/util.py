import json

from openai import OpenAI

from ai_chat_test.functions.get_weather import get_weather
from ai_chat_test.functions.add import add
from ai_chat_test.functions.linear_regression import linear_regression
from ai_chat_test.utils.tools import tools
from rich import print

client = OpenAI(
    api_key="sk-724b234be62c4f0085db7b8ec8a3b6d2",
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
    messages_temp = ""
    function_name = json.loads(json_data)["choices"][0]["message"]["tool_calls"][0]["function"]["name"]
    arguments = json.loads(json_data)["choices"][0]["message"]["tool_calls"][0]["function"]["arguments"]
    role = json.loads(json_data)["choices"][0]["message"]["role"]

    if function_name == "linear_regression":
        function_mapper = {
            "linear_regression": linear_regression
        }
        function = function_mapper.get(function_name)
        if arguments == {}:
            function_output = "No arguments provided."
            print("No arguments")
            messages_temp = messages_temp + function_output
            return None
        else:
            function_output = function(json.loads(arguments)["x"], json.loads(arguments)["y"])
            messages_temp = messages_temp + "tool calling result:" + str(function_output) + ";"

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
            messages_temp = messages_temp + answer_data
            return {"role": role, "content": messages_temp}

    elif function_name == "add":
        function_mapper = {
            "add": add
        }
        function = function_mapper.get(function_name)
        if arguments == {}:
            function_output = "No arguments provided."
            print("No arguments")
            messages_temp = messages_temp + function_output
            return None
        else:
            function_output = function(json.loads(arguments)["x"], json.loads(arguments)["y"])
            messages_temp = messages_temp + "tool calling result:" + str(function_output) + ";"

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
            messages_temp = messages_temp + answer_data
            return {"role": role, "content": messages_temp}
    elif function_name == "get_weather":
        function_mapper = {
            "get_weather": get_weather
        }

        function = function_mapper.get(function_name)
        if arguments == {}:
            function_output = "No arguments provided."
            print("No arguments")
            messages_temp = messages_temp + function_output
            return None
        else:
            function_output = function(json.loads(arguments)["province"],json.loads(arguments)["city"])
            messages = [
                {"role": "user",
                 "content": "Get the data base on the json,and give some introduction about it:" + str(function_output)},
                {"role": "system", "content": ""}
            ]

            answer = send_messages(messages, tools)
            answer_data = json.loads(json.dumps(answer.to_dict()))["choices"][0]["message"]["content"]
            print(f"AI:{answer_data}\n")
            messages_temp = messages_temp + answer_data
            return {"role": role, "content": messages_temp}


    return None


def get_weather_tool(json_data):
    print(json.dumps(json.loads(json_data)))