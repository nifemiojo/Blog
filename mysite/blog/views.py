from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage,\
                                  PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from taggit.models import Tag

"""
A Django view is just a Python function that
    receives a web request and returns a web response.

To change behaviour depending on HTTP request method
    we have to use conditional branching or you could
        use class based view.

Views decide which data gets returned to the user

Templates define how the data is displayed
"""


def post_list(request, tag_slug=None):
    """
    Use pagination to split the list of posts across several pages
    """
    object_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(
        request,
        'blog/post/list.html',
        {'page': page, 'posts': posts, 'tag': tag}
    )


def post_detail(request, year, month, day, post):
    """
    Display a single post
    """
    post = get_object_or_404(
        Post,
        slug=post,
        status='published',
        publish__year=year,
        publish__month=month,
        publish__day=day
    )

    # List of active comments for this post
    comments = post.comments.filter(active=True)

    new_comment = None

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    # List of similar posts
    """
    The values_list() QuerySet returns tuples with the values
        for the given fields (id)
    """
    post_tags_ids = post.tags.values_list('id', flat=True)
    """
    You get all posts that contain any of these tags, 
        excluding the current post itself.
    """
    similar_posts = Post.published.filter(tags__in=post_tags_ids)\
                                  .exclude(id=post.id)
    """
    Use the Count aggregation function to generate a calculated field—same_
        tags—that contains the number of tags shared
            with all the tags queried.
    """
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
        .order_by('-same_tags', '-publish')[:4]

    return render(
        request,
        'blog/post/detail.html',
        {
            'post': post,
            'comments': comments,
            'new_comment': new_comment,
            'comment_form': comment_form,
            'similar_posts': similar_posts,
        }
    )


class PostListView(ListView):
    """
    Class-based views are an alternative way to implement views as
        Python objects, defining views as class methods

    All Django views inherit from the base View class

    Can use different methods for each HTTP request type e.g. GET or POST
    """
    queryset = Post.published.all()

    # Default variable is object_list if you don't specify
    context_object_name = 'posts'

    # passes the selected page in a variable called page_obj
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            """
            You can see a list of validation errors by
                accessing form.errors

            request.build_absolute_uri() builds a complete URL, including the
                HTTP schema and hostname.
            """
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'sparefemi@gmail.com', [cd['to']])
            sent = True

    else:
        form = EmailPostForm()
    return render(
        request,
        'blog/post/share.html',
        {'post': post, 'form': form, 'sent': sent}
    )
