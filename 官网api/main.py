# 这是一个示例 Python 脚本。

# 按 ⌃R 执行或将其替换为您的代码。
# 按 Double ⇧ 在所有地方搜索类、文件、工具窗口、操作和设置。
from pyhanlp import *

# COARSE_ELECTRA_SMALL_ZH ：细分

# tok = hanlp.load(hanlp.pretrained.tok.LARGE_ALBERT_BASE)
# print(tok("一种新能源汽车使用的减震装置"))

HanLP.Config.ShowTermNature = True


# # 极速词典分词
# DAT_segment = HanLP.newSegment("dat")
# print(DAT_segment.seg("一种新能源汽车使用的减震装置"))
#
# # 维特比
# ViterbiNewSegment = HanLP.newSegment("viterbi")
# print(ViterbiNewSegment.seg("一种新能源汽车使用的减震装置"))

def get_entity(text: str):
    import requests
    
    url = "http://comdo.hanlp.com/hanlp/v21/dep/dep"
    
    payload = {}
    headers = {
        'token': '66f194ed12b446f8b1aef6824d5af8671643906145404token'
    }
    # text = '一种新能源汽车使用的减震装置'
    response = requests.request("POST", url, headers=headers, data=payload, params={"text": text, })
    
    return response.text


def get_text(path="../title_100.csv"):
    text_list = []
    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i == 0:
                continue
            text_list.append(line.strip())
    return text_list


if __name__ == '__main__':
    text_list = get_text()
    total_result = []
    for text in text_list:
        single_result = get_entity(text)
        single_result = eval(single_result.replace('null', 'None'))
        tok = single_result["data"]['tok/fine'][0]
        dep = single_result["data"]['dep'][0]
        assert len(tok) == len(dep)
        roots = []
        for j, k in enumerate(dep):
            if k[1] == 'root':
                roots.append(tok[j])
        total_result.append([text, roots])

    with open('result.txt', 'w') as f:
        for line in total_result:
            f.write(line[0] + ',' + ' '.join(line[1]) + '\n')