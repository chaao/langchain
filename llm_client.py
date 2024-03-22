from dotenv import load_dotenv

default_stop = [
    "<|im_end|>",
    "</s>",
    "\n\n\n"
]


def gpt4(temperature=0, **kwargs):
    load_dotenv('env/azure.env', verbose=True)
    from langchain_openai import AzureChatOpenAI
    kwargs.setdefault('seed', 42)
    return AzureChatOpenAI(
        deployment_name="gpt-4",
        temperature=temperature,
        model_kwargs=kwargs
    )


def gpt3_5(temperature=0, **kwargs):
    load_dotenv('env/azure.env', verbose=True)
    from langchain_openai import AzureChatOpenAI
    kwargs.setdefault('seed', 42)
    return AzureChatOpenAI(
        deployment_name="gpt-35-turbo",
        temperature=temperature,
        model_kwargs=kwargs
    )


def qwen72b_chat(temperature=0, max_token=300, **kwargs):
    load_dotenv('env/qwen72b.env', verbose=True)
    from langchain_openai import ChatOpenAI
    kwargs.setdefault('seed', 42)
    return ChatOpenAI(
        model_name="qwen1.5-72b-chat-int4",
        max_tokens=max_token,
        temperature=temperature,
        model_kwargs=kwargs
    )


def qwen72b(temperature=0, max_token=300, **kwargs):
    load_dotenv('env/qwen72b.env', verbose=True)
    from langchain_openai import OpenAI
    kwargs.setdefault('seed', 42)
    return OpenAI(
        model_name="qwen1.5-72b-chat-int4",
        max_tokens=max_token,
        temperature=temperature,
        model_kwargs=kwargs
    )
