from django.shortcuts import render
import markdown2

from django.http import HttpResponseRedirect
from django.urls import reverse

from django import forms

import random

from django import forms

from . import util


class NewEntryForm(forms.Form):
	title = forms.CharField(label = "Enter the title of the Entry here")
	content = forms.CharField(widget=forms.Textarea, label = "Write the Markdown content here")

def index(request):
	if request.method == "GET":
		query = request.GET.get('q')
		if query == None:
			return render(request, "encyclopedia/index.html", {
				"entries": util.list_entries()
				})

		elif query in util.list_entries():
			htmlcon = markdown2.markdown(util.get_entry(query))
			return render(request, "encyclopedia/entry.html",{
				"title": query,
				"content": htmlcon
				})

		else:
			links = []
			ctr = 0
			for ent in util.list_entries():
				if ent.lower().find(query.lower()) >= 0:
					links.append(ent)
					ctr += 1

			if ctr == 0:
				links.append("No results found matching the above query!")

			return render(request, "encyclopedia/searchres.html",{
				"links": links,
				"query": query
				})


def getent(request, entry):
	if entry in util.list_entries():
		htmlcon = markdown2.markdown(util.get_entry(entry))
		return render(request, "encyclopedia/entry.html",{
			"title": entry,
			"content": htmlcon
			})


	else:
		return render(request, "encyclopedia/error.html",{
			"title":"Error 403",
			"content":"Error 403: Requested Page not found!"
			})


def randompage(request):
	rand = random.choice(util.list_entries())
	htmlcon = markdown2.markdown(util.get_entry(rand))
	return render(request, "encyclopedia/entry.html", {
		"title": rand,
		"content": htmlcon
		})

def addentry(request):
	if request.method == "POST":
		form = NewEntryForm(request.POST)
		if form.is_valid():
			newtitle = form.cleaned_data["title"]
			newcontent = form.cleaned_data["content"]
			if newtitle not in util.list_entries():
				util.save_entry(newtitle, newcontent)
				return HttpResponseRedirect(newtitle)

			else:
				return render(request, "encyclopedia/error.html",{
					"title": "Error 404",
					"content": "Error 404: Specified entry already exits!"
					})
		else:
			return render(request, "encyclopedia/addent.html",{
				"form": form
				})

	return render(request, "encyclopedia/addent.html",{
		"form": NewEntryForm()
		})

def editentry(request, entry):

	existing_form = NewEntryForm(initial = {
		'title': entry,
		'content': util.get_entry(entry)
		})
	
	if request.method == "POST":
		form = NewEntryForm(request.POST)
		if form.is_valid():
			newcontent = form.cleaned_data["content"]
			util.save_entry(entry, newcontent)
			return HttpResponseRedirect(f"/wiki/{entry}")

		else:
			return render(request, "encyclopedia/improv_ent.html", {
				"entry": entry,
				"form": form
				})

	return render(request, "encyclopedia/improv_ent.html",{
		"form": existing_form,
		"entry": entry
		})



