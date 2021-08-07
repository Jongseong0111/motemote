from django.db import models

class Order(models.Model):
    member   = models.ForeignKey("users.Member", on_delete=models.CASCADE)
    status   = models.ForeignKey("Status", on_delete=models.CASCADE)
    location = models.ForeignKey("Location", on_delete=models.CASCADE, null=True)
    order_at = models.DateField(auto_now_add=True)

    class Meta:
        db_table = "orders"


class Location(models.Model):
    name         = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=200)
    email        = models.CharField(max_length=200, null=True)
    address      = models.CharField(max_length=500)
    content      = models.TextField(null=True)

    class Meta:
        db_table = "locations"


class OrderItem(models.Model):
    item              = models.ForeignKey("products.Item", on_delete=models.CASCADE)
    order             = models.ForeignKey("Order", on_delete=models.CASCADE)
    order_item_status = models.ForeignKey("OrderItemStatus", on_delete=models.CASCADE)
    quantity          = models.IntegerField()

    class Meta:
        db_table = "orderitems"


class Cart(models.Model):
    member   = models.ForeignKey("users.Member", on_delete=models.CASCADE)
    item     = models.ForeignKey("products.Item", on_delete=models.CASCADE)
    quantity = models.IntegerField()
    
    class Meta:
        db_table = "carts"  


class OrderItemStatus(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "order_item_statuses"  


class Status(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "statuses"  