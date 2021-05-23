from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage,\
                                  PageNotAnInteger
from django.views.generic import ListView

"""
A Django view is just a Python function that
    receives a web request and returns a web response.

To change behaviour depending on HTTP request method
    we have to use conditional branching or you could
        use class based view.

Views decide which data gets returned to the user

Templates define how the data is displayed
"""


def post_list(request):
    """
    Use pagination to split the list of posts across several pages
    """
    object_list = Post.published.all()
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
        {'page': page, 'posts': posts}
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
    return render(
        request,
        'blog/post/detail.html',
        {'post': post}
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
