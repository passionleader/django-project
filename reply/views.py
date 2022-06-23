from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


# 댓글 생성
from boardpan.models import Post
from reply.forms import ReplyForm
from reply.models import Reply


# 게시물 조회 시 댓글도 같이 보이게 할 것이므로 GET은 필요 없음, 처리(POST)만 처리
@login_required(login_url='/user/login')
def create(request, rid):
    if request.method == "POST":

        # 사용자가 요청한 내용을 담은 객체
        replyForm = ReplyForm(request.POST)

        # 사용자가 유효하다(로그인)
        if replyForm.is_valid():
            reply = replyForm.save(commit=False)

            # 작성자는 로그인한 사용자(내장모델), 이거 빼먹으면 is_valid에 의해 에러메시지 출력
            # 유저 객체, 2번 사용자 넣고 싶다고 2를 쓰면 안됨 (제약 조건, user 내 데이터만 가능)
            reply.writer = request.user

            # 몇번 게시글인지 지정 (관계맺어준 변수는 해당 객체를 적어줘야 함)
            post = Post()  # 게시판 post모델의 객체 생성
            post.id = rid  # 게시글 번호 = 사용자가 전달한 번호(몇번 게시글의 댓글인지)
            reply.post = post  # 객체

            # 저장
            reply.save()
        return redirect('/boardpan/read/' + str(rid))


# 댓글 수정
def update(request, rid):
    # rid에 해당하는 댓글을 객체로 담음
    reply = Reply.objects.get(id=rid)
    if request.method == "GET":
        # 불러온 객체를 양식에 맞게 사용자에게 보여줌
        replyForm = ReplyForm(instance=reply)
        return render(request, 'reply/create.html', {'replyForm': replyForm})
    elif request.method == "POST":
        # 불러온 객체를 대체하고 사용자가 올린 내용으로 DB에 올린다
        replyForm = ReplyForm(request.POST, instance=reply)
        if replyForm.is_valid():
            reply = replyForm.save(commit=False)
            reply.save()
        # 댓글목록으로 이동시킴
        return redirect('/reply/read/' + str(reply.id))

# 댓글 삭제
def delete(request, rid):
    reply = Reply.objects.get(id=rid)
    reply.delete()

    return redirect('/reply/list')

# 댓글 목록보기
def list(request):
    replys = Reply.objects.all().order_by('-id')  # 역순 정렬
    return render(request, 'reply/list.html', {'replys':replys})

# 댓글 보기
# ID 값(URI 넘버 쓸 수 있도록) 같이 전달
def read(request, rid):
    reply = Reply.objects.get(id=rid)
    # 일치하는 댓글과 함께 컨텍스트 리턴함
    return render(request, 'reply/read.html', {'reply':reply})