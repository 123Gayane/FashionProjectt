from django.db import models
from django.contrib.auth.models import User


class Fashion(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    size = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField()
    email = models.EmailField(max_length=254, blank=True, null=True)
    number = models.CharField(max_length=35, blank=True, null=True)

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name


class Trend(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Outfit(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Fashion2(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='fashion_images/', null=True, blank=True)

    def __str__(self):
        return self.name

