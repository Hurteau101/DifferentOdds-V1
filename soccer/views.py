from django.shortcuts import render

# Create your views here.
def get_test_view(requests):
    return render(requests, 'soccer_table.html')