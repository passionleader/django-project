from django import forms
from boardpan.models import Post
# 모델의 클래스를 import 한다

class PostForm(forms.ModelForm):
    # 어떤 모델 형식인지 써 줘야함 (이 모델의 양식을 쓸 것이다)
    class Meta:
        model = Post  # model의 클래스명
        fields = ('title', 'contents')  # 어떤 필드들을 입력 받을 지 명시 (시간은 따로 입력받지 않으니 안 써도 됨)
        exclude = ('writer',)  # 입력받고 싶지 않은 것을 명시
