from django.shortcuts import render
from django.http import HttpResponse
import sys
import csv
import os
import pprint

# Create your views here.
def scarabs(request):
    scarab_list = []

    path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    file = path + '/Scarab.csv'
    file = os.path.normpath(file)
    print(file)
    if not os.path.exists(file):
        return render(request, 'fossils/error.html')
    with open(file, "r") as f:
        reader = csv.DictReader(f)
        for line in reader:
            scarab_list.append(line)
            print(line)
    context = { 'scarab_list': scarab_list }
    return render(request, 'scarabs/scarabs.html', context)