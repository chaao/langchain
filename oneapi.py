import json

import pandas as pd
from langchain_core.output_parsers import StrOutputParser

from consts import *
from llm_client import *


def parse_prompt(row):
    # 获取需要的字段
    prompt = json.loads(row['prompt'])

    messages = []
    for item in prompt:
        messages.append(
            {
                'role': str.lower(item['obj']),
                'content': item['value'],
            }
        )
    return messages


def task(row):
    messages = parse_prompt(row)
    query = row['query']
    new_reply = chain.invoke(messages)
    try:
        new_reply = json.loads(new_reply)['response']
    except:
        pass
    print(f"{row.name} {query=} {new_reply=} ")
    return pd.Series({
        "new_reply": new_reply
    })


if __name__ == '__main__':
    llm = qwen72b()
    output_parser = StrOutputParser()

    chain = llm | output_parser
    df = pd.read_excel(resource('检索为空.xlsx'))
    # df = df.sample(100)
    # df = df.iloc[[1]]
    new_df = df.apply(task, axis=1)
    df = pd.concat([df, new_df], axis=1)
    df.to_excel(output('output_file.xlsx'), index=False)
