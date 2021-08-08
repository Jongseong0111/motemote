from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "products"

class Category(models.Model):
    product = models.ForeignKey("Product", on_delete = models.CASCADE)
    name    = models.CharField(max_length=100)

    class Meta:
        db_table = "categories"


class Concept(models.Model):
    name     = models.CharField(max_length=100)
    content  = models.TextField(default='')

    class Meta:
        db_table = "concepts"    


class Item(models.Model):
    concept        = models.ForeignKey("Concept", on_delete=models.CASCADE)
    color          = models.ForeignKey("Color", on_delete=models.CASCADE, null=True)
    option         = models.ForeignKey("Option", on_delete=models.CASCADE, null=True)
    name           = models.CharField(max_length=100)
    price          = models.DecimalField(max_digits=10, decimal_places=2)
    discount       = models.DecimalField(max_digits=10, decimal_places=2)
    stock          = models.IntegerField(default=0)
    order_quantity = models.IntegerField(default=0)
    category       = models.ForeignKey("Category", on_delete=models.CASCADE)

    class Meta:
        db_table = "items"


class Color(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "colors"  


class Option(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "options"  


class Image(models.Model):
    item      = models.ForeignKey("Item", on_delete=models.CASCADE)
    image_url = models.CharField(max_length=500)
    main      = models.BooleanField(default=False)

    class Meta:
        db_table = "images"  

