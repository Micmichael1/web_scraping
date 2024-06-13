import requests
from bs4 import BeautifulSoup
import csv
import os

class Scraping:

    # Empty variable
    list_kota = []
    link_kotor = []
    link_bersih = []
    combine_kota_link = []

    def __init__(self,url):
        # Send an HTTP GET request to the URL
        self.url = url
        self.response = requests.get(url)
        self.check_response()

    def check_response(self):
        # Check if the request was successful (status code 200)
        if(self.response.status_code == 200):
            self.start_scarp()
        else:
            print('Failed to fetch the page:', self.response.status_code)

    def start_scarp(self):
        # Parse the HTML content of the page using BeautifulSoup
        self.soup = BeautifulSoup(self.response.content, 'html.parser')
        # Find the main content of the page (usually within <div id="content"> or <div class="mw-parser-output">)
        self.content = self.soup.find(id='bodyContent')  # You may need to inspect the page source to find the appropriate element
        # Find the second table
        # self.table = self.content.find('table', class_='nowraplinks mw-collapsible autocollapsed navbox-inner')
        self.table = self.content.find('table', class_='wikitable sortable')
        # Find the kota content from the second table
        # self.kota = self.table.find_all('li')
        self.kota = self.table.find_all('td')
        self.kota = self.kota[3::9]
        # Load kota content from table
        self.kota_content_loading()
        # Load kota link content from table
        self.link_content_loading()
        # Zip kota dan link into dict
        self.zip_kota_link()
        # write to CSV
        self.write_to_csv()

    def kota_content_loading(self):
        # clean code untuk kota
        for i in self.kota:
            self.link_kotor.append(i.find_all('a', href=True))
            if i.text != "\n":
                self.list_kota.append(i.text)
            # print(i.text)
        self.list_kota = self.list_kota[3:]

    def link_content_loading(self):
        # clean code untuk link
        # print(link_kotor[0][0]['href'])
        for satu in self.link_kotor:
            # print(satu)
            for dua in satu:
                # print(dua)
                self.link_bersih.append("https://id.wikipedia.org/" + dua['href'])
        self.link_bersih = self.link_bersih[3:]

    def zip_kota_link(self):
        self.dict_kota_dan_link = dict(zip(self.list_kota, self.link_bersih))
        for i in self.dict_kota_dan_link:
            dummy = []
            dummy.append(i)
            dummy.append(self.dict_kota_dan_link[i])
            self.combine_kota_link.append(dummy)

    def write_to_csv(self):
        fields = ['kota', 'link']

        with open('kota_link.csv', 'a', newline='') as f:
            # using csv.writer method from CSV package
            write = csv.writer(f)
            # check if file exist and if it need header
            if (os.path.exists('kota_link.csv') and os.path.getsize('kota_link.csv') == 0):
                write.writerow(fields)  # Write header
                print('tulis header')
            write.writerows(self.combine_kota_link)

# It Allows You to Execute Code When the File Runs as a Script, but Not When It’s Imported as a Module
if __name__ == "__main__":
    # Define the URL of the Wikipedia page you want to scrape
    url = 'https://id.wikipedia.org/wiki/Daftar_kota_di_Indonesia'
    # Instance Scraping class
    scrap = Scraping(url)
    print(scrap.combine_kota_link)




