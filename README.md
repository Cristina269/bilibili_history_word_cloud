# 哔哩哔哩观看历史词云分析

## 功能
获取账号里的观看历史，使用`jieba`分词，`wordcloud`生成词云，使用`cn_stopwords`去除部分无意义的词。
## 说明
扫码登陆，获取观看历史的时间可能会比较长
## 使用帮助
安装必要的库`pip3 install -r requirements.txt`，运行`main.py`扫码登陆，等待读取结束。
## 效果 
![](2022-11-25 _ 16.35.53_预览.png)
## 感谢
1. 参考
https://blog.csdn.net/qq_18303993/article/details/114481841
进行扫码登陆
2. 参考https://zhuanlan.zhihu.com/p/64690193进行词云生成
3. 参考https://github.com/goto456/stopwords中文常用停用词表