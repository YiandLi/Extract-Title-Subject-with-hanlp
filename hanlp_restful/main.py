from hanlp_restful import HanLPClient


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
    
    # 设置参数部分
    api = None  # 公益API，不实用则每分钟2次
    if_coarse = False  # 是否粗分
    
    # 设置CLient，是否使用公益api
    HanLP = HanLPClient('https://www.hanlp.com/api', auth=None, language='zh')
    
    if if_coarse:
        # skip参数使用粗分
        # print(HanLP(text_list, skip_tasks='tok/fine', tasks=['tok/coarse', 'dep']).pretty_print())
        api_result = HanLP(text_list, skip_tasks='tok/fine', tasks=['tok/coarse', 'dep'])
        out_path = "result_coarse.txt"
    else:
        api_result = HanLP(text_list, tasks=['tok/fine', 'dep'])
        out_path = "result_fine.txt"
    
    toks = api_result["tok/coarse" if if_coarse else "tok/fine"]
    deps = api_result["dep"]
    result_pairs = []
    
    for i in range(len(toks)):
        tok = toks[i]
        dep = deps[i]
        roots = []
        for index, j in enumerate(dep):
            if j[1] == 'root':
                roots.append(tok[index])
        result_pairs.append([text_list[i], ' '.join(roots)])
    
    with open(out_path, 'w') as f:
        for line in result_pairs:
            f.write(line[0] + ',' + line[1] + '\n')
