
import os

dir1='val2017'#图片文件存放地址
txt1 = 'val2017.txt'#图片文件名存放txt文件地址
f1 = open(txt1,'a')#打开文件流
for filename in os.listdir(dir1):
    f1.write('data/val2017/'+filename)#只保存名字，去除后缀.jpg
    f1.write("\n")#换行
f1.close()#关闭文件流
