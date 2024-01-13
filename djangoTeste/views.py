from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.cache import cache
from django.shortcuts import render, get_object_or_404, redirect

from .forms import PostForm
from .models import Post, Comment


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect('post_detail', pk=new_post.pk)
    else:
        form = PostForm(initial={field: '' for field in PostForm().fields})
    return render(request, 'blog/post_form.html', {'form': form})


def list_posts(request):
    posts = cache.get('post_list')
    if not posts:
        posts = Post.objects.select_related('author').order_by('-date_published')  # 'author' is a ForeignKey in Post
        cache.set('post_list', posts)

    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


@login_required
def add_new_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if not is_http_post(request) or not is_comment_present(request):
        return redirect_to_post_detail(post_id)
    Comment.objects.create(post=post, content=request.POST.get('comment'), author=request.user)
    return redirect('post_detail', pk=post_id)


@login_required
def delete_comment(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    if not comment or not is_http_post(request):
        return redirect_to_post_detail(comment.post.id)
    if not is_comment_author(request, comment):
        return render(request, 'blog/post_detail.html', {
            'post': comment.post,
            'error': 'You are not authorized to delete this comment.'
        })
    comment.delete()
    return redirect_to_post_detail(comment.post.id)


def is_http_post(request):
    return request.method == 'POST'


def is_comment_present(request):
    return bool(request.POST.get('comment'))


def is_comment_author(request, comment):
    return comment.author == request.user


def redirect_to_post_detail(post_id):
    return redirect('post_detail', pk=post_id)


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect_to_post_detail(post.pk)
    form = PostForm(initial={field: '' for field in PostForm().fields})
    return render(request, 'blog/post_form.html', {'form': form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return redirect('post_detail', pk=post.pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in.
            login(request, user)
            return redirect('post_list')
    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'registration/register.html', context)
