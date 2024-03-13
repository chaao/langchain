import json

import pandas as pd
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from llm_client import gpt4

system_pmt = '''
你是一名电商领域的智能客服，擅长结合历史对话分析用户的问题。
为了准确的回答用户的问题，需要分析当前问题属于哪个分类，现有分类及描述如下：
- 人工参与：不是在询问信息，而是需要人工客服参与做决策或执行某些action
- 问候语：比如 你好/在吗 等
- 肯定/否定语：无实际意义，只是对前序对话的赞同或者否认
- 咨询商品信息-安装：咨询如何安装，或者安装条件是否符合等等
- 咨询商品信息-使用：咨询商品的使用问题
- 咨询商品信息-质保：咨询商品保修，运费，退换策略等信息
- 咨询商品信息：咨询商品本身的参数配置等信息
- 咨询通用信息：全局商品，或者某一系列商品的知识，与特定商品无关
- 对比：询问两个商品的属性的区别，差异等
- 推荐：推荐一款商品
- 优惠/活动信息: 咨询优惠或者活动送赠品等等
- 售后-维修：已经购买商品，商品有问题，咨询如何维修
- 物流信息：已购买商品，询问物流状态

注意：凡事需要人工参与做决策或执行某些action的都属于'人工参与'，其他分类都是在查询信息

指输出上述类型，如果用户的问题不属于上述任何分类，请输出'其他'
'''

user_pmt = '''
历史对话:
```
{history}
```

用户问题: {query}
分类是:
'''

output_parser = StrOutputParser()

prompt = ChatPromptTemplate.from_messages([
    ("system", system_pmt),
    ("user", user_pmt),
])


def task(row):
    messages = json.loads(row['messages'])
    query = messages[-1]['content']
    print(f"{row.name} {query=}")
    if len(messages) == 1:
        history = '无'
    else:
        history = ''
        for i in messages[:-1]:
            role = '用户'
            if i['role'] != 'buyer':
                role = '客服'
            history += f'{role}: {i["content"]}\n'

    res = chain.invoke({"query": query, "history": history})
    print(f"{res=}")
    return pd.Series({
        "分类": res
    })


if __name__ == '__main__':
    llm = gpt4()
    chain = prompt | llm | output_parser

    df = pd.read_excel('可回or不可回_正式版.xlsx')
    # df = df.sample(100)
    df = df.iloc[[464]]
    new_df = df.apply(task, axis=1)
    df = pd.concat([df, new_df], axis=1)
    df.to_excel('output_file.xlsx', index=False)
