import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "motemote.settings")
django.setup()

from products.models import *
from users.models import *

# CSV_PATH_PRODUCTS = './category.csv'

# with open(CSV_PATH_PRODUCTS) as in_file:
#     data_reader = csv.reader(in_file)
#     next(data_reader, None)
#     for row in data_reader:
#         if row[0]:
#             product = Product.objects.create(name = row[0])
#         if row[1]:
#             Category.objects.create(name = row[1], product_id = product.id)

# CSV_PATH_PRODUCTS = './concept.csv'

# with open(CSV_PATH_PRODUCTS) as in_file:
#     data_reader = csv.reader(in_file)
#     next(data_reader, None)
#     for row in data_reader:
#         Concept.objects.create(name = row[0], content = row[1])

# CSV_PATH_PRODUCTS = './color.csv'

# with open(CSV_PATH_PRODUCTS) as in_file:
#     data_reader = csv.reader(in_file)
#     next(data_reader, None)
#     for row in data_reader:
#         if row[0]:
#             Color.objects.create(name = row[0])
#         if row[1]:
#             Option.objects.create(name=row[1])

# CSV_PATH_PRODUCTS = './item.csv'

# with open(CSV_PATH_PRODUCTS) as in_file:
#     data_reader = csv.reader(in_file)
#     next(data_reader, None)
#     for row in data_reader:
#         Item.objects.create(category_id = row[0], concept_id = row[1], option_id = row[2], color_id = row[3], name = row[4], price = row[5], discount = row[6], stock = row[7], order_quantity = row[8])


# CSV_PATH_PRODUCTS = './image.csv'

# with open(CSV_PATH_PRODUCTS) as in_file:
#     data_reader = csv.reader(in_file)
#     next(data_reader, None)
#     for row in data_reader:
#         Image.objects.create(item_id = row[0], image_url=row[1], main = row[2])

CSV_PATH_PRODUCTS = './member.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        Member.objects.create(account = row[0], password = row[1], name = row[2], email=row[3], phone_number="0"+str(row[4]), address=row[5])

          

