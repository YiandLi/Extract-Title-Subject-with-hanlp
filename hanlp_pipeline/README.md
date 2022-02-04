## 思路
多任务精度不佳，所以使用pipeline流水线拼接单任务模型，使用`input_key`指定输入。
单任务依存句法分析模型的输入必须为已分词已词性标注的一个或多个句子，所以使用单任务模型进行拼接：分词模型+词性标注模型+依存句法模型
>疑问：不同模型的词典不同，如何实现？

## 模型选择
- 不同的分词语料模型
{'COARSE_ELECTRA_SMALL_ZH': 'https://file.hankcs.com/hanlp/tok/coarse_electra_small_zh_20210603_112321.zip',
 'CTB6_CONVSEG': 'https://file.hankcs.com/hanlp/tok/ctb6_convseg_nowe_nocrf_20200110_004046.zip',
 'LARGE_ALBERT_BASE': 'https://file.hankcs.com/hanlp/tok/large_corpus_cws_albert_base_20211228_160926.zip',
 'PKU_NAME_MERGED_SIX_MONTHS_CONVSEG': 'https://file.hankcs.com/hanlp/tok/pku98_6m_conv_ngram_20200110_134736.zip',
 'SIGHAN2005_MSR_CONVSEG': 'https://file.hankcs.com/hanlp/tok/convseg-msr-nocrf-noembed_20200110_153524.zip',
 'SIGHAN2005_PKU_BERT_BASE_ZH': 'https://file.hankcs.com/hanlp/tok/sighan2005_pku_bert_base_zh_20201231_141130.zip',
 'SIGHAN2005_PKU_CONVSEG': 'https://file.hankcs.com/hanlp/tok/sighan2005-pku-convseg_20200110_153722.zip'}

- 不同的词性标注语料模型
{'C863_POS_ELECTRA_SMALL': 'https://file.hankcs.com/hanlp/pos/pos_863_electra_small_20210808_124848.zip',
 'CTB5_POS_RNN': 'https://file.hankcs.com/hanlp/pos/ctb5_pos_rnn_20200113_235925.zip',
 'CTB5_POS_RNN_FASTTEXT_ZH': 'https://file.hankcs.com/hanlp/pos/ctb5_pos_rnn_fasttext_20191230_202639.zip',
 'CTB9_POS_ALBERT_BASE': 'https://file.hankcs.com/hanlp/pos/ctb9_albert_base_20211228_163935.zip',
 'CTB9_POS_ELECTRA_SMALL': 'https://file.hankcs.com/hanlp/pos/ctb9_pos_electra_small_20220118_164341.zip',
 'CTB9_POS_ELECTRA_SMALL_TF': 'https://file.hankcs.com/hanlp/pos/pos_ctb_electra_small_20211227_121341.zip',
 'PKU98_POS_ELECTRA_SMALL': 'https://file.hankcs.com/hanlp/pos/pos_pku_electra_small_20210808_125158.zip',
 'PTB_POS_RNN_FASTTEXT_EN': 'https://file.hankcs.com/hanlp/pos/ptb_pos_rnn_fasttext_20200103_145337.zip'}

- 不同的依存句法语料模型
{'CTB5_BIAFFINE_DEP_ZH': 'https://file.hankcs.com/hanlp/dep/biaffine_ctb5_20191229_025833.zip',
 'CTB7_BIAFFINE_DEP_ZH': 'https://file.hankcs.com/hanlp/dep/biaffine_ctb7_20200109_022431.zip',
 'PTB_BIAFFINE_DEP_EN': 'https://file.hankcs.com/hanlp/dep/ptb_dep_biaffine_20200101_174624.zip'}

## 报错和解法
- 报错
直接拼接三个模型
```
HanLP = hanlp.pipeline() \
    .append(hanlp.load('COARSE_ELECTRA_SMALL_ZH'), output_key='tok') \
    .append(hanlp.load('CTB9_POS_ELECTRA_SMALL'), output_key='pos', input_key='tok') \
    .append(hanlp.load('CTB5_BIAFFINE_DEP_ZH'), output_key='dep', input_key='pos')
```
会报错，应该是输出格式不兼容，tok到pos可以正常拼接运行，但是pos到dep则报错。

- 因为：
pos输出为
```
"pos": [
    "NR",
    "NN",
    "VV",
    "NR",
    "NR",
    "VV",
    "NN",
    "PU"
  ]
```
但是dep输入应该为 
```
tree = dep([('蜡烛', 'NN'), ('两', 'CD'), ('头', 'NN'), ('烧', 'VV')])
```

- 解决：
所以使用 pipline(tok,pos) + zip + dep

## 结果
分词中的`COARSE_ELECTRA_SMALL_ZH`预料，应该对应着粗分，但是从实验来看，粒度仍然较细。