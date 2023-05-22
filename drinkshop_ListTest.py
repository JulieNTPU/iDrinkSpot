import requests
from bs4 import BeautifulSoup
import pandas as pd


url = "https://www.findcoupon.tw/showroom-1077/store"

# 发起 HTTP 请求并获取网页内容
response = requests.get(url)
content = response.text

# 使用 BeautifulSoup 解析网页内容
soup = BeautifulSoup(content, "html.parser")

# 找到包含饮料店信息的元素
stores = soup.find_all("div", class_="box-body box box-default")

# 创建空列表来存储饮料店数据
data = []

# 遍历每个饮料店元素，提取名称和地址信息
for store in stores:
    name = store.find("div", class_="td").text.strip()
    address = store.find("i", class_="fa fa-map-marker").text.strip()
    data.append({"Name": name, "Address": address})

# 将饮料店数据转换为 DataFrame
df = pd.DataFrame(data)

# 输出表格
print(df)
