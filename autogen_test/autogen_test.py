from autogen import ConversableAgent
from linear_regression import linear_regression

config_list = [
    {
        "model": "deepseek-chat",
        "api_key": "sk-03e0772701994468ab87c85964e90af7",
        "api_type": "deepseek"
    }
]
# client = OpenAI(api_key="<DeepSeek API Key>", base_url="https://api.deepseek.com")
# Let's first define the assistant agent that suggests tool calls.
assistant = ConversableAgent(
    name="Assistant",
    llm_config={"config_list": config_list},
)

# The user proxy agent is used for interacting with the assistant agent
# and executes tool calls.
user_proxy = ConversableAgent(
    name="User",
    llm_config=False,
    # is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
    human_input_mode="NEVER",
)

# Register the tool signature with the assistant agent.
assistant.register_for_llm(name="linear_regression", description="A simple linear_regression")(linear_regression)

# Register the tool function with the user proxy agent.
user_proxy.register_for_execution(name="linear_regression")(linear_regression)

chat_result = user_proxy.initiate_chat(assistant, message="生成10个随机坐标并返回线性函数")