
import requests
from bs4 import BeautifulSoup
import pandas as pd

baseurl = "https://www.emlakjet.com"
url = "https://www.emlakjet.com/satilik-konut/istanbul-kadikoy/1/"


house_links= []

for i in range(1,51):
    
    r = requests.get(f"https://www.emlakjet.com/satilik-konut/istanbul-kadikoy/{i}/")
    soup = BeautifulSoup(r.content, "lxml")
    soup1 = soup.find("div", class_ = "ej73 styles_listingContent__2o-CU")
    soup2 = soup1.find_all("div", class_ = "styles_listingItem__1asTK")
    for item in soup2:
        link = item.a.get("href")
        all_links = baseurl + link
        house_links.append(all_links)


#test_link = "https://www.emlakjet.com/ilan/ilke-den-idealtepe-isiklarda-ozel-dekorlu-balkonlu-firsat-21-9239506/"
house_properties = []

for link in house_links:
    
    r = requests.get(link)
    soup = BeautifulSoup(r.content, "lxml")
    try:
        price = soup.find("div", class_ = "styles_price__1e65F").text
    except:
        price = None
    table = soup.find("div", id = "bilgiler")
    try:
        table_rows = table.find_all("div", class_ = "styles_listingInformationTable__1X9Aq")
    except:
        pass
    
    house_dict = {
        "İlan Numarası": None,
        "İlan Oluşturma Tarihi": None,
        "İlan Güncelleme Tarihi": None,
        "Türü": None,
        "Kategorisi": None,
        "Yapı Tipi": None,
        "Net Metrekare": None,
        "Brüt Metrekare": None,
        "Salon Metrekare": None,
        "Oda Sayısı": None,
        "Binanın Yaşı": None,
        "Bulunduğu Kat": None,
        "Binanın Kat Sayısı": None,
        "Isıtma Tipi": None,
        "Aidat": None,
        "Kira Getirisi": None,
        "Banyo Sayısı": None,
        "WC Sayısı": None,
        "Site İçerisinde": None,
        "Eşya Durumu": None,
        "Kullanım Durumu": None,
        "Fiyat Durumu": None,
        "Yapı Durumu": None,
        "Krediye Uygunluk": None,
        "Yatırıma Uygunluk": None,
        "Takas": None,
        "Fiyat": price
        
    
        }
    
    for item in table_rows:
        for k in item.find_all("div", class_ = "styles_tableHalfRow__3zO2j"):
            key = k.find_all("div", class_ = "styles_tableColumn__2x6nG")[0].text
            value = k.find_all("div", class_ = "styles_tableColumn__2x6nG")[1].text
            house_dict[key] = value
        
    house_properties.append(house_dict)
                    
    df = pd.DataFrame(house_properties)

df.to_csv("emlakjet.csv")