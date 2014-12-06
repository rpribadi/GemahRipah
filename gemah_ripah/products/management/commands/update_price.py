import csv
import datetime
import glob
import os

from django.core.management.base import BaseCommand, CommandError

from products.models import Product


class Command(BaseCommand):
    help = 'Updates product prices'

    def handle(self, *args, **options):
        filename = "data/product.csv"
        try:
            self.process(filename)
        except Exception, e:
            raise CommandError('Error saving data from "%s". Reason: %s' % (filename, e))

    def process(self, filename):
        counter = 1

        with open(filename, 'rb') as f:
            reader = csv.reader(f, delimiter=',')

            for line in reader:

                record, is_created = Product.objects.update_or_create(
                    brand=line[0].strip(),
                    name=line[1].strip(),
                    defaults={
                        'price': line[2] if line[2] else 0,
                    }
                )
                record.save()
                print "%d. %s" % (counter, record)
                counter += 1

