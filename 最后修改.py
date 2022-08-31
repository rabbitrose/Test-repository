import os
import math
class User(object):
    def __init__(self, data):
        self.data = data
        self.number = data[0]
        self.user_data = data[1]
        self.friends = {}
        self.friends_number = 0


all_user = []
contents = []  # 存放txt文件每行的内容

def user_data_processing(path):
    files = os.listdir(path)  # 得到path1文件夹下所有文件的名称
    files.sort(key=lambda x: int(x[:-4]))
    data_number = -1 # 创造用户数据编号 确保索引便利
    for file in files:  # 遍历文件夹
        if not os.path.isdir(file):  # 判断是否是文件夹，不是文件夹才打开
            f = open(path + "/" + file, 'r', encoding='utf-8')  # 打开文件
            iter_f = iter(f)  # 创建迭代器
            string = ""
            for line in iter_f:  # 遍历文件，一行行遍历，读取文本
                string = string + line
            number = -1
            for j in string:
                number += 1
                if (string[number] == '学' and string[number - 1] == '大') or (string[number] == '学' and string[number + 1] == '院') or (string[number] == '学' and string[number + 1] == '校'):
                    try:
                        b = (str.replace(string[:number], ' ', '') + string[number:])
                    except:
                        pass
                    data_number += 1
                    user = User((data_number, b))
                    all_user.append(user)
                    break
            else:
                data_number += 1
                user = User((data_number, string))
                all_user.append(user)
                continue

def create_connection(file):
    for i in file:
        d = i.split('::')
        d.pop()
        all_user[int(d[0])].friends.setdefault(('number' + d[1]), int(d[2]))
        all_user[int(d[0])].friends_number += 1
        all_user[int(d[1])].friends.setdefault(('number' + d[0]), int(d[2]))
        all_user[int(d[1])].friends_number += 1



'''推荐关联度最高'''
'''新用户推荐'''
x=0
number=3
def recommand(list):
    x = 0
    number = 3
    for t in range(x, number):  # 推荐number数量个
        print('为您推荐用户：', list[t][0])
    x+=number
    number+=number
    while True:
        feedback = input("请为该推荐打分(good/bad)：")
        if feedback!="good":
            for t in range(x, number):  # 推荐number数量个
                print('为您推荐用户：', list[t][0])
            x += number
            number += number
        else:
            return False

def re(list):
    x = 0
    number = 3
    for t in range(x, number):  # 推荐number数量个
        print('为您推荐用户：', list[t][0])
    x += number
    number += number


def find_friends1(new_user_id):
    connection = {}
    for i in all_user:
        numbers1 = 0#关联度
        for j in new_user_id:
            if j in i.user_data:
                numbers1 += (1/len(new_user_id))
        connection[i.number] = numbers1
    connection = sorted(connection.items(), key=lambda x: (x[1], all_user[x[0]].friends_number), reverse=True) #key使用lambda匿名函数取value进行排序
    recommand(connection)
    pass

'''老用户推荐'''
def find_friends2(new_user_id1,number):#这个new——userid代表属性
    connection = {}
    topk = []
    for i in all_user:
        numbers1 = 0
        for j in new_user_id1:
            if j in i.user_data:
                numbers1 += (1/(len(new_user_id1.split(" "))-1))
        connection[i.number] = numbers1
    connection = sorted(connection.items(), key=lambda x: (x[1], all_user[x[0]].friends_number), reverse=True) #key使用lambda匿名函数取value进行排序
    for t in range(1,number+1):#推荐number数量个
        print('为您推荐用户：', connection[t][0])
        topk.append(connection[t][0])
    print("---------------------")
    return topk

'''为已有用户推荐列表'''
def recommand1(id):
    for i in all_user:
        if i.data[0]==id:
            print(i.data[1])
            find_friends2(i.data[1],5)
            print(i.friends)


def HRk(k):
   list=["_" for i in range(0,len(all_user))]
   for id in range(0,len(all_user)):#每一个用户的id
       print(id)
       iui = []
       '''找到当前用户'''

       for i in all_user:
            if i.data[0] == id:#id为用户ui的id
                topk=find_friends2(i.user_data,k)#可以构造出topk的列表，即为aui

                for t in i.friends:
                    if t[6:] not in iui:
                        iui.append(int(t[6:]))#构造iui列表

       if  len([v for v in iui if v in topk])!=0:
            list[id]=1
       else:
            list[id]=0
   print(list)
   num1=0
   for i in list:
       if i==1:
           num1+=1
       else:
           continue
   HRK=num1/len(all_user)
   print("HRK-20"
         "",HRK)


def DCGK(k):
    sumDCG=[]
    sumIDCG=[]
    list1 = []#用来存储所有topk与iui交集为1的用户id
    list2 = []#用来存储所有topk与iui交集为0的用户id
    for id in range(0, len(all_user)):  # 每一个用户的id
        print(id)
        iui = []
        '''找到当前用户'''    
        for i in all_user:
            if i.data[0] == id:  # id为用户ui的id
                topk = find_friends2(i.user_data, k)  # 可以构造出topk的列表，即为aui
                for t in i.friends:
                    if t[6:] not in iui:
                        iui.append(int(t[6:]))  # 构造iui列表
        if len([v for v in iui if v in topk]) != 0:
            list1.append(id)
        else:
            list2.append(id)
    print("////////////////////////////////")
    print("list1",list1)
    print("list2",list2)
    print("////////////////////////////////")
        #------------------------------------------------------
    for ui in list1:
        '''找回该项目的topk 和iui'''
        for i in all_user:
            if i.data[0] == ui:  # id为用户ui的id
                topk = find_friends2(i.user_data, k)  # 可以构造出topk的列表，即为aui
                for t in i.friends:
                    if t[6:] not in iui:
                        iui.append(int(t[6:]))  # 构造iui列表
    '''计算每个用户的DCG和IDCG'''
    sumlist1=["_" for i in range(0,len(topk))]
    sumlist2 = ["_" for i in range(0, len(topk))]
    for index in range(0,len(topk)):
        if topk[index] in iui and math.log(1+index)!=0:
            sumlist1[index]=1/math.log(1+index)#不写底数默认为ln(x)
            sumlist2[index]=(2**1-1)/math.log(1+index)
        else:
            sumlist1[index]=0
            sumlist2[index]=0
    x=sum(sumlist1)
    y=sum(sumlist2)
    sumDCG.append(x)
    sumIDCG.append(y)
    final_sum=0
    for t in range(0,len(sumDCG)):
        if sumIDCG[t]!=0:
            item=sumDCG[t]/sumIDCG[t]
            final_sum+=item
        else:
            continue
    ndcgk=final_sum/len(all_user)
    print("*********")
    print("NDCGK-20",ndcgk)
    print("*********")
        #--------------计算IDCG-----------------------------------
def main(k):
    print('输入out推出此程序 输入new添加新用户 输入recommand为已有用户推荐列表')
    while True:
        user_input = input('请输入命令')
        if user_input == 'out':
            print('程序已退出')
            break
        elif user_input == 'new':
            while True:
                try:
                    personal_data = str(input('输入你的信息, 用空格分割：'))
                    print(personal_data)
                    if personal_data == 'out':
                        break
                    else:
                        find_friends1(personal_data.split())
                    break
                except:
                    print('用户信息输入有误，try again')
        elif user_input=="recommand":
            while True:
                try:
                    personal_data = int(input('输入已知用户id：'))
                    print("你输入的用户id为：",personal_data)
                    find_friends2(all_user[personal_data].user_data, k)#这里面可以得到topk推荐列表
                    if personal_data == 'out':
                        break
                    break
                except:
                    print('用户信息输入有误，try again')

        else:
            print('无法识别命令')
            pass

user_data_processing(r"C:\Users\l\Desktop\我的科研\好友交互推荐\SCHOLAT Interactive User Recommendation\user_attribute")
create_connection(open(r"C:\Users\l\Desktop\我的科研\好友交互推荐\SCHOLAT Interactive User Recommendation\user_interactions.txt", 'r'))
#for i in all_user:
#    print(i.data)
main(6)
#DCG(10)
#DCG(15)
#DCG(5)




#HRk(5）





# import os
# class User(object):
#     def __init__(self, data):
#         self.data = data
#         self.number = data[0]
#         self.user_data = data[1]
#         self.friends = {}
#         self.friends_number = 0
#         self.may_connect = {}
#
# all_user = []
# data_number = 0
# contents = []  # 存放txt文件每行的内容
# path1 = r"C:\Users\94531\Desktop\SCHOLAT Interactive User Recommendation\user_attribute"
# files_1 = os.listdir(path1)  # 得到path1文件夹下所有文件的名称
# for file in files_1:
#     path2 = path1 + "\\" + file
#     with open(path2, 'r', encoding='utf-8') as f:
#         contents = f.readlines()
#         first_number = 0
#         number = -1
#         for j in contents[0]:
#             number += 1
#             if (contents[0][number] == '学' and contents[0][number - 1] == '大') or (contents[0][number] == '学' and contents[0][number + 1] == '院') or (contents[0][number] == '学' and contents[0][number + 1] == '校'):
#                 b = (str.replace(contents[0][:number], ' ', '') + contents[0][number:])
#                 b = b.split(' ')
#                 b.pop()
#                 data_number += 1
#                 user = User((data_number, b))
#                 all_user.append(user)
#
# file1 = open(r'C:\Users\94531\Desktop\SCHOLAT Interactive User Recommendation\user_interactions.txt', 'r')
# for i in file1:
#     d = i.split('::')
#     d.pop()
#     all_user[int(d[0])].friends.setdefault(('number' + d[1]), int(d[2]))
#     all_user[int(d[0])].friends_number += 1
#     all_user[int(d[1])].friends.setdefault(('number' + d[0]), int(d[2]))
#     all_user[int(d[1])].friends_number += 1
#
#
#
# for i in all_user:
#     print(i.number)
#     print(i.user_data)
#     print(i.friends_number)
#     print(i.friends)
#     print()
#
#
#
#
# import os
# class User(object):
#     def __init__(self, data):
#         self.data = data
#         self.number = data[0]
#         self.user_data = data[1]
#         self.friends = {}
#         self.friends_number = 0
#         self.may_connect = {}
#
# all_user = []
# contents = []  # 存放txt文件每行的内容
#
# def user_data_processing(path):
#     files = os.listdir(path)  # 得到path1文件夹下所有文件的名称
#     data_number = 0 # 创造用户数据编号 确保索引便利
#     for file in files:
#         path2 = path + "\\" + file
#         with open(path2, 'r', encoding='utf-8') as f:
#             contents = f.readlines()
#             number = -1
#             for j in contents[0]:
#                 number += 1
#                 if (contents[0][number] == '学' and contents[0][number - 1] == '大') or (contents[0][number] == '学' and contents[0][number + 1] == '院') or (contents[0][number] == '学' and contents[0][number + 1] == '校'):
#                     b = (str.replace(contents[0][:number], ' ', '') + contents[0][number:])
#                     b = b.split(' ')
#                     b.pop()
#                     data_number += 1
#                     user = User((data_number, b))
#                     all_user.append(user)
#
# def create_connection(file):
#     for i in file:
#         d = i.split('::')
#         d.pop()
#         all_user[int(d[0])].friends.setdefault(('number' + d[1]), int(d[2]))
#         all_user[int(d[0])].friends_number += 1
#         all_user[int(d[1])].friends.setdefault(('number' + d[0]), int(d[2]))
#         all_user[int(d[1])].friends_number += 1
#
# user_data_processing(r"C:\Users\94531\Desktop\SCHOLAT Interactive User Recommendation\user_attribute")
# create_connection(open(r'C:\Users\94531\Desktop\SCHOLAT Interactive User Recommendation\user_interactions.txt', 'r'))
#
# for i in all_user:
#     print(i.number)
#     print(i.user_data)
#     print(i.friends_number)
#     print(i.friends)
#     print()








#
# class User(object):
#     def __init__(self, data):
#         self.data = data
#         self.number = data[0]
#         self.user_data = data[1]
#         self.friends = {}
#         self.friends_number = 0
#         self.may_connect = {}
#
# import os
# all_user = []
# number = 0
# contents = []  # 存放txt文件每行的内容
# path1 = r"C:\Users\94531\Desktop\SCHOLAT Interactive User Recommendation\user_attribute"
# files_1 = os.listdir(path1)  # 得到path1文件夹下所有文件的名称
# for file in files_1:
#     path2 = path1 + "\\" + file
#     with open(path2, 'r', encoding='utf-8') as f:
#         contents = f.readlines()
#         a = str.replace(contents[0], ' ', '')
#         b = (number, a)
#         number += 1
#         user = User(b)
#         all_user.append(user)
#
# # all_connect = []
# file1 = open(r'C:\Users\94531\Desktop\SCHOLAT Interactive User Recommendation\user_interactions.txt', 'r')
# for i in file1:
#     d = i.split('::')
#     d.pop()
#
#     all_user[int(d[0])].friends.setdefault(('number' + d[1]), int(d[2]))
#     all_user[int(d[0])].friends_number += 1
#     all_user[int(d[1])].friends.setdefault(('number' + d[0]), int(d[2]))
#     all_user[int(d[1])].friends_number += 1
#
# # print(all_user[2].friends)
# # print(all_connect)
#
# for i in all_user:
#     for j in all_user:
#         if j.user_data != i.user_data and len(j.user_data) < len(i.user_data):
#             pass
#
