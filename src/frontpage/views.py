from django.shortcuts import render
from django.http import HttpResponse
import sys


sys.path.append(r'C:\Users\Jacob\PycharmProjects\PoeBulkFlipper')

import poeAPI

fossil = poeAPI.fossil(1, 2, "wohaoao", 4)

context = {
    'fossil' : fossil
}
# Create your views here.
def home(request):
    return render(request, 'frontpage/home.html', context)