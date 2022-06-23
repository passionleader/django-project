from django.shortcuts import render
from product.models import Fruits


# 데이터를 입력받는 페이지를 클라이언트로 띄움(get)
def createFruitGet(request):
    return render(request, "product/create.html")


# 폼에 담긴 데이터를 서버로 전송하는 역할(post, 접속 불가능)
def createFruitPost(request):
    # 객체 생성! 이 클래스는 상속받은 클래스에서 생성된 객체
    fruit = Fruits()
    fruit.name = request.POST.get('fname', None)
    fruit.descript = request.POST.get('fdescript', None)
    fruit.price = request.POST.get('fprice', None)
    fruit.quantity = request.POST.get('fquantity', None)

    # DB에 저장!
    fruit.save()
    
    # 전송한 뒤에도 동일한 페이지를 띄움
    return render(request, "product/create.html")


# DB에 담긴 데이터들을 조회하는 역할
def readFruitGet(request):
    # Fruits table 내의 모든 필드들을 ORM을 통해 django의 객체로 전부 꺼내온다

    # 조회하는 방법
    # fruits = Fruits.objects.all()  # 전체조회
    # fruits = Fruits.objects.filter(id=4)  # 필터를 사용해서 일치하는 값으로 조회
    fruits = Fruits.objects.filter(name__contains="App")  # 필터를 사용해서 포함된 일부문자로 검색

    # SQL문 사용 가능(SQL문 쓸거면 ORM을 사용하는 이유가 없지)
    # fruits = Fruits.objects.raw('SELECT * FROM product_fruits')

    context = {
        'fruits': fruits
    }
    print(fruits)

    # 리턴 (context 추가하는 거 까먹지 말것, html 결과에 context 결과값을 같이 전달)
    return render(request, "product/read.html", context)