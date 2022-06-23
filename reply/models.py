from django.contrib.auth.models import User
from django.db import models

from boardpan.models import Post


class Reply(models.Model):
    contents = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)

    # 게시물과 관계를 맺어 줌, DB에 저장된 Post만 들어올 수 있다
    # cascade: 게시물 제거시 댓글 삭제
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    # User와 관계를 맺어 줌, DB에 저장된 User만 들어올 수 있다
    # cascade: 유저가 회원 탈퇴시 댓글 제거 (존재하는 유저의 댓글만 저장가능)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)