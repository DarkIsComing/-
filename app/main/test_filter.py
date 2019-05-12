# def filter_name(*args, **kwargs):
#     word_list=list(args)+list(kwargs.values())
#     for i,word in enumerate(word_list):
#         print('{}'.format(str(i+1)),type('{}'.format(str(i+1))))
#         print('word'+str(i))
#         # 'word'+str(i+1)=word
#         #word{}.format(str(i+1))=word
    
#     # for i in range(4):
#     #     print(word{}.format(str(i)))

#     # print(args,type(args))
#     # print(kwargs,type(kwargs))
#     # print(args[0])
#     # print(word_list)

# filter_name(1,2,a=3,b=4)

# createVar = locals()
# listTemp = [1,2,3,4]
# for i,s in enumerate(listTemp):
#     createVar['a'+str(i+1)] = s

# # print(createVar,type(createVar))
# # print(a1,a2,a3,a4)

# words={'a':1,'b':2}
# #words=[1,2]
# word='a'
# print(word if word in words else 'c')
    # print(word)
# for i,s in enumerate(listTemp):
#     word['words_{}'.format(i)] = s
#print(word)
#print(next(word,0))
#a=0
# z=[a+i for i in listTemp]
# print(z,type(z))
# while True:
#     print(next(z,1))
#print(next(listTemp))
# print(next(a for a in listTemp) if next(listTemp) is not None)

# print(word if word in words)
# import os
# print(os.path.dirname('static'))
# UPLOAD_FOLDER='/Users/zhaotengwei/Desktop/ERP/app/static'

# ids=['id=0805', 'id=1206', 'id=0603-ARC', 'id=FIDUCIAL_1MM', 'id=SSOP28DB', 'id=TQFP100', 'id=CRYSTAL-3.2-2.5', 'id=SOT-23', 'id=SOT223', 'id=SOT323-5L', 'id=DIO4148-0805']
# for i,item in enumerate(ids):
#     ids[i]=ids[i][3:]
# print(ids)
# # s='id=0805'
# # print(s[3:])
# # s=s[3:]
# # print(s)

# fz=['0805', '1206', '0603-ARC', 'FIDUCIAL_1MM', 'SOT-23', 'SSOP28DB', 'TQFP100', 'SOT223', 'DIO4148-0805', 'SOT323-5L', 'CRYSTAL-3.2-2.5']
# num=['25', '13', '3', '2', '1', '1', '1', '1', '1', '1', '1']
# print(zip(fz,num))
# for i, j in zip(fz,num):
#     print(i,j)

# import pandas as pd

# #任意的多组列表
# a = [1,2,3]
# b = [4,5,6]    

# #字典中的key值即为csv中列名
# dataframe = pd.DataFrame({'a_name':a,'b_name':b})

# #将DataFrame存储为csv,index表示是否显示行名，default=True
# dataframe.to_csv("test.csv",index=False,sep=',')
# s='shouchiji.mnt'
# print(s.split('.')[0])


# import os

# fname=[]
# path = "/Users/zhaotengwei/Desktop/ERP/app/static/csv" #文件夹目录
# files= os.listdir(path) #得到文件夹下的所有文件名称
# for file in files:
#     fname.append(file)
# print(files)
# print(fname)
# for fpath, dirname, fnames in os.walk(path):
#     print('路径：',fpath,type(fpath))
#     print('文件夹名',dirname,type(dirname))
#     print('文件名：',fnames,type(fnames))
# s = []
# for file in files: #遍历文件夹
#      if not os.path.isdir(file): #判断是否是文件夹，不是文件夹才打开
#           f = open(path+"/"+file); #打开文件
#           iter_f = iter(f); #创建迭代器
#           str = ""
#           for line in iter_f: #遍历文件，一行行遍历，读取文本
#               str = str + line
#           s.append(str) #每个文件的文本存到list中
# print(s) #打印结果

# a=(None,)
# b=a is None
# print(a[0])

import pandas as pd
import numpy as np

dict_obj = {'key1' : ['a', 'b', 'a', 'b', 
                      'a', 'b', 'a', 'a'],
            'key2' : ['one', 'one', 'two', 'three',
                      'two', 'two', 'one', 'three'],
            'key3':[1,2,3,4,5,6,7,8]}
df_obj = pd.DataFrame(dict_obj)
print(df_obj)
# grouped2 = df_obj['data1'].groupby(df_obj['key1'])
# print(grouped2.count())

# grouped1 = df_obj.groupby('key1')
# print(grouped1.count())

# self_def_key = [0, 1, 2, 3, 3, 4, 5, 7]
# print(df_obj.groupby(self_def_key).size())

# 按自定义key分组，多层列表
df=df_obj.groupby([df_obj['key1'], df_obj['key2']]).size()
print(df)
new_df=df.reset_index(name='counts')
print(new_df)
print(new_df['key1'].values)
# for (k1, k2), group in df_obj.groupby([df_obj['key1'],df_obj['key2']]):
#     print(k1, k2)
#     print('------')
#     print(group)
# # 按多个列多层分组
# grouped2 = df_obj.groupby(['key1', 'key2'])
# print(grouped2.size())

# # 多层分组按key的顺序进行
# grouped3 = df_obj.groupby(['key2', 'key1'])
# print(grouped3.mean())
# # unstack可以将多层索引的结果转换成单层的dataframe
# print(grouped3.mean().unstack())

