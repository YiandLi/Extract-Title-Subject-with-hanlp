import hanlp


def get_text(path="../title_100.csv"):
    text_list = []
    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i == 0:
                continue
            text_list.append(line.strip())
    return text_list


if __name__ == '__main__':
    # 定义模型
    # tok = hanlp.load(hanlp.pretrained.tok.COARSE_ELECTRA_SMALL_ZH)
    # pos = hanlp.load(hanlp.pretrained.pos.CTB9_POS_ELECTRA_SMALL)
    dep = hanlp.load(hanlp.pretrained.dep.CTB5_BIAFFINE_DEP_ZH)
    
    HanLP = hanlp.pipeline() \
        .append(hanlp.load('COARSE_ELECTRA_SMALL_ZH'), output_key='tok') \
        .append(hanlp.load('CTB9_POS_ELECTRA_SMALL'), output_key='pos', input_key='tok')
    
    texts = get_text()
    result_pairs = []
    for text in texts:
        result = HanLP(text)
        dep_input = list(zip(result['tok'], result['pos']))
        # 返回为CoNLLSentence类型
        result = list(dep(dep_input))
        roots = []
        for i in result:
            if i['deprel'].lower() == 'root':
                roots.append(i['form'])
        result_pairs.append([text, ' '.join(roots)])

    out_path = "result.txt"
    with open(out_path, 'w') as f:
        for line in result_pairs:
            f.write(line[0] + ',' + line[1] + '\n')
