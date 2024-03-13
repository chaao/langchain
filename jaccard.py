def jaccard_similarity(str1, str2):
    set1 = set(str1)
    set2 = set(str2)
    intersection_set = set1.intersection(set2)
    # print(f"{set1=}")
    # print(f"{set2=}")
    # print(f"{intersection_set=}")
    # print(f"{len(intersection_set)=} {len(set1)=} {len(set2)=}")
    return 2 * len(intersection_set) / (len(set1) + len(set2))


text1 = "亲亲，我看到您希望3月1号再发货，我会帮您登记延迟到3月1号发货的请求。请您在1小时内点击我们推送的【协商发货】卡片，确认延迟时间并点击【同意】。如果没操作，系统会按原计划发货。如果有变动或需要拦截已发出的包裹，随时联系我们哦。"
text2 = "嗯嗯麻烦您点击下上面协商小卡片 点击同意呢 如果【没有点击！！！】的话，我们系统会按正常发货时间发哦。麻烦您哈 "

text1_words = set(text1)
text2_words = set(text2)

if __name__ == '__main__':
    similarity = jaccard_similarity(text1_words, text2_words)
    print("Jaccard 相似度:", similarity)
