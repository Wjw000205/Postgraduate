import requests

def get_weather(province,city):

    url = "https://cn.apihz.cn/api/tianqi/tqyb.php?id=88888888&key=88888888&sheng="+province+"&place="+city

    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查HTTP错误（如404/500）

        # 解析JSON响应
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print("请求失败:", e)