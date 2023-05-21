from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
import requests


# 美食抽象類別
class Food(ABC):
 
    def __init__(self, area):
        self.area = area  # 地區
 
    @abstractmethod
    def scrape(self):  #抽象方法(abstractmethod)就是共同的介面，未來新增的美食網頁爬蟲，就可以依據各自的邏輯來實作這個介面。
        pass


 
# 愛食記爬蟲
class IFoodie(Food):
 
    def scrape(self):
        response = requests.get(
            "https://ifoodie.tw/explore/" + self.area + "/list?opening=true")
             # https://ifoodie.tw/explore/%E5%8F%B0%E5%8C%97%E5%B8%82/list?opening=true
 
        soup = BeautifulSoup(response.content, "html.parser")

        # 爬取前五筆餐廳卡片資料
        cards = soup.find_all(
            'div', {'class': 'jsx-1156793088 restaurant-info'}, limit=5)
 
        content = ""
        for card in cards:
 
            title = card.find(  # 餐廳名稱
                "a", {"class": "jsx-1156793088 title-text"}).getText()
 
            stars = card.find(  # 餐廳評價
                "div", {"class": "jsx-2373119553 text"}).getText()
 
            address = card.find(  # 餐廳地址
                "div", {"class": "jsx-1156793088 address-row"}).getText()
 
 
            #將取得的餐廳名稱、評價及地址連結一起，並且指派給content變數
            content += f"{title} \n{stars}顆星 \n{address} \n\n"
 
        return content