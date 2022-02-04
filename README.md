## 解决方法
使用依存句法分析抽取出`root`实体，即为主体（产品）名称。

## 调用方式
三种调用方式来识别主体，结果都在文件夹下`result.txt`文件中。
1. 官网申请API直接调用（https://www.hanlp.com），对应`官网api`文件夹。
没有找到如何设置模型选项，这个应该是给公司使用的，

2. 使用hanlp轻量级版本`hanlp_restful`进行API调用，对应`hanlp_restful`文件夹。
`result_coarse.txt`对应粗粒度结果，`result_fine`对应细粒度结果。

3. 直接使用hanlp专业版搭建pipeline模型，对应`hanlp_pipeline`文件夹。
可以选择不同的语料模型，具体的应该可以选择使用的模型和对应的词典。
这个方法的具体使用见`hanlp_pipeline`文件夹下的`README.md`，结果只使用了一个demo得到结结果，具体可以尝试不同模型组装求最优。

从结果看，第二种方法效果最好，但是第二种方式好像不能设置使用的语料和模型。