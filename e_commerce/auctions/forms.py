from django.db import models
from django.forms import ModelForm

from .models import *


class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'category', 'image_url', 'current_price']
    
    def __init__(self, *args, **kwargs):
        super(ListingForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']
    
    def __init__(self, *args, **kwargs):
        super(BidForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
    
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['border-radius'] = '10px'
            visible.field.widget.attrs['placeholder'] = 'Comment Here'