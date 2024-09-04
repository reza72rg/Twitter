from django import template

from comment.models import Comment

register = template.Library()


@register.simple_tag(name="comments_count")
def function(pid):
    return Comment.objects.filter(post=pid, approach=True).count()
