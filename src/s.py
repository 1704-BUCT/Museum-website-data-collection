import MySQLdb
import pymysql
alllo=[]
class ConnMysql(object):
    def __init__(self):
        # 连接数据库
        self.db = pymysql.connect(host='39.97.241.101',
                                  port=3306,
                                  database='testsitedb',
                                  user='root',
                                  password='root',
                                  charset='utf8')
        self.cursor = self.db.cursor()
    def update(self,dict1):
        sql_2 = "update museums set lng=%s,lat=%s where name=%s"
        for i in dict1:
            data_2 = [i["jin"],i["wei"],i['name']]
            try:
                self.cursor.execute(sql_2,data_2)
                self.db.commit() # 提交操作
            except:
                self.db.rollback()
        self.db.close()
def save_data(dict_data):
    # 存数据库
    database = ConnMysql()
    database.update(dict_data)
    #数据更新
   
def getinfo():
    f = open("2.txt")             # 返回一个文件对象
    line = f.readline()             # 调用文件的 readline()方法
    while line:
        a={}
        s=line.split( )
        a['name']=s[0]
        a['jin']=s[3]
        a['wei']=s[4]
        alllo.append(a)
        print (a)               # 后面跟 ',' 将忽略换行符
    # print(line, end = '')　　　# 在 Python 3中使用
        line = f.readline()
    f.close()
    save_data(alllo)
getinfo()