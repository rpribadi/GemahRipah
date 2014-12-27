import datetime
import difflib
import re
import time

from urllib2 import urlopen
from bs4 import BeautifulSoup

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from products.models import Merchant, Product, ProductComparison

SAME_ITEM_THRESHOLD = 0.965

class Command(BaseCommand):
    help = 'Updates comparison prices'

    def handle(self, *args, **options):
        for url in settings.COMPARISON_URLS['RS']:
            try:
                self.process(url)
            except Exception, e:
                raise CommandError('Error saving data from RS %s. Reason: %s' % (url, e))
            finally:
                print "Sleeping..."
                time.sleep(2)

    def process(self, url):
        seller = Merchant.objects.get(code='RS')
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
                if ratio >= SAME_ITEM_THRESHOLD:
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
                the_url = "%s&page=%d" % (url, page_number)
                print "Downloading from %s" % the_url
                page = urlopen(the_url).read()
            except Exception, e:
                print "Exception: ", e
                break
            else:
                soup = BeautifulSoup(page.decode('utf-8', 'ignore'), 'html.parser')
                table = soup.find("div", class_="product-list")
                if not table:
                    print "  --> Empty"
                    break

                rows = table.find_all("div", recursive=False)
                print "  --> Found %d" % len(rows)

                for index, row in enumerate(rows):
                    name = row.find(class_="name").get_text().strip()
                    name = name.upper().replace("GR.","GR").strip()
                    name = re.sub(" \*.*\*", "", name.upper()).strip()

                    if row.find(class_="price-old"):
                        price = row.find(class_="price-old").get_text().strip()
                        promotion_price = row.find(class_="price-new").get_text().strip()
                    else:
                        price = row.find(class_="price").get_text().strip()
                        promotion_price = None

                    price = float(price.replace("Rp", "").replace(".", ""))
                    if promotion_price:
                        promotion_price = float(promotion_price.replace("Rp", "").replace(".", ""))

                    item = {
                        'name': name,
                        'price': price,
                        'promotion_price': promotion_price
                    }

                    products.append(item)
            page_number += 1

        return products