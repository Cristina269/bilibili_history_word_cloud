import api

user = api.bilibili()

# 获取历史
history_list = user.get_history_others()

# 合并histort_list
a=[]
for i in range(len(history_list)):
    for u in range(len(history_list[i])):
        a.append(history_list[i][u])
history_list = a
b = api.Word.merge(history_list, history_list)

# 统计词频
hist_dict = api.Word.count(b, b)

# 删除不常用的词
hist_dict_del = api.Word.Delete_stop_Words(hist_dict,hist_dict)

# 画图
api.Word.generate_cloud(hist_dict_del,hist_dict_del)

print(hist_dict_del)
