from django.shortcuts import render


def main(request):
    return render(request, 'pocadeco/main.html')
def decolist(request):
    return render(request, 'pocadeco/decolist.html')
