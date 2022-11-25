import requests
import jieba
import json
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from os import path
import login


class bilibili(object):
    def __init__(self):
        self.session = login.To_login().try_to_login()

    def get_history_1(self, view_at=''):
        url = 'https://api.bilibili.com/x/web-interface/history/cursor?max=&view_at=' + str(view_at) + '&business='
        result = json.loads(self.session.get(url=url).text)
        print(result)
        history_title = result['data']['list']

        history_all = []

        user = self.get_user_name()

        for i in range(len(history_title)):
            history_all.append(history_title[i]['title'])
            if i == len(history_title) - 1:
                # print(history_title[i]['view_at'])
                return history_all, history_title[i]['view_at']

    def get_history_others(self):
        b = []
        view_at = self.get_history_1()[1]
        b.append(self.get_history_1()[0])
        n = 0
        while 1:
            try:
                history_all, view_at = self.get_history_1(view_at)
                b.append(history_all)
                print(view_at)
                n = n + 1
                if n == 999:
                    print(dsadsad)
            except:
                return b


class Word(object):
    def __init__(self, history_all=0):
        self.history_all = history_all

    def cut(self):
        accurate = jieba.cut(self.history_all)
        # 单个列表，分词后。多个句子会有多个列表，函数只能分一个句子。
        # ['asdada','basdsasdsa']
        return accurate

    def merge(self, history_list):
        z = []
        b = []
        for i in range(len(history_list)):
            z.append([a for a in Word(history_list[i]).cut()])
            for d in range(len(z[i])):
                b.append(z[i][d])
        return b

    def count(self, words_list):
        dict = {}  # 这里建一个列表用于记录列表中的所有唯一值出现的次数
        for key in words_list:
            dict[key] = dict.get(key, 0) + 1
        return dict

    def Delete_stop_Words(self, hist_dict):
        f_stop = open('cn_stopwords.txt', encoding='utf-8')  # 自己的中文停用词表
        sw = [line.strip() for line in f_stop]  # strip() 方法用于移除字符串头尾指定的字符（默认为空格）
        f_stop.close()

        del_word = sw
        list_1 = []
        list_2 = []
        for k, v in hist_dict.items():
            if k in del_word:
                pass
            else:
                list_1.append(k)
                list_2.append(v)
        return dict(zip(list_1, list_2))

    def generate_cloud(self, dict):
        d = path.dirname(__file__)
        backgroud_Image = np.array(Image.open(path.join(d, "bg.jpeg")))
        wc = WordCloud(
            background_color='white',  # 设置背景颜色，与图片的背景色相关
            font_path='/Users/hanyibo/Library/Fonts/HanaMinA.ttf',  # 显示中文，可以更换字体
            max_words=500,  # 设置最大显示的字数
            # width = 1280,
            # height = 960,
            mask=backgroud_Image,  # 设置背景图片
            max_font_size=150,  # 设置字体最大值
            random_state=1,  # 设置有多少种随机生成状态，即有多少种配色方案
            scale=1  # 设置生成的词云图的大小
        )
        # 传入需画词云图的文本
        wc.fit_words(dict)
        image_colors = ImageColorGenerator(backgroud_Image)
        plt.subplots(figsize=(12, 8), dpi=600)
        plt.imshow(wc.fit_words(dict))

        # 隐藏图像坐标轴
        plt.axis("off")
        # 展示图片
        plt.show()
