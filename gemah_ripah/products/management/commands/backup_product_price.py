import csv
import datetime
import glob
import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail, EmailMessage

from products.models import Product


class Command(BaseCommand):
    help = 'Send backup product price'

    def handle(self, *args, **options):
        try:
            self.process()
        except Exception, e:
            raise CommandError('Error sending backup product price. Reason: %s' % (e, ))

    def process(self):
        now = datetime.datetime.now()
        subject = "Product Price Per %s" % now
        sender = "GemahRipah.net <shop@gemahripah.net>"
        recipients = ["pribadi.riki@gmail.com", "ulnita.prihastie@gmail.com"]
        message = "Please find the attachment for the latest product price.\n\nRegards,\nGemah Ripah"
        attachment = "product-%s.csv" % now.strftime("%d-%b-%Y")

        import csv
        with open(attachment, 'wb') as f:
            writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_ALL)

            writer.writerow(['PRODUCT', 'BUY PRICE', 'SELL PRICE', 'MARGIN', 'STOCK'])

            for product in Product.objects.filter(is_active=True):
                if product.purchaseitem_set.all().count():
                    product.buy_price = product.purchaseitem_set.all()[0].price
                    product.margin = product.price - product.buy_price
                else:
                    product.buy_price = "-"
                    product.margin = "-"
                writer.writerow([product.name, product.buy_price, product.price, product.margin, product.stock])

        email = EmailMessage(
            subject,
            message,
            sender,
            recipients,
            [],
            headers={'Reply-To': 'shop@gemahripah.net'}
        )

        with open(attachment) as f:
            email.attach(attachment, f.read(), 'text/plain')

        email.send()