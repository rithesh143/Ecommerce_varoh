from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import random

def generate_otp():
    return random.randint(1000, 2000)


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='address_list')
    full_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    pin_code = models.IntegerField()
    house = models.CharField(max_length=500)
    area = models.CharField(max_length=500)
    landmark = models.CharField(max_length=500)
    town = models.CharField(max_length=500)
    state = models.CharField(max_length=200)

    @property
    def addr_str(self):
        return f"""
        <hr/>
            <p>{self.full_name}</p>
            <p>Phone:{self.phone}</p>
            <p>Pin:{self.pin_code}</p>
            <p>House:{self.house}</p>
            <p>Area:{self.area}</p>
            <p>Landmark:{self.landmark}</p>
            <p>Town:{self.town}</p>
            <p>State:{self.state}</p>
        <hr/>
        """

    @property
    def addr_str_(self):
        return f"""
            Pin:{self.pin_code}
            House:{self.house}
            Area:{self.area}
            Landmark:{self.landmark}
            Town:{self.town}
            State:{self.state}
        """

    def __str__(self):
        return f"{self.addr_str_}"

    class Meta:
        verbose_name_plural = 'ADDRESS'


class ContactUs(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    subject = models.CharField(max_length=200)
    message = models.TextField()

    class Meta:
        verbose_name_plural = 'CONTACT US'

    def __str__(self):
        return f"{self.name}[{self.subject}]"

# Create your models here.
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)