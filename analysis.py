import pandas as pd



def calculate_sales_metrics(df):

    metrics = {}

    gmv = df["实付款（元）"].sum()

    order_count = df["订单号"].nunique()

    # 改成客户主体
    customer_count = df["客户主体"].nunique()

    product_count = df["货品标题"].nunique()


    avg_order_value = (
        gmv / order_count
        if order_count > 0
        else 0
    )


    metrics["GMV"] = round(gmv, 2)

    metrics["订单数量"] = order_count

    metrics["客户主体数量"] = customer_count

    metrics["产品数量"] = product_count

    metrics["客单价"] = round(
        avg_order_value,
        2
    )


    return metrics





def top_customers(df, n=10):

    """
    TOP客户销售额
    基于客户主体
    """


    customer_df = df.dropna(
        subset=["客户主体"]
    )


    result = (
        customer_df
        .groupby("客户主体")
        ["实付款（元）"]
        .sum()
        .sort_values(
            ascending=False
        )
        .head(n)
    )


    return result





def top_products(df, n=10):

    """
    TOP产品销售额
    """


    result = (
        df.groupby("货品标题")
        ["实付款（元）"]
        .sum()
        .sort_values(
            ascending=False
        )
        .head(n)
    )


    return result





# ==========================
# 客户集中度分析
# ==========================


def customer_concentration(df):

    """
    客户集中度分析
    """


    result = {}


    customer_df = df.dropna(
        subset=["客户主体"]
    )


    customer_sales = (
        customer_df
        .groupby("客户主体")
        ["实付款（元）"]
        .sum()
        .sort_values(
            ascending=False
        )
    )


    customer_total_sales = (
        customer_sales.sum()
    )


    top10_sales = (
        customer_sales
        .head(10)
        .sum()
    )


    # 数据质量

    result["客户主体缺失订单数"] = int(
        df["客户主体"]
        .isnull()
        .sum()
    )


    result["客户信息完整率"] = round(
        len(customer_df)
        /
        len(df)
        *
        100,
        2
    )


    # 客户分析

    result["客户主体数量"] = (
        len(customer_sales)
    )


    result["有效客户销售额"] = round(
        customer_total_sales,
        2
    )


    result["TOP10客户销售额"] = round(
        top10_sales,
        2
    )


    result["TOP10客户贡献率"] = round(
        top10_sales
        /
        customer_total_sales
        *
        100,
        2
    )


    return result





# ==========================
# 产品贡献分析
# ==========================


def product_contribution(df):


    result = {}


    product_sales = (
        df.groupby("货品标题")
        ["实付款（元）"]
        .sum()
        .sort_values(
            ascending=False
        )
    )


    total_sales = product_sales.sum()


    top5_sales = (
        product_sales
        .head(5)
        .sum()
    )


    result["SKU数量"] = len(product_sales)


    result["TOP5产品贡献率"] = round(
        top5_sales
        /
        total_sales
        *
        100,
        2
    )


    result["最大贡献产品"] = (
        product_sales.index[0]
    )


    result["最大产品销售额"] = round(
        product_sales.iloc[0],
        2
    )


    return result





# ==========================
# 销售趋势分析
# ==========================


def sales_trend(df):


    result = {}


    temp = df.copy()


    temp["月份"] = (
        temp["订单创建时间"]
        .dt.to_period("M")
        .astype(str)
    )


    monthly_sales = (
        temp.groupby("月份")
        ["实付款（元）"]
        .sum()
    )


    result["月销售额"] = (
        monthly_sales.to_dict()
    )


    return result