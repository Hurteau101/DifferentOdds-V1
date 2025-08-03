from django.shortcuts import render

# Create your views here.
def new_update_view(request):
    """
    Render the new update page.
    """
    return render(request, 'new_update.html')