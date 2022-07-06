from django.db import models
# from django.contrib.auth.models import User
from users.models import Address
from django.contrib.auth.models import User

# Create your models here.
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
# from datetime import datetime
from django.utils.timezone import now
import uuid

def generate_id():
    return str(uuid.uuid4().int)

def is_past_due(value):
    if now().date() > value:
        return True
    return False

def negative_date(value):
    if is_past_due(value):
        raise ValidationError('day cant be in past')

# Create your models here.
class Copun(models.Model):
    code = models.CharField(max_length=100, unique=True)
    percentage = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    expire_date = models.DateField(validators=[negative_date])
    status = models.BooleanField(default=False)
    is_combo = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.code}"

    class Meta:
        db_table = 'copuns'
        verbose_name = 'COUPON'
        verbose_name_plural = 'COUPONS'



class Order(models.Model):
    timestamp = models.DateTimeField(default=now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_id = models.CharField(max_length=64, default=generate_id, unique=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='orders')
    copun = models.ForeignKey(Copun, on_delete=models.SET_NULL, null=True, related_name='orders')
    is_processed = models.BooleanField(default=False)
    total = models.FloatField(default=0)
    razor_pay = models.CharField(max_length=100, default='')

    cod = models.BooleanField(default=False)

    class Meta:
        db_table = 'order'
        verbose_name_plural = 'ORDERS'


class OrderItem(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    price = models.FloatField()
    quantity = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    image = models.CharField(max_length=1000, default='')

    class Meta:
        db_table = 'order_item'
        verbose_name_plural = 'ORDER ITEMS'
