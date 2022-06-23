from django.contrib.auth.models import User
from django.db import models


# Create your models here.
# 클래스 생성, 제목 내용 시간 작성자
class Post(models.Model):
    title = models.CharField(max_length=100)
    contents = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)

    # User와 관계를 맺어 줌, cascade: 유저가 회원 탈퇴시 댓글 제거 (존재하는 유저의 댓글만 저장가능)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)



