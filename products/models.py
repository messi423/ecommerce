from django.db import models
from users.models import Profile


class Article(models.Model):
    name = models.CharField(max_length=50)
    in_stock = models.IntegerField()
    price = models.FloatField()
    image = models.ImageField(default='electronic.jpg', upload_to='electronic')
    type = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Order(models.Model):
    ownwer = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    items = models.ManyToManyField(Article)

    def cart_items(self):
        return self.items.all()

    def cart_total(self):
        return sum([item.price for item in self.items.all()])