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
            "https://ifoodie.tw/explore/" + self.area + "/list?sortby=popular&opening=true")
        
        soup = BeautifulSoup(response.content, "html.parser")