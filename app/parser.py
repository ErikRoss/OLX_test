import re
import requests
from threading import Thread
from sqlalchemy.exc import IntegrityError
from bs4 import BeautifulSoup

from app import db
from app.models import Ad


class Parser:
    def __init__(self, url, limit=100):
        """
        Init Parser

        :param url: category url
        :param limit: limit of ads
        """
        self.category_url = url
        self.limit = limit
        self.soup = None
        self.ads_urls = []
        self.used_urls = []

    def get_soup(self, url=None):
        """Get soup from url"""
        if url is None:
            url = self.category_url
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

    def collect_ads(self):
        """Collect ads data"""
        ads_urls = []
        threads = []
        page = 1
        while len(self.used_urls) < self.limit:
            if page == 1:
                url = self.category_url
            else:
                url = self.category_url + f'?p={page}'
            self.soup = self.get_soup(url)
            ads_urls = self.get_ads_from_page()
            page += 1
            for ad in ads_urls:
                if len(self.used_urls) >= self.limit:
                    break
                threads.append(Thread(target=self.collect_ad, args=(ad,)))
                threads[-1].start()
                print(f"Collecting ad {len(self.used_urls) + 1} of {self.limit}")
            for thread in threads:
                thread.join()
        print(f"Collected {len(self.used_urls)} ads")

    def collect_ad(self, ad_page):
        """
        Collect ad data to db and download image

        :param ad_page: ad page source
        """
        soup = self.get_soup("https://www.olx.ua/" + ad_page)
        title = soup.find('h1').text
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
            currency = price_value[-1]
        try:
            image = soup.find('img', class_='css-1bmvjcs').get('src')
        except AttributeError:
            image_name = None
        else:
            image_name = image.split("/")[-2] + ".jpg"
            with open(f"static/img/{image_name}", "wb") as f:
                f.write(requests.get(image).content)
        ad = {
            'title': title,
            'price': price,
            'currency': currency,
            'image': image_name,
            'seller': soup.find('h4').text
        }
        db.session.add(Ad(ad))
        db.session.commit()
        self.used_urls.append(ad_page)


def main():
    """Collect ads and write to db"""
    parser = Parser('https://www.olx.ua/d/uk/transport/legkovye-avtomobili/')
    parser.collect_ads()


if __name__ == '__main__':
    main()
