from django.shortcuts import render
from django.http import HttpResponse
import sys
import csv
import os
import pprint

# Create your views here.
def deliriumorbs(request):
    deliriumorb_list = []

    path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    file = path + '/DeliriumOrb.csv'
    file = os.path.normpath(file)
    print(file)
    if not os.path.exists(file):
        return render(request, 'fossils/error.html')
    with open(file, "r") as f:
        reader = csv.DictReader(f)
        for line in reader:
            deliriumorb_list.append(line)
            print(line)
    context = { 'deliriumorb_list': deliriumorb_list }
    return render(request, 'deliriumorbs/deliriumorbs.html', context)