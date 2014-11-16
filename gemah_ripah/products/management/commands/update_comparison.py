import csv
import datetime
import glob
import os

from django.core.management.base import BaseCommand, CommandError

from products.models import Comparison


class Command(BaseCommand):
    help = 'Updates comparison prices'

    def handle(self, *args, **options):
        directory = "data/comparison/*.csv"
        try:
            for filename in glob.glob(directory):
                print "Reading", filename
                self.process(filename)
        except Exception, e:
            raise CommandError('Error saving data from directory "%s". Reason: %s' % (directory, e))

    def process(self, filename):
        seller = os.path.splitext(os.path.basename(filename))[0]
        today = datetime.datetime.now()
        counter = 1

        with open(filename, 'rb') as f:
            reader = csv.reader(f, delimiter=',')

            for line in reader:
                promotion_price = line[2] if len(line) >= 3 and line[2] else None

                record, is_created = Comparison.objects.get_or_create(
                    seller=seller,
                    product=line[0].strip(),
                    defaults={
                        'price': line[1],
                        'promotion_price': promotion_price,
                        'last_update': today
                    }
                )
                record.save()
                print "%d. %s" % (counter, record)
                counter += 1

