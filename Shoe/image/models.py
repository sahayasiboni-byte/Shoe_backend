from django.db import models

# Create your models here.

class img(models.Model):
    image=models.ImageField(upload_to='image/',null=True,blank=True)
    categories=models.CharField(max_length=150)

    def __str__(self):
        return self.categories
    

class products(models.Model):
    productimage = models.ImageField(upload_to='image/', null=True, blank=True)
    productname = models.CharField(max_length=100)
    currentprice = models.IntegerField()
    previousprice = models.IntegerField()
    descripe = models.CharField(max_length=300)
    count = models.FloatField()
    categorie = models.ForeignKey(
        img,
        on_delete=models.CASCADE,
        related_name='categorie'
    )

    def __str__(self):
        return self.productname
    
