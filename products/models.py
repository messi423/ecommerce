from django.db import models
from users.models import Profile
from django.contrib.auth.models import User

ProductChoices = (
    ('e', 'Electronic'),
    ('uw', 'Upperwear'),
    ('lw', 'Lowerwear')
)


class Article(models.Model):
    name = models.CharField(max_length=50)
    in_stock = models.IntegerField()
    price = models.FloatField()
    image = models.ImageField(default='electronic.jpg', upload_to='electronic')
    type = models.CharField(choices=ProductChoices, max_length=10)

    def __str__(self):
        return self.name


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    stripe_charge_id = models.CharField(max_length=50, default=" ")

    def __str__(self):
        return self.user.username


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address1 = models.TextField()
    address2 = models.TextField()
    zip = models.CharField(max_length=20)
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username


class Order(models.Model):

    ownwer = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    items = models.ManyToManyField(Article)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    def cart_items(self):
        return self.items.all()

    def cart_total(self):
        return sum([item.price for item in self.items.all()])


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"

