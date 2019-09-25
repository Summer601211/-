# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 09:03:39 2019

@author: Administrator
"""

#项目13：社会财富分配问题模拟
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from bokeh.plotting import figure,show,output_file
import warnings
warnings.filterwarnings('ignore')
import os
import time
plt.rcParams['font.sans-serif']=['SimHei']  # 用来正常显示中文标签  
plt.rcParams['axes.unicode_minus']=False  # 用来正常显示负号
os.chdir('F:\\学习新玩意儿\\python\\作业完成\\项目13')
#(1)第一轮游戏分配模拟
#不考虑财富值为0的情况
person_n=[x for x in range(1,101)]
#person_y=list(range(1,101)) 等同于上一行代码
fortune=pd.DataFrame([100 for i in range(100)],index=person_n)
fortune.index.name='id'
#设置基本参数
round_r1=pd.DataFrame({'pre_round':fortune[0],'lost':1})
choice_r1=pd.Series(np.random.choice(person_n,100))#模拟每个人把钱给了谁
gain_r1=pd.DataFrame({'gain':choice_r1.value_counts()})#数据汇总多少个人得到了多少钱
round_r1=round_r1.join(gain_r1)
round_r1.fillna(0,inplace=True)
fortune[1]=round_r1['pre_round']-round_r1['lost']+round_r1['gain']
#(2)第一轮游戏分配模拟
#考虑财富值为0不分配财富值
person_n=[x for x in range(1,101)]
#person_y=list(range(1,101)) 等同于上一行代码
fortune=pd.DataFrame([100 for i in range(100)],index=person_n)
fortune.index.name='id'
#设置基本参数
round_r1=pd.DataFrame({'pre_round':fortune[0],'lost':0})#lost为0
#--设定筛选条件，使得财富值大于0的玩家才可以给出1块钱
round_r1['lost'][round_r1['pre_round']>0]=1
#--筛选出此轮的玩家
round_players=round_r1[round_r1['pre_round']>0]
#--模拟每个人把钱给了谁
choice_r1=pd.Series(np.random.choice(person_n,len(round_players)))
#--数据汇总多少个人得到了多少钱
gain_r1=pd.DataFrame({'gain':choice_r1.value_counts()})
round_r1=round_r1.join(gain_r1)
round_r1.fillna(0,inplace=True)
fortune[1]=round_r1['pre_round']-round_r1['lost']+round_r1['gain']
#（3）函数封装，创建模型
def game1(data,roundi):
    #当财富值包含为0的玩家时
    if len(data[data[roundi-1]==0])>0:
        round_i=pd.DataFrame({'pre_round':data[roundi-1],'lost':0})
        con=round_i['pre_round']>0
        round_i['lost'][con]=1
        round_players_i=round_i[con]
        choice_i=pd.Series(np.random.choice(person_n,len(round_players_i)))
        gain_i=pd.DataFrame({'gain':choice_i.value_counts()})
        round_i=round_i.join(gain_i)
        round_i.fillna(0,inplace=True)
        return round_i['pre_round']-round_i['lost']+round_i['gain']
    else:
        round_i=pd.DataFrame({'pre_round':data[roundi-1],'lost':1})
        choice_i=pd.Series(np.random.choice(person_n,100))
        gain_i=pd.DataFrame({'gain':choice_i.value_counts()})
        round_i=round_i.join(gain_i)
        round_i.fillna(0,inplace=True)
        return round_i['pre_round']-round_i['lost']+round_i['gain']

#--设置基本参数
person_n=[x for x in range(1,101)]
#person_y=list(range(1,101)) 等同于上一行代码
fortune=pd.DataFrame([100 for i in range(100)],index=person_n)
fortune.index.name='id'    
#--测试模型速度
starttime=time.time()
for round in range(1,17001):
    fortune[round]=game1(fortune,round)
    print('已经跑了第%i轮'%round)
game1_result=fortune.T
endtime=time.time()
print('模型总共用时%.3f秒'%(endtime-starttime))
#(4)绘制柱状图——不排序
'''
前100轮，按照每10轮绘制一次柱状图
100至1000轮，按照每100轮绘制一次柱状图
1000至17000轮，按照每400轮绘制一次柱状图
'''
os.chdir('F:\学习新玩意儿\python\作业完成\项目13\pic1')
def graph1(data,start,end,length):
    for n in list(range(start,end,length)):
        datai=data.iloc[n]
        plt.figure(figsize=(10,6))
        plt.bar(datai.index,datai.values,color='gray',
                alpha=0.8,width=0.9,)
        plt.ylim([0,400])
        plt.xlim([-10,110])
        plt.title('Round %d'%n)
        plt.xlabel('PlayerId')
        plt.ylabel('fortune')
        plt.grid(color='gray',linestyle='--',linewidth=0.5)
        plt.savefig('graph1_round_%d.png'%n,dpi=200)
        print('成功绘制第%d轮结果柱状图'%n)
graph1(game1_result,0,100,10)
graph1(game1_result,100,1000,100)
graph1(game1_result,1000,17000,400)
#绘制柱状图——排序
os.chdir('F:\学习新玩意儿\python\作业完成\项目13\pic2')
def graph2(data,start,end,length):
    for n in list(range(start,end,length)):
        datai=data.iloc[n].sort_values().reset_index()[n]
        plt.figure(figsize=(10,6))
        plt.bar(datai.index,datai.values,color='gray',
                alpha=0.8,width=0.9,)
        plt.ylim([0,400])
        plt.xlim([-10,110])
        plt.title('Round %d'%n)
        plt.xlabel('PlayerId')
        plt.ylabel('fortune')
        plt.grid(color='gray',linestyle='--',linewidth=0.5)
        plt.savefig('graph2_round_%d.png'%n,dpi=200)
        print('成功绘制第%d轮结果柱状图'%n)
graph2(game1_result,0,100,10)
graph2(game1_result,100,1000,100)
graph2(game1_result,1000,17000,400)

#(5)结论1
#--最富有的人相比于初始值翻了几倍
richest=game1_result.iloc[17000].max()
print('最富有的人翻了%.3f倍'%(richest/100))
#--前10%的人掌握着多少的财富？
#--前30%的人掌握着多少的财富？
#--又有百分之多少人财富缩水至100元以下了？
round_17000_1=pd.DataFrame({'money':game1_result.iloc[17000]}).sort_values(by='money',ascending=False).reset_index()
round_17000_1['fortune_pre']=round_17000_1['money']/round_17000_1['money'].sum()
round_17000_1['fortune_cum']=round_17000_1['fortune_pre'].cumsum()
v10=round_17000_1.iloc[9]['fortune_cum']
v30=round_17000_1.iloc[29]['fortune_cum']
vunder100=len(round_17000_1[round_17000_1['money']<100])
print('前%%10的人掌握着%.1f%%的财富'%(v10*100))
print('前%%30的人掌握着%.1f%%的财富'%(v30*100))
print('有%.1f%%人财富低于100元'%(vunder100))

#要求2：允许借贷的情况
#（1）函数封装
def game2(data,roundi):
    round_i=pd.DataFrame({'pre_round':data[roundi-1],'lost':1})
    choice_i=pd.Series(np.random.choice(person_n,100))
    gain_i=pd.DataFrame({'gain':choice_i.value_counts()})
    round_i=round_i.join(gain_i)
    round_i.fillna(0,inplace=True)
    return round_i['pre_round']-round_i['lost']+round_i['gain']
#--设置基本参数
person_n=[x for x in range(1,101)]
fortune=pd.DataFrame([100 for i in range(100)],index=person_n)
fortune.index.name='id'
#--进行游戏
starttime=time.time()
for round in range(1,17001):
    fortune[round]=game2(fortune,round)
    print('已经完成%i轮'%round)
game2_result=fortune.T
endtime=time.time()
print('总共用时%.3f秒'%(endtime-starttime))
#(2)查看财富分布情况
round_17000_2=pd.DataFrame({'money':game2_result.iloc[17000]}).sort_values(by='money',ascending=False).reset_index()
round_17000_2['fortune_per']=round_17000_2['money']/round_17000_2['money'].sum()
round_17000_2['fortune_cum']=round_17000_2['fortune_per'].cumsum()
v10=round_17000_2.iloc[9]['fortune_cum']
v30=round_17000_2.iloc[29]['fortune_cum']
vunder100=len(round_17000_2[round_17000_2['money']<100])
print('前%%10的人掌握着%.1f%%的财富'%(v10*100))
print('前%%30的人掌握着%.1f%%的财富'%(v30*100))
print('有%.1f%%人财富低于100元'%(vunder100))
#(3)画图
#绘制柱状图——排序
os.chdir('F:\学习新玩意儿\python\作业完成\项目13\pic3')
def graph3(data,start,end,length):
    for n in list(range(start,end,length)):
        datai=data.iloc[n].sort_values().reset_index()[n]
        plt.figure(figsize=(10,6))
        plt.bar(datai.index,datai.values,color='gray',
                alpha=0.8,width=0.9,)
        plt.ylim([-300,400])
        plt.xlim([-10,110])
        plt.title('Round %d'%n)
        plt.xlabel('PlayerId')
        plt.ylabel('fortune')
        plt.grid(color='gray',linestyle='--',linewidth=0.5)
        plt.savefig('graph3_round_%d.png'%n,dpi=200)
        print('成功绘制第%d轮结果柱状图'%n)
graph3(game2_result,0,100,10)
graph3(game2_result,100,1000,100)
graph3(game2_result,1000,17000,400)
#（4）游戏次数和财富标准差的关系
geme2_st=game2_result.std(axis=1)
geme2_st.plot(figsize=(12,5),color='red',alpha=0.6,grid=True)
#(5)逆袭之路
#玩家从18岁开始，在经过17年后为35岁，这个期间共进行游戏6200次左右
game2_round6200=pd.DataFrame({'money':game2_result.iloc[6200].sort_values().reset_index()[6200],
                              'id':game2_result.iloc[6200].sort_values().reset_index()['id'],
                                'color':'gray'})
game2_round6200['color'][game2_round6200['money']<0]='red'
id_broken=game2_round6200['id'][game2_round6200['money']<0].tolist()
plt.figure(figsize=(10,6))
plt.bar(game2_round6200.index,game2_round6200['money'],
        color=game2_round6200['color'],alpha=0.6)
plt.xlim([-10,110])
plt.ylim([-200,400])
plt.title('game2 Round6200')
plt.xlabel('playerID')
plt.ylabel('fortune')
plt.grid()
#--有没有逆袭的可能
os.chdir('F:\学习新玩意儿\python\作业完成\项目13\pic4')
def graph4(data,start,end,length):
    for n in list(range(start,end,length)):
        datai=pd.DataFrame({'money':data.iloc[n],'color':'gray'})
        datai['color'].loc[id_broken]='red'
        datai=datai.sort_values(by='money').reset_index()
        plt.figure(figsize=(10,6))
        plt.bar(datai.index,datai['money'],color=datai['color'],
                alpha=0.8,width=0.9,)
        plt.ylim([-300,400])
        plt.xlim([-10,110])
        plt.title('Round %d'%n)
        plt.xlabel('PlayerId')
        plt.ylabel('fortune')
        plt.grid(color='gray',linestyle='--',linewidth=0.5)
        plt.savefig('graph4_round_%d.png'%n,dpi=200)
        print('成功绘制第%d轮结果柱状图'%n)
graph4(game2_result,6200,17000,400)
#要求3、努力的人生会更好吗？
#（1）创建函数
def game3(data,roundi):
    round_i=pd.DataFrame({'pre_round':data[roundi-1],'lost':1})
    #努力的10个人[1,11,21,31,41,51,61,71,81,91]，获得钱的概率为0.0101，其余90人为0.899/90
    choice_i=pd.Series(np.random.choice(person_n,100,p=person_p))
    gain_i=pd.DataFrame({'gain':choice_i.value_counts()})
    round_i=round_i.join(gain_i)
    round_i.fillna(0,inplace=True)
    return round_i['pre_round']-round_i['lost']+round_i['gain']
#--设置参数
person_n=[x for x in range(1,101)]
fortune=pd.DataFrame([100 for i in range(100)],index=person_n)
fortune.index.name='id'
person_p=[0.899/90 for i in range(100)]
for i in [1,11,21,31,41,51,61,71,81,91]:
    person_p[i-1]=0.0101
#--进行游戏
starttime=time.time()
for round in range(1,17001):
    fortune[round]=game3(fortune,round)
    print('已经完成%i轮'%round)
game3_result=fortune.T
endtime=time.time()
print('总共用时%.3f秒'%(endtime-starttime))
#(2)绘制图形
os.chdir('F:\学习新玩意儿\python\作业完成\项目13\pic5')
data0=pd.DataFrame({'money':game3_result.iloc[0],'color':'gray'})
data0['color'].loc[[1,11,21,31,41,51,61,71,81,91]]='red'
plt.figure(figsize=(10,6))
plt.bar(data0.index,data0['money'],color=data0['color'],alpha=0.8,width=0.9,)
plt.ylim([-300,400])
plt.xlim([-10,110])
plt.title('努力的人--Round0')
plt.xlabel('PlayerId')
plt.ylabel('fortune')
plt.grid(color='gray',linestyle='--',linewidth=0.5)
plt.savefig('graph5_round_0.png',dpi=200)
#--前后对比
def graph5(data,start,end,length):
    for n in list(range(start,end,length)):
        datai=pd.DataFrame({'money':data.iloc[n],'color':'gray'})
        datai['color'].loc[[1,11,21,31,41,51,61,71,81,91]]='red'
        datai=datai.sort_values(by='money').reset_index()
        plt.figure(figsize=(10,6))
        plt.bar(datai.index,datai['money'],color=datai['color'],
                alpha=0.8,width=0.9,)
        plt.ylim([-300,400])
        plt.xlim([-10,110])
        plt.title('Round %d'%n)
        plt.xlabel('PlayerId')
        plt.ylabel('fortune')
        plt.grid(color='gray',linestyle='--',linewidth=0.5)
        plt.savefig('graph5_round_%d.png'%n,dpi=200)
        print('成功绘制第%d轮结果柱状图'%n)
graph5(game3_result,0,100,10)
graph5(game3_result,100,1000,100)
graph5(game3_result,1000,17000,400)
#（3）结论3
#努力的人有70%都在200元以上，超过了20%的人
result_round16999=game3_result.iloc[16999].sort_values(ascending=False).reset_index()
id_hard=game3_result.iloc[16999,[0,10,20,30,40,50,60,70,80,90]]
rich_hard_per=len(id_hard[id_hard>200])/10
print('努力的10个人中有%.1f%%收入在200元以上'%(rich_hard_per*100))
print('finished!!!')