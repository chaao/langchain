from langchain.agents import load_tools, initialize_agent, AgentType
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from llm_client import *

prompt = PromptTemplate.from_template(
    "What is a good name for a company that makes {product}?"
)

output_parser = StrOutputParser()


def test_gpt():
    llm = gpt4()
    chain = llm | output_parser
    res = chain.invoke('hi')
    print(res)


def test_chain():
    llm = qwen72b_chat(temperature=0)
    chain = LLMChain(
        prompt=prompt,
        llm=llm,
        output_parser=output_parser,
    )

    res = chain.invoke({'product': 'socks'})
    print(res)


def test_agent():
    llm = qwen72b_chat(temperature=0, stop=None)
    tools = load_tools(["llm-math"], llm=llm)
    agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
    res = agent.run("2 raised to the 8 power?")
    print(res)


def test_conversation():
    from langchain.chains import ConversationChain
    llm = qwen72b(temperature=0, max_token=20)
    conversation = ConversationChain(llm=llm, verbose=True)
    output = conversation.predict(input="Hi there!")
    print(output)
    output = conversation.predict(input="enen!")
    print(output)


def test_chat():
    llm = qwen72b_chat(temperature=0)
    from langchain_core.prompts import ChatPromptTemplate
    messages = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant that translates English to Chinese."),
        ("user", "Translate this sentence from English to Chinese. I love programming.")
    ])
    chain = messages | llm
    res = chain.invoke({})
    res.pretty_print()


def test_python():
    from langchain_experimental.agents.agent_toolkits import create_python_agent
    llm = qwen72b(stop=None)
    from langchain_experimental.tools import PythonREPLTool
    agent = create_python_agent(
        llm=llm,
        tool=PythonREPLTool(),
        verbose=True
    )
    res = agent.invoke({'input': '把"abc"拆封成array'})
    print(res)


def custom_agent():
    from langchain.agents import Tool
    from langchain_core.prompts import PromptTemplate

    template = '''
Answer the following questions as best you can. You have access to the following tools:
You might know the answer without running any tools, but you should still run the tools to get the answer.
If it does not seem like you can write code to answer the question, just return "I don't know" as the answer.

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}'''

    prompt = PromptTemplate.from_template(template)

    def add(value: int):
        print("run add")
        return int(value) + 1

    tools = [
        Tool.from_function(add,
                           name='add',
                           description=(
                               "一个计算器工具，用于为给定的数字加1"
                               "输入是一个int类型的值"
                           ),
                           return_direct=False)
    ]

    from langchain.agents import create_react_agent, AgentExecutor
    llm = qwen72b()
    agent = create_react_agent(llm, tools, prompt)

    executor = AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=tools,
        verbose=True,
        stream_runnable=False,
    )

    res = executor.invoke({'input': '给2增加1'}, return_only_outputs=True)
    print(res)


if __name__ == '__main__':
    test_gpt()
