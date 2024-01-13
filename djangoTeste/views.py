from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment


def list_posts(request):
    posts = Post.objects.order_by('-date_published')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


POST_DETAIL_PAGE = 'post_detail'


@login_required
def add_new_comment(request, post_id):
    print(post_id)
    post = get_object_or_404(Post, pk=post_id)
    if not is_post_request(request):
        return redirect_to_post_detail(post_id)
    comment = request.POST.get('comment')
    if not comment:
        return redirect_to_post_detail(post_id)
    user = request.user
    Comment.objects.create(post=post, content=comment, author=user)
    return redirect_to_post_detail(post_id)


def is_post_request(request):
    return request.method == 'POST'


def redirect_to_post_detail(post_id):
    return redirect(POST_DETAIL_PAGE, pk=post_id)


@login_required
def delete_comment(request, comment_id):
    # Get comment
    comment = Comment.objects.get(pk=comment_id)
    if not comment:
        return redirect_to_post_detail(comment.post.id)
    if not request.method == 'POST':
        return redirect_to_post_detail(comment.post.id)
    if comment.author != request.user:
        return render(request, 'blog/post_detail.html', {
            'post': comment.post,
            'error': 'You are not authorized to delete this comment.'
        })
    comment.delete()
    return redirect_to_post_detail(comment.post.id)
