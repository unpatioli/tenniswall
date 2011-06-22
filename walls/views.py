# Create your views here.
from bson.objectid import ObjectId
from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, redirect
from pymongo.connection import Connection
from walls import forms

db = Connection().tenniswall

def index(request):
    return render(request, 'walls/index.html')

def show(request, wall_id):
    wall = db.walls.find_one(ObjectId(wall_id))
    if wall:
        return render(request, 'walls/show.html', {'wall': wall})
    else:
        raise Http404

def add(request):
    if request.method == 'POST':
        form = forms.AddWallForm(request.POST)
        if form.is_valid():
            wall = form.cleaned_data
            wall_id = db.walls.insert(wall)
            messages.success(request, "Wall added")
            return redirect('walls_show', str(wall_id))
        else:
            messages.error(request, "Wall is not added")
    else:
        form = forms.AddWallForm()

    return render(request, 'walls/add.html', {'form': form})