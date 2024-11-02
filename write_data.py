import json
data = {"语文":{"金牌学典":{"课文":{"name":"金牌学典 - 课文","date":"2024-11-2","dir":"data/chinese/0/"},"周测小卷":{"name":"金牌学典 - 周测小卷","date":"2024-11-2","dir":"data/chinese/1/"},"练习卷":{"name":"金牌学典 - 练习卷","date":"2024-11-2","dir":"data/chinese/2/"}}},"数学":{"学考精练":{".":{"name":"学考精练","date":"2024-11-2","dir":"data/math/0/"}}},"历史":{"金牌学典":{"课后精练":{"name":"金牌学典 - 课后精练","date":"2024-11-2","dir":"data/history/0/"},"试卷":{"name":"金牌学典 - 试卷","date":"2024-11-2","dir":"data/history/1/"}}}}
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)