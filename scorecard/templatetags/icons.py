from django import template

register = template.Library()


@register.filter
def rating(rating):
    if rating == "good" or rating == "great":
        return "fa-smile-o"
    if rating == "ave":
        return "fa-meh-o"
    if rating == "bad":
        return "fa-frown-o"
