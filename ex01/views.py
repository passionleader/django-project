from unittest import result

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def func1(request):
    numVar1 = request.GET.get('num1', None)
    numVar2 = request.GET.get('num2', None)
    result = int(numVar1) + int(numVar2)
    print(numVar1+numVar2)
    context = {'key1': result}
    return render(request, 'ex01/page1.html', context)


def func2(request):
    return render(request, 'ex01/input.html')


def getPost(request):
    num1 = request.POST.get('num1', None)
    num2 = request.POST.get('num2', None)
    return HttpResponse(int(num1) + int(num2))
