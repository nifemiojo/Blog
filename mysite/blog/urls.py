from django.urls import path
from . import views

"""
URL patterns map URLs to views

Can define an application namespace. Allows you to organize URLs
    by application and use the name when referring to them
https://docs.djangoproject.com/en/3.0/topics/http/urls/#url-namespaces

"""

# Defining an application namespace
app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path(
        '<int:year>/<int:month>/<int:day>/<slug:post>/',
        views.post_detail,
        name='post_detail'
    ),
]
