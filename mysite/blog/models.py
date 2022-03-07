from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

"""
The custom manager will allow you to retrieve posts using Post.published

The first manager declared in a model becomes the default manager. Can override
    in Meta.

The convention in Django is to add a get_absolute_url()
    method to the model that returns the canonical URL for the object.
"""


class PublishedManager(models.Manager):
    """
    The manager will allow you to retrieve posts using Post.published.<action>
    e.g. Post.published.filter(title__startswith='Who')
    """
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    author = models.ForeignKey(
                                User,
                                on_delete=models.CASCADE,
                                related_name='blog_posts'
                            )
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')
    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # Our custom manager.
    """
    The tags manager will allow you to add, retrieve, and remove tags from Post
        objects.
    """
    tags = TaggableManager()

    class Meta:
        ordering = ('-publish',)
        default_manager_name = 'objects'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
        Returns the canonical URL for the object

        Use this method in templates to link to specific posts

        Reverse allows you to build URLs by their name and pass
            optional parameters
        """
        return reverse(
            'blog:post_detail',
            args=[
                self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug
            ]
        )


class Comment(models.Model):
    """
    related_name allows you to use Post.comments.all()
        default is comment_set
    """
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
