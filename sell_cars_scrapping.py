import requests
from bs4 import BeautifulSoup
import pandas as pd


cities = ["hyderabad","ahmedabad","ajmer","bangalore","chandigarh","new-delhi","pune","gurgaon",
"ghaziabad","jaipur","jodhpur","kota","mumbai","noida","udaipur"]

header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
}

data = {
    'Vehicle Name': [],
    'Year of Model' : [],
    'Brand Name' : [],
    'Engine' : [],
    'Kms Driven' : [],
    'Variant' : [],
    'Transmission Type' : [],
    'Number of Photos Uploaded' : [],
    'Total Views' : [],
    'Price of the Car' : [],
}


for city in cities : 
    test_url = f'https://www.cardekho.com/buy-used-cars+in+{city}'
    response = requests.get(test_url,headers=header)
    soup = BeautifulSoup(response.text, 'lxml')
    grid = soup.find_all('div',class_='gsc_col-md-4 gsc_col-sm-6 gsc_col-xs-12')
    for elem in grid:
        data['Vehicle Name'].append(elem.find('a').text)
        year_of_model = elem.find('a').text.split()[0]
        brand_name = elem.find('a').text.split()[1]
        data['Year of Model'].append(year_of_model)
        data['Brand Name'].append(brand_name)
        data['Engine'].append(elem.find('div',attrs={'style':'min-height:16px'}).text)
        span_elems = elem.find('div',class_='dotlist truncate').find_all('span')
        data['Kms Driven'].append(span_elems[0].text.split()[0])
        data['Variant'].append(span_elems[1].text)
        data['Transmission Type'].append(span_elems[2].text)
        data['Number of Photos Uploaded'].append(elem.find('div',class_='photoNumber badge').text)
        data['Total Views'].append(elem.find('div',class_='views badge').text)
        data['Price of the Car'].append(elem.find('span',class_='amnt').text)

        

df = pd.DataFrame.from_dict(data)
df.to_csv("data.csv",index = False)
