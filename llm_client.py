from dotenv import load_dotenv


def gpt4():
    load_dotenv('env/azure.env', verbose=True)
    from langchain_openai import AzureChatOpenAI
    return AzureChatOpenAI(
        deployment_name="gpt-4",
        temperature=0,
        model_kwargs={
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
            'stop': [
                "<|im_end|>",
                "</s>",
                "\n\n\n"
            ]
        }
    )


def qiwen():
    pass
