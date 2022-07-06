from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from orders.models import Copun
import uuid
#from PIL import Image

# Create your models here.

def validate_image(fieldfile_obj):
    filesize = fieldfile_obj.file.size
    megabyte_limit = 5.0
    if filesize > megabyte_limit*1024*1024:
        raise ValidationError("Max file size is %sMB" % str(megabyte_limit))

class Games(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField()
    short_decription = models.TextField(default='')
    price = models.FloatField()
    rating = models.IntegerField(default=5, validators=[MinValueValidator(0), MaxValueValidator(5)])
    copun = models.ForeignKey(Copun, null=True, on_delete=models.SET_NULL)
    main_image = models.ImageField(upload_to='media/images/', null=False, validators=[validate_image,])
    image1 = models.ImageField(upload_to='media/images/', validators=[validate_image,])
    image2 = models.ImageField(upload_to='media/images/', validators=[validate_image,])
    image3 = models.ImageField(upload_to='media/images/', validators=[validate_image])
    image4 = models.ImageField(upload_to='media/images/', validators=[validate_image,])
    # image5 = models.ImageField(upload_to='media/images/', validators=[validate_image,])
    # image6 = models.ImageField(upload_to='media/images/', validators=[validate_image])
    youtube_link = models.CharField(max_length=200, default='')

    def __str__(self):
        return f"{self.name}"


    class Meta:
        db_table = 'games'
        verbose_name_plural = 'GAMES'

class Standard(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = 'standard'
        verbose_name_plural = 'STANDARDS'

class ActivityBox(models.Model):
    # CLASS_CHOICES = [
    #     ('I', 'I'),
    #     ('II', 'II'),
    #     ('III', 'III'),
    #     ('IV', 'IV'),
    #     ('V', 'V'),
    #     ('VI', 'VI'),
    #     ('VII', 'VII')
    # ]
    # DEFAULT_CLASS = 'I'
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField()
    short_decription = models.TextField(default='')
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE)
    price = models.FloatField()
    copun = models.ForeignKey(Copun, null=True, on_delete=models.SET_NULL)
    rating = models.IntegerField(default=5, validators=[MinValueValidator(0), MaxValueValidator(5)])
    main_image = models.ImageField(upload_to='media/images/', null=False, validators=[validate_image,])
    image1 = models.ImageField(upload_to='media/images/', validators=[validate_image,])
    image2 = models.ImageField(upload_to='media/images/', validators=[validate_image,])
    image3 = models.ImageField(upload_to='media/images/', validators=[validate_image])
    image4 = models.ImageField(upload_to='media/images/', validators=[validate_image,])
    # image5 = models.ImageField(upload_to='media/images/', validators=[validate_image,])
    # image6 = models.ImageField(upload_to='media/images/', validators=[validate_image])
    youtube_link = models.CharField(max_length=200, default='')


    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = 'activity_box'
        verbose_name_plural = 'ACTIVITY BOXES'

class SpecialBooks(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField()
    short_decription = models.TextField(default='')
    price = models.FloatField()
    rating = models.IntegerField(default=5, validators=[MinValueValidator(0), MaxValueValidator(5)])
    copun = models.ForeignKey(Copun, null=True, on_delete=models.SET_NULL)
    main_image = models.ImageField(upload_to='media/images/', null=False, validators=[validate_image,])
    image1 = models.ImageField(upload_to='media/images/', validators=[validate_image,])
    image2 = models.ImageField(upload_to='media/images/', validators=[validate_image,])
    image3 = models.ImageField(upload_to='media/images/', validators=[validate_image])
    image4 = models.ImageField(upload_to='media/images/', validators=[validate_image,])
    # image5 = models.ImageField(upload_to='media/images/', validators=[validate_image,])
    # image6 = models.ImageField(upload_to='media/images/', validators=[validate_image])


    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = 'special_books'
        verbose_name_plural = 'SPECIAL BOOKS'

class KnowledgeCapsule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    city_name = models.CharField(max_length=200)
    school_name = models.CharField(max_length=200)
    standard = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = 'knowledge_capsule'
        verbose_name_plural = 'KNOWLEDGE CAPSULES'

class Pricing(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField()

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = 'PRICING'


class APIRazor(models.Model):
    api_key = models.CharField(max_length=200)
    api_secret = models.CharField(max_length=200)

    def __str__(self):
        return "API Credentials"

    class Meta:
        verbose_name_plural = 'API CREDENTIALS'