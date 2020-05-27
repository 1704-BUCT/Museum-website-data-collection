import os
libray_inf=[]
#数据的格式
def get_line(str1,str2):
    str1.replace('\\n','')
    str2.replace('\\n','')
    a={}
    a["name"]=str1
    a["provience"]=str2
    libray_inf.append(a)
#读文件表得到各个博物馆的名字信息
def get_information():
    filename="C:/Study/work/Museum-website-data-collection/src/1.txt"
    f = open(filename)
    str1=""
    str2=""
    for line in f:
        if line[0]=='#':
            str2=line[1:len(line)-1]
        else:
            str1=line[0:len(line)-1]
        if(str1!=''):
            get_line(str1,str2)
        # print(line)
    f.close()
def print_out():
    for i in libray_inf:
        print(i)
def mkdir(path):
    # 引入模块
    # 去除首位空格
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path) 
        print (path+' 创建成功')
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print (path+' 目录已存在')

# 定义要创建的目录
# 调用函数
def makefile():
    filepath="C:\\Study\\work\\Museum-website-data-collection\\images\\"
    for i in libray_inf:
        # print(i["name"])
        # mkdir(filepath+i["name"])
        mkdir(filepath+i["name"]+"\\展览")
        mkdir(filepath+i["name"]+"\\藏品")
        mkdir(filepath+i["name"]+"\\教育活动")
get_information()
#print_out()
makefile()