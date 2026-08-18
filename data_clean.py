import pandas as pd



def load_data(file_path):
    """
    读取原始订单数据
    """

    df = pd.read_excel(file_path)

    return df





def data_quality_report(df):
    """
    数据质量检查
    """

    report = {}

    report["数据行数"] = df.shape[0]

    report["字段数量"] = df.shape[1]


    # 原始字段缺失

    missing = df.isnull().sum()


    report["原始字段缺失情况"] = (
        missing[missing > 0]
        .to_dict()
    )


    # 客户主体质量检查

    if (
        "买家公司名称" in df.columns
        and
        "买家会员" in df.columns
    ):

        customer_missing = (
            df["买家公司名称"].isnull()
            &
            df["买家会员"].isnull()
        ).sum()


        report["客户主体真正缺失数量"] = int(
            customer_missing
        )


    # 重复数据

    report["重复行数量"] = int(
        df.duplicated().sum()
    )


    return report





def clean_data(df):
    """
    B2B订单数据清洗流程

    包含：
    1. 删除重复订单
    2. 删除关键字段缺失
    3. 日期标准化
    4. 金额格式转换
    5. 创建客户主体字段
    6. 删除无价值字段
    """

    report = {}


    # =====================
    # 清洗前
    # =====================

    report["清洗前数据量"] = len(df)



    # =====================
    # 删除重复数据
    # =====================

    duplicate_count = df.duplicated().sum()


    df = df.drop_duplicates()


    report["删除重复数据"] = int(duplicate_count)




    # =====================
    # 删除关键字段为空
    # =====================

    key_columns = [
        "订单号",
        "订单创建时间",
        "实付款（元）"
    ]


    exist_columns = [
        col for col in key_columns
        if col in df.columns
    ]


    before = len(df)


    if exist_columns:

        df = df.dropna(
            subset=exist_columns
        )


    report["删除缺失关键字段"] = (
        before - len(df)
    )





    # =====================
    # 创建客户主体
    # =====================

    if "买家公司名称" in df.columns:


        df["客户主体"] = (
            df["买家公司名称"]
        )


        if "买家会员" in df.columns:


            df["客户主体"] = (
                df["客户主体"]
                .fillna(
                    df["买家会员"]
                )
            )



    report["客户主体缺失数量"] = (
        df["客户主体"].isnull().sum()
        if "客户主体" in df.columns
        else None
    )





    # =====================
    # 日期转换
    # =====================

    date_columns = [
        "订单创建时间",
        "订单付款时间"
    ]


    for col in date_columns:


        if col in df.columns:


            df[col] = pd.to_datetime(
                df[col],
                errors="coerce"
            )





    # =====================
    # 金额转换
    # =====================

    money_columns = [
        "实付款（元）",
        "结算价（元）",
        "货品总价"
    ]


    for col in money_columns:


        if col in df.columns:


            df[col] = (
                df[col]
                .astype(str)
                .str.replace(
                    ",",
                    ""
                )
            )


            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )






    # =====================
    # 删除无价值字段
    # =====================

    remove_columns = [

        "发票：购货单位名称",
        "发票：纳税人识别号",
        "发票：地址、电话",
        "发票：开户行及账号"

    ]



    remove_exist = [

        col for col in remove_columns
        if col in df.columns

    ]



    df = df.drop(
        columns=remove_exist
    )





    # =====================
    # 清洗后数量
    # =====================

    report["清洗后数据量"] = len(df)



    return df, report