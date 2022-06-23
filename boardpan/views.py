from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect

# Create your views here.
from django.shortcuts import render
from boardpan.models import Post
from boardpan.forms import PostForm
from django.http import HttpResponse


# 목록보기 페이지 (전체 쿼리)
from reply.forms import ReplyForm


def mainPage(request):
    return render(request, 'boardpan/index.html')


# 데코레이터(@)를 통해 로그인 한 경우에만 쓸 수 있도록 함, 달아주기만 하면 해당 기능이 함수에 추가됨
# login_url을 통해 login이 되어있지 않은 경우 login페이지로 이동시켜준다
@login_required(login_url='/user/login')
def create(request):
    # request가 GET 방식이면 수행하는 코드(입력 페이지를 클라이언트에 전달해 줌)
    if request.method == "GET":
        postForm = PostForm()
        context = {'postForm': postForm}
        return render(request, 'boardpan/create.html', context)

    # request가 POST 방식이면 수행하는 코드(입력 양식을 받아감)
    elif request.method == "POST":
        # 값을 Form에 전달
        postForm = PostForm(request.POST)

        # 폼에 전달받은 값 검증
        if postForm.is_valid():
            post = postForm.save(commit=False)
            # 게시글 작성자 정보 추가
            post.writer = request.user
            post.save()
            return redirect('/boardpan/read/' + str(post.id))
        else:
            return HttpResponse("값이 올바르지 않습니다 ")


# 전체 목록 보기
def list(request):
    # order by로 정렬이 가능함, id로 정렬하되 오름차순 (-)
    posts = Post.objects.all().order_by('-id')
    context = {
        'posts': posts
    }
    print(posts)

    # 서버가 context값과 함께 클라이언트에 리턴한다
    return render(request, 'boardpan/list.html', context)


# 게시글 하나를 조회한다(get), 파라미터로 bid값도 같이 줌
def read(request, bid):
    # 조회하는 번호의 게시물 페이지를 준다
    post = Post.objects.get(Q(id=bid))
    
    # 댓글 입력 양식을 전달해 줌 (ReplyForm 클래스의 객체 생성)
    replyForm = ReplyForm()
    
    # 컨텍스트에 위 두개를 담는다
    context = {'post': post, 'replyForm':replyForm}

    # context값과 함께 클라이언트에 리턴
    return render(request, 'boardpan/read.html', context)


@login_required(login_url='/user/login')
def delete(request, bid):
    # q는 여기서 안써도 됨
    post = Post.objects.get(id=bid)  # 삭제할 ID 담기

    # 작성자가 아니면 다른곳으로 내보냄
    if request.user != post.writer:
        return redirect('/boardpan/read/' + str(post.id))
    
    # 바로그냥 삭제
    post.delete()

    # 삭제 후 페이지이동
    return redirect('/boardpan/list')


# 조회한다 - (조회한 내용을 고찬 것을)생성한다 를 함수 하나에 입력할 것
@login_required(login_url='/user/login')
def update(request, bid):  # 몇번 게시글을 수정할 건지 번호를 지정해서 수정 -> delete url 추가 필요

    # 게시글 조회를 먼저 해야 함, ID 에 맞는 데이터를 조회한다
    post = Post.objects.get(id=bid)

    # 작성자가 아니면 다른곳으로 내보냄
    if request.user != post.writer:
        return redirect('/boardpan/read/' + str(post.id))

    # 요청한 게 get이면 수정하는 페이지를 뜨게 함
    if request.method == "GET":

        # 입력하는 곳에 조회한 내용(post)가 미리 들어가 있도록 함
        postForm = PostForm(instance=post)

        # 즉 form 양식을 context에 담아서 브라우저에 띄우도록 한다 (전송)
        context = {'postForm': postForm}

        # updates.html을 새로 만들어도 되고, create 입력 양식을 그대로 써도 무방하다
        return render(request, 'boardpan/create.html', context)

    # 요청한 게 post면 양식 제출하기
    elif request.method == "POST":

        # 원래 게시판에 있던 원본을 대체한다
        postForm = PostForm(request.POST, instance=post)

        # 값이 유효한지 검증
        if postForm.is_valid():
            # post.title = postForm.cleaned_data['title']  # 나쁜 예
            # post.contents = postForm.cleaned_data['contents']  # 나쁜 예
            post = postForm.save(commit=False)  # 좋은 예 (commit: 굳이 저장을 안 시키고, 모델의 객체를 반환한다)
            post.save()  # 저장
            # create.html에서 <post> 태그 내 action=create(URI)를 지워야함
            return redirect('/boardpan/read/' + str(post.id))
            # 수정이 완료되면 해당 게시글로 이동하게 함

        else:
            return HttpResponse("양식오류")
