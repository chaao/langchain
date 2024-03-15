from dotenv import load_dotenv


def gpt4():
    load_dotenv('env/azure.env', verbose=True)
    from langchain_openai import AzureChatOpenAI
    return AzureChatOpenAI(
        deployment_name="gpt-4",
        temperature=0,
        model_kwargs={
            'seed': 42,
            'stop': [
                "<|im_end|>",
                "</s>",
                "\n\n\n"
            ]
        }
    )


def gpt3_5():
    load_dotenv('env/azure.env', verbose=True)
    from langchain_openai import AzureChatOpenAI
    return AzureChatOpenAI(
        deployment_name="gpt-35-turbo",
        temperature=0,
        model_kwargs={
            'seed': 42,
            'stop': [
                "<|im_end|>",
                "</s>",
                "\n\n\n"
            ]
        }
    )


def qwen72b():
    load_dotenv('env/qwen72b.env', verbose=True)
    from langchain_openai import ChatOpenAI
    return ChatOpenAI(
        model_name="qwen1.5-72b-chat-int4",
        max_tokens=300,
        temperature=0,
        model_kwargs={
            'seed': 42,
            'stop': [
                "<|im_end|>",
                "</s>",
                "\n\n\n"
            ]
        }
    )
