from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ModelForm


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"


class Categories(models.Model):
    name = models.CharField(max_length=20, primary_key=True)

    def __str__(self):
        return f"{self.name}" 


class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name='listings', null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    current_price = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True)

    def __str__(self):
            return f"{self.title} : {self.category}"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} -> {self.listing}"


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids', null=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bids')
    amount = models.IntegerField()

    def __str__(self):
        return f"{self.user}: {self.amount} -> {self.listing}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()  
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} : {self.content}"
