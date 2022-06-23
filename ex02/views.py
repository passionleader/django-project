from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def func1(request):
    return render(request, "ex02/func1.html")

def formtag(request):
    return render(request, "ex02/formtag.html")

def getdata(request):
    userid = request.POST.get('userid', None)
    userpw = request.POST.get('userpw', None)
    print(userid, userpw)
    return HttpResponse("전송되었습니다")