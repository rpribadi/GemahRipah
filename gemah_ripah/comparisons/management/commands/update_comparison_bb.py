import csv
import difflib
import httplib
import re
import time

from urllib2 import urlopen
from bs4 import BeautifulSoup

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from products.models import Merchant, Product, ProductComparison

SAME_ITEM_THRESHOLD = 0.97

class Command(BaseCommand):
    help = 'Updates comparison prices'

    def handle(self, *args, **options):
        for url in settings.COMPARISON_URLS['BB']:
            try:
                self.process(url)
            except Exception, e:
                raise CommandError('Error saving data from BB %s. Reason: %s' % (url, e))

    def process(self, url):
        comparison_list = self.read(url)

        with open('BB.csv', 'w') as f:
            writer = csv.writer(
                f, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL
            )
            for item in comparison_list:
                writer.writerow([
                    item['name'],
                    item['price']
                ])

        """
        seller = Merchant.objects.get(code='BB')
        product_list = Product.objects.all()

        for index, comparison in enumerate(comparison_list):

            record, is_created = ProductComparison.objects.update_or_create(
                seller=seller,
                name=comparison['name'],
                defaults={
                    'price': comparison['price']
                }
            )

            for product in product_list:
                ratio = difflib.SequenceMatcher(None, product.name, record.name).ratio()
                if ratio > SAME_ITEM_THRESHOLD:
                    record.product = product
                    break
                ratio = 0

            record.save()
            print "%d. [%s] %s: %s" % (index+1, is_created, record, ratio)

            pass


        """


    def read(self, url):

        products = []
        page_number = 0
        while True:
            html = None
            try:
                the_host = url.split("/")[0]
                the_host = the_host.replace("/", "")

                the_url = "%s%d" % ("/".join(url.split("/")[1:]), page_number)
                print "Downloading from %s" % the_url
                conn = httplib.HTTPSConnection(the_host)
                conn.request('GET', "/%s" % the_url)
                response = conn.getresponse()
                html = response.read()
            except Exception, e:
                raise e
            else:
                soup = BeautifulSoup(html)
                rows = soup.find_all("div", class_="product-detail")
                print len(rows)
                if len(rows) <= 0:
                    break

                print "  --> Found %d" % len(rows)
                for index, row in enumerate(rows):
                    name = row.find('div', class_='product-title').get_text().strip()
                    name = re.sub('[\t\n\r\f\v]+', '', name).strip()
                    name = re.sub('[ ]{2,}', ' ', name).strip()
                    name = name.upper()

                    price = row.find('span', class_='new-price-text').get_text().replace(".", "").replace(",", "").replace("Rp ", "").strip()
                    price = int(price)

                    print name, price
                    item = {
                        "name": name,
                        "price": price,
                    }
                    products.append(item)

            page_number += 24

            print "Sleeping..."
            time.sleep(3)

        return products