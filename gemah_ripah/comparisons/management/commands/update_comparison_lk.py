import datetime
import difflib
import re

from urllib2 import urlopen
from bs4 import BeautifulSoup

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from products.models import Merchant, Product, ProductComparison

SAME_ITEM_THRESHOLD = 0.975


class Command(BaseCommand):
    help = 'Updates comparison prices'

    def handle(self, *args, **options):
        try:
            self.process(settings.COMPARISON_URLS['LK'])
        except Exception, e:
            raise CommandError('Error saving data from LK. Reason: %s' % (e, ))

    def process(self, url):
        seller = Merchant.objects.get(code='LK')
        today = datetime.datetime.now()
        comparison_list = self.read(url)

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
                if ratio >= SAME_ITEM_THRESHOLD:
                    record.product = product
                    break

            record.save()
            print "%d. [%s] %s %s" % (index+1, is_created, record.name, record.price)
            pass


    def read(self, url):
        products = []
        try:
            print "Downloading from %s" % url
            page = urlopen(url).read()
        except Exception, e:
            raise e
        else:
            soup = BeautifulSoup(page.decode('utf-8', 'ignore'))
            rows = soup.find_all("tr")

            print "  --> Found %d" % len(rows)
            for index, row in enumerate(rows):
                cols = row.find_all("td")
                if index >= 2 and cols[0].get_text().strip():
                    name = "%s %s" % (cols[2].get_text().strip(), cols[3].get_text().strip())
                    name = name.strip().upper()
                    name = re.sub('[\t\n\r\f\v]+', '', name).strip()
                    name = re.sub('[ ]{2,}', ' ', name).strip()

                    price = int(float(cols[5].get_text().replace(",", "").strip()))

                    item = {
                        "name": name,
                        "price": price
                    }
                    products.append(item)

        return products