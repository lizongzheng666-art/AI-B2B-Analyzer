import plotly.express as px
import streamlit as st
import pandas as pd


from ai_analysis import generate_ai_report
from data_clean import (
    load_data,
    clean_data,
    data_quality_report
)

from analysis import (
    calculate_sales_metrics,
    top_customers,
    top_products,
    customer_concentration,
    product_contribution,
    sales_trend
)


# ==========================
# 页面设置
# ==========================

st.set_page_config(
    page_title="AI B2B经营分析助手",
    page_icon="📊",
    layout="wide"
)



# ==========================
# 首页 Hero
# ==========================


st.markdown(
"""
<style>

.hero{
    text-align:center;
    padding:40px 20px;
}


.hero h1{
    font-size:55px;
    font-weight:700;
}


.hero h2{
    font-size:28px;
    color:#555;
}


.hero p{
    font-size:20px;
    color:#666;
}


.upload-box{

    background:#f6f8fb;
    padding:30px;
    border-radius:18px;
    margin-top:30px;

}


.feature{

    text-align:center;
    padding:20px;

}


</style>

""",
unsafe_allow_html=True
)




st.markdown(
"""
<div class="hero">


<h1>
📊 AI B2B经营分析助手
</h1>


<h2>
让订单数据转化为经营洞察
</h2>


<p>
基于 Python 数据处理 + AI 大模型分析
</p>


<p>
自动完成 数据清洗 → 指标分析 → 商业诊断
</p>


</div>

""",
unsafe_allow_html=True
)

st.markdown(
"""
<div style="
text-align:center;
margin-top:20px;
font-size:24px;
font-weight:600;
color:#444;
">

开发者：李成裕

</div>

<div style="
text-align:center;
margin-top:8px;
font-size:16px;
color:#888;
">

Python Data Analytics · AI Business Intelligence

</div>

""",
unsafe_allow_html=True
)


# ==========================
# 功能展示
# ==========================


col1,col2,col3,col4 = st.columns(4)


with col1:

    st.markdown(
    """
    <div class="feature">

    🧹

    <br>

    数据清洗

    <br>

    自动处理异常数据

    </div>
    """,
    unsafe_allow_html=True
    )



with col2:

    st.markdown(
    """
    <div class="feature">

    📈

    <br>

    经营分析

    <br>

    核心指标计算

    </div>
    """,
    unsafe_allow_html=True
    )



with col3:

    st.markdown(
    """
    <div class="feature">

    👥

    <br>

    客户洞察

    <br>

    识别关键客户

    </div>
    """,
    unsafe_allow_html=True
    )



with col4:

    st.markdown(
    """
    <div class="feature">

    🤖

    <br>

    AI诊断

    <br>

    自动生成建议

    </div>
    """,
    unsafe_allow_html=True
    )





st.divider()



# ==========================
# 上传入口
# ==========================


st.markdown(
"""
<div class="upload-box">

<h2 style="text-align:center">

📂 上传企业订单数据

</h2>


<p style="text-align:center">

支持 Excel 文件，自动生成经营分析报告

</p>


</div>

""",
unsafe_allow_html=True
)



uploaded_file = st.file_uploader(
    "",
    type=["xlsx"]
)



st.caption(
"Developed by Chengyu Li"
)





if uploaded_file:


    st.success("数据上传成功")



    # ==========================
    # 数据读取
    # ==========================

    df = load_data(uploaded_file)



    # 清洗

    clean_df, clean_report = clean_data(df)



    # ==========================
    # 指标
    # ==========================


    metrics = calculate_sales_metrics(
        clean_df
    )



    st.divider()


    st.subheader(
        "📈 经营概览"
    )



    col1,col2,col3,col4,col5 = st.columns(5)



    col1.metric(
        "💰 GMV",
        f"{metrics['GMV']/10000:.2f} 万元"
    )


    col2.metric(
        "📦 订单数量",
        f"{metrics['订单数量']} 单"
    )


    col3.metric(
        "👥 客户主体",
        f"{metrics['客户主体数量']} 个"
    )


    col4.metric(
        "🏷️ 产品SKU",
        f"{metrics['产品数量']} 个"
    )


    col5.metric(
        "💵 客单价",
        f"{metrics['客单价']:.2f} 元"
    )




    # ==========================
    # 分析模块
    # ==========================


    customer_result = top_customers(
        clean_df
    )


    product_result = top_products(
        clean_df
    )


    customer_analysis = customer_concentration(
        clean_df
    )


    product_analysis = product_contribution(
        clean_df
    )


    trend_analysis = sales_trend(
        clean_df
    )




    st.divider()


    st.subheader(
        "📊 经营分析"
    )



    tab1,tab2,tab3 = st.tabs(
        [
            "👥 客户分析",
            "📦 产品分析",
            "📈 销售趋势"
        ]
    )



    # ==========================
    # 客户
    # ==========================


    with tab1:


        st.markdown(
            "### TOP客户贡献"
        )


        customer_chart = (
            customer_result
            .reset_index()
        )


        customer_chart.columns=[
            "客户主体",
            "销售额"
        ]


        fig_customer = px.bar(
            customer_chart,
            x="客户主体",
            y="销售额",
            title="TOP10客户销售额"
        )


        st.plotly_chart(
            fig_customer,
            use_container_width=True
        )


        st.write(
            customer_analysis
        )





    # ==========================
    # 产品
    # ==========================


    with tab2:


        st.markdown(
            "### TOP产品贡献"
        )


        product_chart = (
            product_result
            .reset_index()
        )


        product_chart.columns=[
            "产品",
            "销售额"
        ]


        fig_product = px.bar(
            product_chart,
            x="产品",
            y="销售额",
            title="TOP10产品销售额"
        )


        st.plotly_chart(
            fig_product,
            use_container_width=True
        )


        st.write(
            product_analysis
        )





    # ==========================
    # 趋势
    # ==========================


    with tab3:


        st.markdown(
            "### 月度销售趋势"
        )


        trend_df = pd.DataFrame(
            trend_analysis["月销售额"].items(),
            columns=[
                "月份",
                "销售额"
            ]
        )


        fig = px.line(
            trend_df,
            x="月份",
            y="销售额",
            markers=True
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )





    # ==========================
    # AI
    # ==========================


    st.divider()


    st.subheader(
        "🤖 AI经营诊断"
    )


    if st.button(
        "生成AI分析报告"
    ):


        with st.spinner(
            "AI正在分析经营数据..."
        ):


            report = generate_ai_report(

                metrics,

                customer_result,

                product_result,

                customer_analysis,

                product_analysis,

                trend_analysis

            )


        st.markdown(
            report
        )




    # ==========================
    # 技术详情
    # ==========================


    st.divider()


    with st.expander(
    "🔧 数据处理与清洗记录（Data Processing Log）"
    ):

        st.markdown(
        """
        ### 数据清洗流程

        本系统自动完成：

        1. 删除重复订单
        2. 删除关键字段缺失记录
        3. 日期格式标准化
        4. 金额字段转换
        5. 客户主体字段构建
        6. 无价值字段删除

        """
        )


        st.subheader(
            "清洗统计"
        )


        st.write(
            clean_report
        )


        st.subheader(
            "数据质量检查"
        )


        st.write(
            data_quality_report(df)
        )


        st.subheader(
            "清洗后数据样例"
        )


        st.dataframe(
            clean_df.head(10)
        )