from openai import OpenAI
import os

def generate_ai_report(
    metrics,
    customers,
    products,
    customer_analysis,
    product_analysis,
    trend_analysis
):




      client = OpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com"
    )


    response = client.chat.completions.create(

        model="deepseek-chat"

        messages=[

            {
                "role":"system",
                "content":"你是一名专业B2B商业分析师"
            },

            {
                "role":"user",
                "content":f"""
根据以下经营数据生成分析：

核心指标：
{metrics}

客户分析：
{customers}

客户集中度：
{customer_analysis}

产品分析：
{product_analysis}

销售趋势：
{trend_analysis}


输出：

1.经营情况

2.风险

3.机会

4.建议

"""
            }
        ]

    )


    return response.choices[0].message.content
