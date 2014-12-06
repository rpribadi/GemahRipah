import difflib
import json
import re

from bs4 import BeautifulSoup

from products.models import Product, ProductComparison

SAME_ITEM_MIN_RATIO = 0.98


def check_ratio(item, product_list):
    for product in product_list:
        if difflib.SequenceMatcher(None, item.name, product.name).ratio() >= SAME_ITEM_MIN_RATIO:
            item.product = product
            break
    return item


def parse_RS(seller, raw_json):
    product_list = Product.objects.all()

    data = json.loads(raw_json)["result_html"]
    soup = BeautifulSoup(data, 'html.parser')
    rows = soup.find_all("div", recursive=False)

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

        obj, is_created = ProductComparison.objects.update_or_create(
            seller=seller,
            name=name,
            defaults={
                'price': price,
                'promotion_price': promotion_price
            }
        )

        obj = check_ratio(obj, product_list)
        obj.save()
        print "%d. [%s] %s" % (index+1, is_created, obj.name)


def parse_HP(seller, raw_json):
    product_list = Product.objects.all()

    rows = json.loads(raw_json)['items']

    print "  --> Found %d" % len(rows)

    for index, row in enumerate(rows):
        price = float(row['product_price'].replace(".", "").strip())

        promotion_price = row.get('promotion_price', None)
        if promotion_price:
            promotion_price = float(promotion_price.replace(".", "").strip())

        name = re.sub("\s*\(.*\)\**", "", row['product_name'].upper()).strip()


        obj, is_created = ProductComparison.objects.update_or_create(
            seller=seller,
            name=name,
            defaults={
                'price': price,
                'promotion_price': promotion_price
            }
        )

        obj = check_ratio(obj, product_list)
        obj.save()
        print "%d. [%s] %s" % (index+1, is_created, obj.name)

