import json

import pandas as pd
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from consts import *
from llm_client import *

system_pmt = '''
你是一名电商领域的智能客服，擅长结合历史对话分析用户的问题。
为了准确的回答用户的问题，需要分析当前问题属于哪个分类，现有分类及描述如下：
- 问候语：比如 你好/在吗 等
- 肯定/否定语：无实际意义，只是对前序对话的赞同或者否认
- 表情/符号：
- 商品安装：咨询如何安装，或者安装条件是否符合等等
- 商品使用：咨询如何使用商品，或者使用中遇到的问题
- 商品质保：咨询商品或者其部件的保修时长，试用运费，退换策略等信息
- 商品属性：咨询商品本身的参数配置等信息
- 通用知识：咨询无关特定商品或者某一系列商品的知识
- 对比：询问两个商品的属性的区别，差异等
- 推荐：请求客服推荐一款商品或者给出选择建议
- 优惠/活动信息: 咨询优惠或者活动送赠品等等
- 售后维修：已经购买商品，咨询如何维修，或者预约维修
- 发货信息：咨询购买后发货时间或者能否发货到指定地区
- 人工：要求人工接待，或者要求客服做一些事情，比如备注

输出格式：请分析用户问题属于哪个分类，只输出上述分类，如不属于上述任何分类，请输出'其他'
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
    print(f"{row.name} {res=} {query=}")
    return pd.Series({
        "gpt4": res
    })


if __name__ == '__main__':
    llm = qwen72b()
    chain = prompt | llm | output_parser
    df = pd.read_excel(resource('可回or不可回_正式版.xlsx'))
    # df = df.sample(100)
    # df = df.iloc[[464]]
    new_df = df.apply(task, axis=1)
    df = pd.concat([df, new_df], axis=1)
    df.to_excel(output('output_file.xlsx'), index=False)
