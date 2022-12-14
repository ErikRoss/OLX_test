import json
import requests
from threading import Thread
from bs4 import BeautifulSoup
from queue import Queue
from flask_socketio import emit

from app import db
from app.models import Ad


class Parser:
    def __init__(self):
        """Init Parser"""
        self.soup = None
        self.ads = []
        self.ads_urls = []
        self.used_urls = []

    @staticmethod
    def get_soup(url):
        """Get soup from url"""
        response = requests.get(url)
        return BeautifulSoup(response.text, 'html.parser')

    def get_ads_from_page(self):
        """Get ads urls from page"""
        ads_urls = []
        for ad in self.soup.find_all('a', class_='css-1bbgabe'):
            ad_url = ad.get('href')
            if ad_url not in self.ads_urls:
                ads_urls.append(ad_url)
                self.ads_urls.append(ad_url)
        return ads_urls

    def collect_ads(self, url, access_level):
        """
        Collect ads data

        :param socket: socketio
        :param url: category url
        :param access_level: access level of current user
        """
        limit = access_level * 100
        threads = []
        page = 1
        i = 0
        while len(self.used_urls) < limit:
            if page != 1:
                url = f'{url}?p={page}'
            self.soup = self.get_soup(url)
            ads_urls = self.get_ads_from_page()
            page += 1
            tasks = Queue()
            for ad_url in ads_urls:
                tasks.put(ad_url)
            for _ in range(5):
                thread = Thread(target=self.collect_ad, args=(tasks,))
                thread.start()
            tasks.join()
            for ad in self.ads:
                if i < limit:
                    ad_item = Ad(ad)
                    db.session.add(ad_item)
                    db.session.commit()
                    ad["id"] = ad_item.id
                    if access_level in [1, 2]:
                        ad["seller"] = ""
                    emit('send ad', json.dumps(ad))
                    i += 1
                else:
                    break
            self.ads.clear()
        print(f"Collected {len(self.used_urls)} ads")

    def collect_ad(self, ad_pages):
        """
        Collect ad data to db and download image

        :param ad_pages: tasks list
        """
        while not ad_pages.empty():
            ad_page = ad_pages.get()
            print(f"Collecting ad {len(self.used_urls) + 1}")
            soup = self.get_soup("https://www.olx.ua/" + ad_page)
            try:
                title = soup.find('h1').text
            except AttributeError:
                ad_pages.task_done()
                return
            try:
                price_value = soup.find('h3').text.split(" ")
            except AttributeError:
                price = None
                currency = None
                print(ad_page)
            else:
                price = "".join(price_value[:-1])
                if price == "":
                    price = None
                else:
                    price = int(float(price))
                currency = price_value[-1]
            try:
                image = soup.find('img', class_='css-1bmvjcs').get('src')
            except AttributeError:
                image_name = None
            else:
                image_name = image.split("/")[-2] + ".jpg"
                with open(f"app/static/img/{image_name}", "wb") as f:
                    f.write(requests.get(image).content)
            ad_params = {
                'title': title,
                'price': price,
                'currency': currency,
                'image': image_name,
                'seller': soup.find('h4').text
            }
            self.used_urls.append(ad_page)
            self.ads.append(ad_params)
            print("Collected")
            ad_pages.task_done()


parser = Parser()


if __name__ == '__main__':
    parser = Parser()
