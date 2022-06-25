"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

import ex01.views
import ex02.views
import ex03.views
import product.views
import boardpan.views
import reply.views
import user.views

# 맨 뒤에 /는 입력하지 말 것(abcd가 폴더로 인식될 수가 있음)
urlpatterns = [
    path('admin/', admin.site.urls),

    path('qwer/abcd', ex01.views.func1),
    path('qqqq', ex01.views.func2),
    path('getPost', ex01.views.getPost),
    path('ex02/func1', ex02.views.func1),
    path('ex02/formtag', ex02.views.formtag),
    path('ex02/getdata', ex02.views.getdata),
    path('product/create', product.views.createFruitGet),
    path('product/list', product.views.readFruitGet),

    # path('', frontapp.views.index),

    path('boardpan/mainPage', boardpan.views.mainPage),
    path('boardpan/create', boardpan.views.create),
    path('boardpan/list', boardpan.views.list),
    path('boardpan/read/<int:bid>', boardpan.views.read),
    path('boardpan/delete/<int:bid>', boardpan.views.delete),
    path('boardpan/update/<int:bid>', boardpan.views.update),

    path('reply/create/<int:rid>', reply.views.create),
    path('reply/read/<int:rid>', reply.views.read),
    path('reply/delete/<int:rid>', reply.views.delete),
    path('reply/update/<int:rid>', reply.views.update),

    path('user/signup', user.views.signup),
    path('user/login', user.views.login),
    path('user/logout', user.views.logout),



    path('ex03/func1', ex03.views.func1),
    path('ex03/ajax', ex03.views.ajax),
]