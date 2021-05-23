"""
QUERYSETS
    A QuerySet is a collection of database
        queries to retrieve objects from your database.

    get() errors:
        - DoesNotExist
        - MultipleObjectsReturned

    <Name_of_model>.objects.create() -- persist new object to db
    instance.save() -- updates after an edit

    Each Django model has at least one manager,
        and the default manager is called objects.

    You get a QuerySet object using a method model manager
    e.g. all_posts = Post.objects.all()

    Django QuerySets are lazy, which means
        they are only evaluated when they are forced to be.

    Creating a QuerySet doesn't involve any database
        activity until it is evaluated. QuerySets usually
            return another unevaluated QuerySet

    QuerySets are only evaluated in the following cases:
        • The first time you iterate over them
        • When you slice them, for instance, Post.objects.all()[:3]
        • When you pickle or cache them
        • When you call repr() or len() on them
        • When you explicitly call list() on them
        • When you test them in a statement, such as bool(), or, and, or if

CUSTOM MODEL MANAGERS
    E.G. Create a manager to retrieve all posts with the published status.

https://docs.djangoproject.com/en/3.0/ref/models/querysets/
"""
