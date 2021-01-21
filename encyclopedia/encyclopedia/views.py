from django.shortcuts import render, redirect
from django.contrib import messages
from markdown2 import markdown
from django import forms
from random import randint
from . import util


class NewPageForm(forms.Form):
    title = forms.CharField()
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder' : 'Enter Content Here (In Markdown)'}))


class ExistingPageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def page(request, title):
    try:
        entry = util.get_entry(title)
        return render(request, "encyclopedia/display.html", {
            "title": title.capitalize,
            "html_body": markdown(entry)
        })
    except TypeError:
        return render(request, "encyclopedia/error.html", {
            "title": title
        })


def create_page(request):
    if request.method == 'POST':
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            if util.get_entry(title) == None:
                content = form.cleaned_data["content"]
                util.save_entry(title, content)
                return redirect('encyclopedia:page', title=title) # REDIRECT to new page
            else:
                messages.info(request, 'Entry with this TITLE already exists!') 
                return render(request, "encyclopedia/create.html", {
                    "form": form
                }) 
        else:
            # To ensure server side validation 
            return render(request, "encyclopedia/create.html", {
                "form": form
            })
    return render(request, 'encyclopedia/create.html', {
        "form": NewPageForm()
    }) 


def edit_page(request, title):
    if request.method == 'POST':
        form = ExistingPageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return redirect('encyclopedia:page', title=title) # REDIRECT to new page
        else:
            # To ensure server side validation 
            return render(request, "encyclopedia/edit.html", {
                "title": title.capitalize,
                "form": form
            })
    initial_data = {
        'content' : util.get_entry(title)
    }
    return render(request, 'encyclopedia/edit.html', {
        "title": title.capitalize,
        "form": ExistingPageForm(initial=initial_data)
    })


def search_results(request):
    if request.method == 'POST':
        entries = util.list_entries()
        search_query = request.POST.get('q')
        matches = []
        for entry in entries:
            if search_query.lower() == entry.lower():
                return redirect('encyclopedia:page', title=entry) # REDIRECT to new page
            elif search_query.lower() in entry.lower():
                matches.append(entry)

        if matches:
            return render(request, 'encyclopedia/search_results.html', {
                'entries': matches
            })
        else:
            return render(request, 'encyclopedia/no_results.html', {
                'search_query': search_query
            })


def random_page(request):
    entries = util.list_entries()
    random_index = randint(0, len(entries) - 1)
    return redirect('encyclopedia:page', entries[random_index])
