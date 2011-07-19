from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def safe_html(var):
    from lxml.html.clean import clean_html
    from lxml import etree

    try:
        data = clean_html(var)
    except (etree.ParseError, etree.XMLSyntaxError):
        data = ''
    return mark_safe(data)
