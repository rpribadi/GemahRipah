import difflib
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
        try:
            self.process(settings.COMPARISON_URLS['SM'])
        except Exception, e:
            raise CommandError('Error saving data from SM %s. Reason: %s' % (settings.COMPARISON_URLS['SM'], e))

    def process(self, url):
        seller = Merchant.objects.get(code='SM')
        comparison_list = self.read(url)

        product_list = Product.objects.all()

        for index, comparison in enumerate(comparison_list):

            record, is_created = ProductComparison.objects.update_or_create(
                seller=seller,
                name=comparison['name'],
                defaults={
                    'price': comparison['price'],
                    'promotion_price': comparison['promotion_price']
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


    def read(self, url):
        products = []
        page_number = 1
        while True:
            try:
                the_url = "%s/%d" % (url, page_number)
                print "Downloading from %s" % the_url
                page = urlopen(the_url).read()
            except Exception, e:
                break
            else:
                soup = BeautifulSoup(page.decode('utf-8', 'ignore'))
                rows = soup.find_all("div", attrs={"class": "prodbox"})
                if len(rows) <= 0:
                    break

                print "  --> Found %d" % len(rows)
                for index, row in enumerate(rows):
                    row = row.find_all("p")

                    name = row[0].get_text().strip()
                    name = re.sub('[\t\n\r\f\v]+', '', name).strip()
                    name = re.sub('[ ]{2,}', ' ', name).strip()
                    name = name.upper()

                    price = row[1].get_text().replace(".", "").replace(",", "").replace("Rp", "").strip()
                    price = int(price)

                    promotion_price = None
                    if row[2].find("span", class_="pricediscount"):
                        promotion_price = int(row[2].find("span", class_="pricediscount").get_text().replace(".", "").replace(",", "").replace("NOW", "").replace("Rp", "").strip())

                    item = {
                        "name": name,
                        "price": price,
                        "promotion_price": promotion_price
                    }
                    products.append(item)

            page_number += 1

            print "Sleeping..."
            time.sleep(3)

        return products