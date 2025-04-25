import json
from ai_chat_test.utils.util import send_messages, use_tools
from ai_chat_test.utils.tools import tools

def main_loop():
    print("Welcome to DeepSeek")
    while True:
        try:
            #Get the user input
            user_input = input("user input(input 'exit' to quit):")

            if user_input == "exit":
                print("Goodbye!")
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
