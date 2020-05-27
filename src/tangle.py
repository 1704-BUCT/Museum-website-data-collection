import math
print("请输入 a b c \n")
a,b,c=map(float,input ().split(' '))#以空格为间隔符
if(a+b <= c or a+c<=b or b+c<=a or abs(a-b) >=c or abs(a-c) >=b or abs(b-c) >= a):
    print("不是三角形\n")
else:
    #判断是否为等腰三角形
    if(a == b or a==c or b==c):
    #判断是否为等边三角形
        if(a==b and b==c):
            print("等边三角形\n")
        else:
            print("等腰三角形\n")
    else:
        print("一般三角形\n")
