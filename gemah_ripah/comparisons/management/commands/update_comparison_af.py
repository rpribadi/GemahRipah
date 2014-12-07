import datetime
import difflib
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
        for url in settings.COMPARISON_URLS['AF']:
            try:
                self.process(url)
            except Exception, e:
                raise CommandError('Error saving data from AF %s. Reason: %s' % (url, e))
            finally:
                print "Sleeping..."
                time.sleep(5)

    def process(self, url):
        seller = Merchant.objects.get(code='AF')
        today = datetime.datetime.now()
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

            record.save()
            print "%d. [%s] %s" % (index+1, is_created, record)

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
                rows = soup.find('ul', class_='product_gallery').find_all("div", class_="product_detail")

                print "  --> Found %d" % len(rows)
                for index, row in enumerate(rows):
                    name = row.find('div', class_='product_title').get_text().strip()
                    name = name.replace("\n", "").strip().upper()

                    if row.find('span', class_='product_price_promo'):
                        price = row.find('span', class_='product_price_promo').get_text().replace(".", "").replace("Rp", "").strip()
                        promotion_price = row.find('div', class_='product_price').get_text().replace(".", "").replace("Rp", "").replace(price, "").strip()
                    else:
                        price = row.find('div', class_='product_price').get_text().replace(".", "").replace("Rp", "").strip()
                        promotion_price = 0

                    price = int(price)
                    promotion_price = int(promotion_price) if promotion_price else None

                    item = {
                        "name": name,
                        "promotion_price": promotion_price,
                        "price": price
                    }
                    products.append(item)

            pagination_links = soup.find("div", class_="paginationControl")
            if not pagination_links:
                break

            pager = []
            for item in pagination_links.find_all("a"):
                try:
                    pager.append(int(item.get('href').split("/")[-1]))
                except:
                    pass
            if not pager:
                break

            max_page_number = max(pager)
            page_number += 1

            if page_number > max_page_number:
                break

        return products