import csv
import datetime
import glob
import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from merchants.models import Merchant
from products.models import Product
from purchase.models import Purchase, PurchaseItem


class Command(BaseCommand):
    help = 'Load initial purchase'

    def handle(self, *args, **options):
        filename = "data/initial_purchase.csv"
        try:
            self.process(filename)
        except Exception, e:
            raise CommandError('Error saving data from "%s". Reason: %s' % (filename, e))

    def process(self, filename):
        counter = 1

        with open(filename, 'rb') as f:
            reader = csv.reader(f, delimiter=',')

            user = User.objects.get(username="riki")
            supplier = Merchant.objects.get(code="LK")
            purchase, is_created = Purchase.objects.get_or_create(
                date=datetime.date(2014, 10, 13),
                supplier=supplier,
                remarks="Initial Purchase",
                modified_by=user
            )

            print "IS_CREATED = ", is_created

            purchase.purchaseitem_set.all().delete()

            for line in reader:
                if not line[1].strip() or not line[2].strip():
                    print "%d. [SKIPPED] %s" % (counter, line[0])
                else:
                    product = Product.objects.get(name=line[0].strip())

                    record = PurchaseItem(
                        purchase=purchase,
                        product=product,
                        price=int(float(line[1].strip())),
                        quantity=int(line[2].strip()),
                        modified_by=user
                    )
                    record.save()
                    print "%d. %s" % (counter, record)
                counter += 1

