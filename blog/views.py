from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from .models import Post
from .modelforms import PostForm, CommentForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


# Create your views here.
def post_list(request):
    # name = 'NAVI'
    # return HttpResponse('''<h1>Hello {myname} </h1>'''.format(myname=name))
    posts = Post.objects.filter(published_date__lte=timezone.now()).\
                                order_by('published_date')
    return render(request,'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

# def post_new(request):
#     form = PostForm()
#     return render(request, 'blog/post_edit.html', {'form': form})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()

    return render(request, 'blog/post_edit.html', {'form': form})

def post_new_form(request):
    if request.method == 'POST':
        # POST 요청일 때
        form = PostForm(request.POST, request.FILES)
        # 인자로 받은 값에 대해서, 유효성 검증 수행
        if form.is_valid():  # 검증이 성공하면, True 리턴
            # 검증에 성공한 값들을 dict타입으로 제공받아서 이 값을 DB에 저장하기
            form.cleaned_data
            post = Post(author=request.user, title=form.cleaned_data['title'], text=form.cleaned_data['text'],
                        published_date=timezone.now())  # DB에 저장하기

            #post = Post(**form.cleaned_data)  # DB에 저장하기 **dict type

            post.save()
            return redirect('post_detail', pk=post.pk)
        else:  # 검증에 실패하면, form.errors와 form.각필드.errors 에 오류정보를 저장
            form.errors

    else:
        # GET 요청읷 때
        form = PostForm()

    return render(request,'blog/post_form.html', {'form':form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)

