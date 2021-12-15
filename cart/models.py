from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import tree
from store.models import Product, Variation
# Create your models here.

class Cart(models.Model):
    cart_id  = models.CharField(max_length=250, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=CASCADE)
    variation = models.ManyToManyField(Variation, blank=True)
    cart = models.ForeignKey(Cart, on_delete=CASCADE)
    quamtity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quamtity

    def __unicode__(self):
        return self.product
