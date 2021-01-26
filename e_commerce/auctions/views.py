from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from .models import *
from .forms import *


def index(request):
    return render(request, "auctions/index.html", {
        'listings': Listing.objects.all() 
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create_listing(request, username):
    user = User.objects.get(username=username)
    f = ListingForm()
    if request.method == 'POST':
        f = ListingForm(request.POST)
        if f.is_valid():
            listing = f.save(commit=False)
            listing.user = user
            listing.save()
            return redirect("listings", id=listing.id, username=user.username)
        else:
            return render(request, "auctions/create_listing.html", {
            'form': f
        })
    
    else:
        return render(request, "auctions/create_listing.html", {
            'form': f
        })


def display_listing(request, id, username):
    listing = Listing.objects.get(pk=id)
    print(listing.winner)
    if listing.winner != None:
        message = 'This bid is closed'
        if username != '#':
            user = User.objects.get(username=username)
            if user == listing.winner:
                message = 'Congratulations! You won this bid :)'
        context = {
            'listing': listing, 
            'button_title': get_watchlist_button(id, username),
            'message': message,
            'comment_form': CommentForm(),
            'comments': listing.comments.all().reverse()
        } 
    else:
        context = {
            'listing': listing, 
            'bid_form': BidForm(), 
            'button_title': get_watchlist_button(id, username),
            'comment_form': CommentForm(),
            'comments': listing.comments.all().reverse()
        }
        if username != '#':
            user = User.objects.get(username=username)
            if user == listing.user:
                context['close_button'] = 'Close Bid'
            if request.method == 'POST':
                bid_form = BidForm(request.POST)
                bid = bid_form.save(commit=False)
                if bid_form.is_valid() and bid.amount > listing.current_price:
                    bid.listing = listing
                    bid.user = user
                    bid.save()
                    listing.current_price = bid.amount
                    listing.save()
                    context['message'] = 'Bid recorded successfully!'
                else:
                    context['message'] = 'Your bid amount must be more than current bid!'
                    context['bid_form'] = bid_form
                
    return render(request, "auctions/listing.html", context)


def edit_watchlist(request, id, username):
    user = User.objects.get(username=username)
    listing = Listing.objects.get(pk=id)
    item = Watchlist()
    item.user = user
    item.listing = listing
    if get_watchlist_button(id, username) == 'Add to Watchlist':
        item.save()
    else:
       Watchlist.objects.get(user=user, listing=listing).delete()
    return redirect("listings", id=listing.id, username=username)
  

def display_watchlist(request, username):
    user = User.objects.get(username=username)
    watchlist = user.watchlist.all()
    listings = []
    for item in watchlist:
        listings.append(item.listing)

    return render(request, "auctions/watchlist.html", {
        'listings': listings
    })


def categories(request, name):
    if name == '#':
        categories = Categories.objects.all()
        return render(request, "auctions/all_categories.html", {
            'categories': categories
        })
    else:
        category = Categories.objects.get(name=name)
        return render(request, "auctions/category_listings.html", {
            'name': category.name,
            'listings': category.listings.all()
        })


def close_listing(request, id, username):
    listing = Listing.objects.get(pk=id)
    user = User.objects.get(username=username)
    bids = listing.bids.all()
    max_bid = bids[0]
    print(max_bid)
    for bid in bids:
        if bid.amount > max_bid.amount:
            max_bid = bid
    listing.winner = max_bid.user
    listing.save()
    print(listing.winner)
    return redirect("listings", id=listing.id, username=username)


def add_comment(request, id, username):
    listing = Listing.objects.get(pk=id)
    user = User.objects.get(username=username)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        comment = comment_form.save(commit=False)
    comment.user = user
    comment.listing = listing
    comment.save()
    return redirect("listings", id=listing.id, username=username)


def get_watchlist_button(id, username):
    if username != '#':
        user = User.objects.get(username=username)
        listing = Listing.objects.get(pk=id)
        watchlist = user.watchlist.all()

        for item in watchlist:
            if listing == item.listing:
                return 'Remove from Watchlist'
    
    return 'Add to Watchlist'