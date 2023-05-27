from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
import requests


# 發送 HTTP GET 請求獲取網頁內容
# url = 'https://julientpu.github.io/coco都可-分店'
url_allshop = 'https://jiatongoo.github.io/alldrinks.html'

# 飲料抽象類別
class Drink(ABC):
 
    #def __init__(self, area):
        #self.area = area  # 地區
 
    @abstractmethod
    def scrape(self):  #抽象方法(abstractmethod)就是共同的介面，未來新增的美食網頁爬蟲，就可以依據各自的邏輯來實作這個介面。
        pass

# 飲料地圖爬蟲
class iDrink(Drink):
    
    def scrape(self): # 取得經緯度

        # 解析HTML內容
        response = requests.get(url_allshop)        
        soup = BeautifulSoup(response.text, 'html.parser')

        coordinates = [] # 儲存經緯度的 list
        cards = soup.find_all('tr', {"class": "data"}) # 提取經緯度資料，先讀取所有tr標籤，並且class為data的元素。

        # 找到tr標籤內，包含經緯度資料的元素。分別存入coordinates list中。
        for card in cards:
            SHOP = card.find('td', {"class": "ShopName"}).getText() #店名
            BRANCH_SHOP = card.find('td', {"class": "shop"}).getText() #分店
            Addr = card.find('td', {"class": "address"}).getText() #地址
            LAT = card.find('td', {"class": "lat"}).text  
            LON = card.find('td', {"class": "lon"}).text

            coordinates.append((SHOP, BRANCH_SHOP, Addr, float(LAT), float(LON)))
        return coordinates
    
 

'''
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
'''    