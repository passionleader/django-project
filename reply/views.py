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
@login_required(login_url='/user/login')
def update(request, rid):
    # rid에 해당하는 댓글을 객체로 담음
    reply = Reply.objects.get(id=rid)

    # 댓글 작성자가 아니면 수정 불가, 원래 게시물페이지로 이동 (테이블 id로 확인함)
    if request.user.id != reply.writer_id:
        return redirect('/boardpan/read/' + str(reply.post_id))

    # 원래 적혀있던 양식 전달하기 (get)
    if request.method == "GET":

        # 불러온 객체를 양식에 맞게 사용자에게 보여줌
        replyForm = ReplyForm(instance=reply)

        # 입력하는 곳에 원래 적은 댓글 들어가있으라
        context = {'replyForm': replyForm}
        
        # 전달
        return render(request, 'reply/create.html', context)
    
    # 원래 서버(DB)에 있던 것을 대체해라!(post)
    elif request.method == "POST":

        # 불러온 객체를 대체하고 사용자가 올린 내용으로 DB에 올린다
        replyForm = ReplyForm(request.POST, instance=reply)
        
        # 유효하다면 저장함
        if replyForm.is_valid():
            reply = replyForm.save(commit=False)
            reply.save()
            
        # 원래 있던 게시물로 이동
        return redirect('/boardpan/read/' + str(reply.post_id))


# 댓글 삭제, 물론 로그인 필요
@login_required(login_url='/user/login')
def delete(request, rid):
    # rid에 해당하는 댓글을 객체로 담음
    reply = Reply.objects.get(id=rid)

    # 댓글 작성자가 아니면 삭제 불가, 원래 게시물페이지로 이동 (테이블 id로 확인함)
    if request.user.id != reply.writer_id:
        return redirect('/boardpan/read/' + str(reply.post_id))

    # 본인이 맞으면 삭제
    reply.delete()

    # 삭제가 완료되면 해당 댓글이 있던 게시글로 이동함
    return redirect('/boardpan/read/' + str(reply.post_id))


# 댓글 목록보기
def list(request):
    replys = Reply.objects.all().order_by('-id')  # 역순 정렬
    return render(request, 'reply/list.html', {'replys':replys})


# def read(request, rid): 는 boardpan/raed에 구현이라 불필요
