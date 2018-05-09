from django import forms
from .models import Post, Comment

def min_length_3_validator(value):
    if len(value) < 3:
        raise forms.ValidationError('3글자 이상 입력해주세요')

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','text']
        #fields = '__all__' # 전체필드지정 혹은 list로 끌어올 필드명 지정

class PostForm1(forms.Form):
    title = forms.CharField(validators=[min_length_3_validator])
    text = forms.CharField(widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text',)
