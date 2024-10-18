from django.db import models

# Create your models here.
class InfoProduct(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    tig_id = models.CharField(max_length=20, blank=True, default='')
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, default='')
    category = models.IntegerField(default=-1)
    price = models.FloatField(default=0.0)
    unit = models.CharField(max_length=20, blank=True, default='')
    availability = models.BooleanField(default=True)
    sale = models.BooleanField(default=False)
    discount = models.FloatField(default=0.0)
    comments = models.CharField(max_length=100, blank=True, default='')
    owner = models.CharField(max_length=20, blank=True, default='tig_orig')
    quantityInStock = models.IntegerField(default='0')

    class Meta:
        ordering = ('name',)

class Transaction(models.Model):

    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    is_purchase = models.BooleanField()  # True for purchase, False for sale
    product = models.ForeignKey(InfoProduct, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-date',)