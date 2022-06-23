from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout


# Create your views here.
def signup(request):
    if request.method == "GET":
        # 회원가입 폼: 장고 내장
        signupForm = UserCreationForm()
        # 전달할 때는 항상 딕셔너리 형태
        context = {'signupForm': signupForm}
        return render(request, 'user/signup.html', context)

    elif request.method == "POST":
        # 기본 모델로부터 객체 생성함
        signupForm = UserCreationForm(request.POST)
        # 데이터 검사
        if signupForm.is_valid():
            user = signupForm.save(commit=False)
            user.save()

            # 처리 이후 context를 더 줄 필요가 없으니까 게시판으로 redirect 시켜버리자
            # return render(request, 'user/signup.html')
            return redirect('/boardpan/listGet')
        else:
            return HttpResponse("잘못된 비밀번호입니다")


def login(request):
    if request.method == "GET":
        # 로그인 폼: 장고 내장
        loginForm = AuthenticationForm()
        # 전달할 때는 항상 딕셔너리 형태
        context = {'loginForm': loginForm}
        return render(request, 'user/login.html', context)

    elif request.method == "POST":
        # 기본 모델로부터 객체 생성함
        loginForm = AuthenticationForm(request, request.POST)  # 두개 다 넣어야 함

        # ID, PW가 일치할 경우 (내장 모델의 폼 사용)
        # 예전같은 경우 일일이 DB 정보를 가져와 if문으로 일치여부를 비교해야 했음
        if loginForm.is_valid():
            auth_login(request, loginForm.get_user())  # 함수명이 겹쳐서 다른이름으로 import 했음

            # 처리 이후 context를 더 줄 필요가 없으니까 게시판으로 redirect 시켜버리자
            # return render(request, 'user/signup.html')
            return redirect('/boardpan/listGet')

        # 로그인 실패 시
        else:
            return HttpResponse("잘못된 비밀번호입니다")


def logout(request):
    # GET만 필요(로그아웃할래!)
    auth_logout(request)
    return redirect('/boardpan/listGet')


