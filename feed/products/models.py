from django.db import models
# Create your models here.

class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now=True)
    modified_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class Category(BaseModel):
    name = models.CharField(max_length=55)

class Product(BaseModel):
    image = models.ImageField(blank=True, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)




