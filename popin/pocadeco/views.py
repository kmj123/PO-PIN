from django.shortcuts import render


def decoMain(request):
    return render(request,'pocadeco/decoMain.html')

def main(request):
    return render(request, 'pocadeco/main.html')
def mydecolist(request):
    return render(request, 'pocadeco/mydecolist.html')
