import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image

#use the whole screen
st.set_page_config(layout="wide")
st.title('销售营收统计小工具')
#顶头背景图
image = Image.open('logo.png')
interest_option = st.sidebar.radio("请选择计算利息的方案：", ['固定利率','阶梯式利率'])
st.subheader('使用方法：选择合适条件，实时统计销售营收。')

@st.cache(suppress_st_warning=True)
def total_revenue(income,currency,tons,days,interest_opt,
year_interest=0.084,volume_interest=0,tariff=0.08,value_added=0.09,custom=280,operation=70):

    """
    #income是订单每吨金额（货值美金），因变量
    #currency是当天选择的汇率，因变量
    #volume_interest是从量关税，因变量，默认为0
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
        if volume_interest == 0:
            #计算货值的总利率费用
            total_interest = income*tons*currency*(1+tariff)*(1+value_added)*daily_interest*days
        else:
            total_interest = (income*tons*currency*(1+value_added)+(tons*volume_interest))*daily_interest*days
        #合并总营收
        total = custom_operation + total_interest

    elif interest_opt == 2:
        ###阶梯式利息费用###
        #确定阶梯阶段
        period1,period2,period3 = 0,0,0
        daily_interest1 = 0.072/365
        daily_interest2 = 0.084/365
        daily_interest3 = 0.096/365
        if days<=30:
            if volume_interest == 0:
                period1 = income*tons*currency*(1+tariff)*(1+value_added)*daily_interest1*days
            else:
                period1 = (income*tons*currency*(1+value_added)+(tons*volume_interest))*daily_interest1*days
        elif days >=31 and days <=60:
            if volume_interest == 0:
                period1 = income*tons*currency*(1+tariff)*(1+value_added)*daily_interest1*30
                period2 = (days-30)*(income*tons*currency*(1+tariff)*(1+value_added)*daily_interest2)
            else:
                period1 = (income*tons*currency*(1+value_added)+(tons*volume_interest))*daily_interest1*30
                period2 = (days-30)*(income*tons*currency*(1+value_added)+(tons*volume_interest))*daily_interest2
        else:
            if volume_interest == 0:
                period1 = income*tons*currency*(1+tariff)*(1+value_added)*daily_interest1*30
                period2 = 30*(income*tons*currency*(1+tariff)*(1+value_added)*daily_interest2)
                period3 = (days-60)*(income*tons*currency*daily_interest3)
            else:
                period1 = (income*tons*currency*(1+value_added)+(tons*volume_interest))*daily_interest1*30
                period2 = (income*tons*currency*(1+value_added)+(tons*volume_interest))*daily_interest2*30
                period3 = (income*tons*currency*(1+value_added)+(tons*volume_interest))*daily_interest3*(days-60)
        total_interest = period1 + period2 + period3

        #计算清关代理费和操作费的总和
        custom_operation = (custom+operation)*tons
        #合并总营收
        total = custom_operation + total_interest

    return total, custom_operation, total_interest

############################################
#streamlit layout design#
############################################
#income,currency,tons,days,interest_opt,
#year_interest=0.084,volume_interest=0,tariff=0.08,value_added=0.09,custom=280,operation=70
if interest_option == '固定利率':
    st.markdown('> 年利率默认8.4%；清关代理费默认280元/每吨；操作费默认70元/每吨；关税默认8%；增值税默认9%；从量关税默认0%。')
    try:
        # Attempt a layout with beta_expander
        layout = st.beta_expander('营收统计：', expanded=True)
        # Add a header
        with layout:
            # Add another container
            left, middle, right = st.beta_columns((1, 1, 2))

            with left:
                income = st.number_input('每吨货值(美元)：',0,10000,3500)
                currency = st.number_input('汇率：',5.0,7.5,6.45)
                tons = st.slider('吨数：',1,100,27,1)
                days = st.slider('天数：',1,150,60,1)
                interest_opt = 1

            with middle:
                volume_interest = st.number_input('从量关税：',0)
                tariff = st.slider('关税：',4.0,15.0,8.4,0.5)
                tariff = tariff/100
                value_added = st.slider('增值税：',4.0,15.0,9.0,0.5)
                value_added = value_added/100
                year_interest = st.slider('年固定利率：',4.0,15.0,8.4,0.5)
                year_interest = year_interest/100
                #call the function
                total, custom_operation, total_interest = total_revenue(income,currency,tons,days,interest_opt,year_interest,
                volume_interest,tariff,value_added)

            with right:
                #营收统计
                #st.markdown("<h2 style='text-align: center; color: black;'>营收统计</h1>", unsafe_allow_html=True)
                st.image(image,clamp=True)
                st.markdown("* 清关代理费操作费合计："+"￥"+str(custom_operation))
                st.markdown("* 平均每吨清关代理费用："+"￥"+str(round(custom_operation/tons,2)))
                st.markdown("")
                st.markdown("* 总利息费用："+"￥"+str(round(total_interest,2)))
                st.markdown("* 平均每吨中利息费用："+"￥"+str(round(total_interest/tons,2)))
                st.markdown("")
                st.markdown("* 总计费用："+"￥"+str(round(total,2)))
                st.markdown("* 平均每吨总计费用："+"￥"+str(round(total/tons,2)))

    except Exception as e:
        print(e)

elif interest_option == '阶梯式利率':
    try:
        st.markdown('> 清关代理费默认280元/每吨；操作费默认70元/每吨；关税默认8%；增值税默认9%；从量关税默认0%。')
        st.text('备注：阶梯式年利率，第一个月7.2%；第二个月8.4%；第三个月9.6%。')
        # Attempt a layout with beta_expander
        layout = st.beta_expander('输入特定的条件：', expanded=True)
        # Add a header
        with layout:
            # Add another container
            left, middle, right = st.beta_columns((1, 1, 2))

            with left:
                income = st.number_input('每吨货值(美元)：',0,10000,3500)
                currency = st.number_input('汇率：',5.0,7.5,6.45)
                tons = st.slider('吨数：',1,100,27,1)
                days = st.slider('天数：',1,150,60,1)

            with middle:
                interest_opt = 2
                volume_interest = st.number_input('从量关税：',0)
                tariff = st.slider('关税：',4.0,15.0,8.0,0.5)
                tariff = tariff/100
                value_added = st.slider('增值税：',4.0,15.0,9.0,0.5)
                value_added = value_added/100
                year_interest = st.slider('年固定利率：',4.0,15.0,8.4,0.5)
                year_interest = year_interest/100
                #call the function
                total, custom_operation, total_interest = total_revenue(income,currency,tons,days,interest_opt,year_interest,
                volume_interest,tariff,value_added)

            with right:
                #营收统计
                #st.markdown("<h2 style='text-align: center; color: black;'>营收统计</h1>", unsafe_allow_html=True)
                st.image(image,clamp=True)
                st.markdown("* 清关代理费操作费合计："+"￥"+str(custom_operation))
                st.markdown("* 平均每吨清关代理费用："+"￥"+str(round(custom_operation/tons,2)))
                st.markdown("")
                st.markdown("* 总利息费用："+"￥"+str(round(total_interest,2)))
                st.markdown("* 平均每吨中利息费用："+"￥"+str(round(total_interest/tons,2)))
                st.markdown("")
                st.markdown("* 总计费用："+"￥"+str(round(total,2)))
                st.markdown("* 平均每吨总计费用："+"￥"+str(round(total/tons,2)))
    except Exception as e:
        print(e)
