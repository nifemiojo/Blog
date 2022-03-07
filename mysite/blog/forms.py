from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    """
    Each field type has a default widget that determines
        how the field is rendered in HTML.

    The default widget can be overridden with the
        widget attribute.
    https://docs.djangoproject.com/en/3.0/ref/forms/fields/
    """
    name = forms.CharField(max_length=25)
    to = forms.EmailField()
    comments = forms.CharField(
        required=False,
        widget=forms.Textarea
    )


class CommentForm(forms.ModelForm):
    """
    Each model field type has a corresponding default form field type
    """
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
