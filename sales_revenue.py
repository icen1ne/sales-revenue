#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import streamlit as st

#use the whole screen
st.set_page_config(layout="wide")
st.title('马力科技销售部营收统计小工具')
interest_option = st.sidebar.radio("请选择计算利息的方案：", ['固定利率','阶梯式利率'])
st.markdown('> 请通过滑动条选择需要的每吨金额、汇率、吨数、利息日数、年利率')
st.text('年利率默认8.4%；清关代理费默认280元/每吨；操作费默认70元/每吨')
# In[38]:


def total_revenue(income,currency,tons,days,interest_opt,
year_interest=0.084,volume_interest=0,tariff=0.08,value_added=0.09,custom=280,operation=70):

    """
    #income是订单每吨金额（货值美金），因变量
    #currency是当天选择的汇率，因变量
    #volume_interest是从属关税，因变量，默认为0
    #tariff是海关关税，因变量，默认为0.08
    #value_added是增值税，因变量，默认为0.09
    #tons吨数是因变量，浮动变化
    #operation操作费是因变量，浮动变化
    #days是计算利息的日数
    #year_interest是年利率，year_interest转化成日利率
    #interest_opt是利率计算方案，固定利率或者阶梯式利率
    #custom是清关代理费，目前固定是280元每吨
    """
    if interest_opt == 1:
        
        #计算日利率
        interest = year_interest
        daily_interest = year_interest/365
        #计算清关代理费和操作费的总和
        custom_operation = (custom+operation)*tons
        #计算货值的总利率费用
        total_interest = income*tons*currency*daily_interest*days
        #合并总营收
        total = custom_operation + total_interest

    elif interest_opt == 2:
        ###阶梯式利息费用###
        #确定阶梯阶段
        period1,period2,period3 = 0,0,0
        if days<=30:
            daily_interest1 = 0.072/365
            period1 = days*income*tons*currency*daily_interest1
        elif days >=31 and days <=60:
            daily_interest1 = 0.072/365
            period1 = days*income*tons*currency*daily_interest1
            daily_interest2 = 0.084/365
            period2 = (days-30)*(income*tons*currency*daily_interest2)
        else:
            daily_interest1 = 0.072/365
            period1 = days*income*tons*currency*daily_interest1
            daily_interest2 = 0.084/365
            period2 = (days-30)*(income*tons*currency*daily_interest2)
            daily_interest3 = 0.096/365
            period3 = (days-60)*(income*tons*currency*daily_interest3)
        total_interest = period1 + period2 + period3

        #计算清关代理费和操作费的总和
        custom_operation = (custom+operation)*tons
        #合并总营收
        total = custom_operation + total_interest

    return total, custom_operation, total_interest


#income,currency,tons,days,interest_opt,year_interest=0.084,custom=280,operation=70
if interest_option == '固定利率':
    try:
        income = st.number_input('请输入每吨货值的美金金额：',1)
        currency = st.number_input('请输入制定的汇率：',6.0)
        tons = st.number_input('请输入吨数：',1)
        days = st.slider('请输入天数：',1,150,60,1)
        interest_opt = 1
        year_interest = st.slider('请滑动至需要的年固定利率：默认8.4%',0.05,0.15,0.084,0.005)
        total, custom_operation, total_interest = total_revenue(income,currency,tons,days,interest_opt,year_interest)

        #营收统计
        st.subheader("基本数据统计")
        st.markdown("* 清关代理费操作费合计："+"￥"+str(custom_operation)+"  \n"
            "* 总利息费用："+"￥"+str(round(total_interest,2))+"  \n"
            "* 总计费用："+"￥"+str(round(total,2)))
        st.text('数字解析：以上数字为销售营收类别汇总统计。')
        st.markdown('#')
    except Exception as e:
        print(e)

elif interest_option == '阶梯式利率':
    try:
        income = st.number_input('请输入每吨货值的美金金额：',1)
        currency = st.number_input('请输入制定的汇率：',6.0)
        tons = st.number_input('请输入吨数：',1)
        days = st.slider('请输入天数：',1,150,60,1)
        interest_opt = 2
        total, custom_operation, total_interest = total_revenue(income,currency,tons,days,interest_opt)

        #营收统计
        st.subheader("基本数据统计")
        st.markdown("* 清关代理费操作费合计："+"￥"+str(custom_operation)+"  \n"
            "* 总利息费用："+"￥"+str(round(total_interest,2))+"  \n"
            "* 总计费用："+"￥"+str(round(total,2)))
        st.text('数字解析：以上数字为销售营收类别汇总统计。')
        st.markdown('#')
    except Exception as e:
        print(e)
