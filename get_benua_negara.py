import requests
from bs4 import BeautifulSoup
list_benua = []
list_negara = []
url = 'https://id.wikipedia.org/wiki/Kategori:Daftar_kota_menurut_negara'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
# soup = soup.find(id='content')
soup = soup.find(id='bodyContent')
soup = soup.find('table')
for item in soup.find_all(['th','li']):
    if item.name == 'th':
        list_benua.append(item.getText())
    else:
        list_negara.append(item.getText())
list_benua  = list_benua[1:]
list_negara = list_negara[3:]
print("list_benua :",list_benua)
print("list_negara :",list_negara)