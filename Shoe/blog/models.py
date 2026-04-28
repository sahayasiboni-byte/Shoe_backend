from django.db import models
from image.models import products

class User(models.Model):
    name=models.CharField(max_length=150)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=10)

    def __str__(self):
        return self.name
    

class AddCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart_items'
    )

    product = models.ForeignKey(
        products,
        on_delete=models.CASCADE,
        related_name='cart_items'
    )

    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user} - {self.product}"