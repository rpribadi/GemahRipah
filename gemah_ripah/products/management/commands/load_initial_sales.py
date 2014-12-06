import csv
import datetime
import glob
import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from products.models import Product
from sales.models import Sales, SalesItem


class Command(BaseCommand):
    help = 'Load initial sales'

    def handle(self, *args, **options):
        filename = "data/initial_sales.csv"
        try:
            self.process(filename)
        except Exception, e:
            raise CommandError('Error saving data from "%s". Reason: %s' % (filename, e))

    def process(self, filename):
        counter = 1

        with open(filename, 'rb') as f:
            reader = csv.reader(f, delimiter=',')

            user = User.objects.get(username="riki")
            sales, is_created = Sales.objects.update_or_create(
                date=datetime.date(2014, 11, 20),
                remarks="Initial Sales",
                modified_by=user
            )

            print "IS_CREATED = ", is_created

            sales.salesitem_set.all().delete()

            for line in reader:
                if not line[1].strip() or not line[2].strip():
                    print "%d. [SKIPPED] %s" % (counter, line[0])
                else:
                    product = Product.objects.get(name=line[0].strip())

                    record = SalesItem(
                        sales=sales,
                        product=product,
                        price=int(float(line[1].strip())),
                        quantity=int(line[2].strip()),
                        modified_by=user
                    )
                    record.save()
                    print "%d. %s" % (counter, record)
                counter += 1

