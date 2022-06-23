from django.http import JsonResponse
from django.shortcuts import render


# Create your views here.
# restapi test


json_data = {
    'message': '안녕하세요',
    '배울과목': ['파이썬', '장고', '리액트', 'k8s']
}

def ajax(request):
    return render(request, 'ajax.html')

def func1(request):
    return JsonResponse(json_data)
