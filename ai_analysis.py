from openai import OpenAI
import os


def safe_text(data, max_chars=3000):
    """
    限制输入长度，防止异常数据导致token爆炸
    """
    text = str(data)

    if len(text) > max_chars:
        text = text[:max_chars] + "\n...(内容已截断)"

    return text



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


    prompt = f"""
你是一名专业B2B商业分析师。

请根据以下经营数据生成分析报告。


【核心指标】

{safe_text(metrics)}


【TOP客户】

{safe_text(customers)}


【客户集中度】

{safe_text(customer_analysis)}


【TOP产品】

{safe_text(products)}


【产品贡献】

{safe_text(product_analysis)}


【销售趋势】

{safe_text(trend_analysis)}



请输出：

1. 经营情况总结

2. 主要风险

3. 增长机会

4. 具体经营建议


要求：
- 使用商业分析语言
- 避免重复数据
- 给出可执行建议
"""


    print("AI输入字符数:", len(prompt))


    try:

        response = client.chat.completions.create(

            model="deepseek-v4-flash",

            max_tokens=1200,

            messages=[

                {
                    "role": "system",
                    "content": "你是一名专业B2B商业分析师"
                },

                {
                    "role": "user",
                    "content": prompt
                }

            ]

        )


        print(
            "输入token:",
            response.usage.prompt_tokens
        )

        print(
            "输出token:",
            response.usage.completion_tokens
        )


        return response.choices[0].message.content


    except Exception as e:

        return f"""
AI分析失败：

{str(e)}
"""
