from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.tag(name='link')
def do_link(parser, token):
    try:
        tag_name, request, url_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            '%r tag requires two arguments' % token.contents.split()[0]
        )

    nodelist = parser.parse(('endlink',))
    parser.delete_first_token()
    return LinkNode(request, url_name, nodelist)

class LinkNode(template.Node):
    def __init__(self, request, url_name, nodelist):
        self.request = template.Variable(request)
        self.url_name = url_name
        self.nodelist = nodelist

    def render(self, context):
        import re
        pattern = reverse(self.url_name)
        output = self.nodelist.render(context)
        try:
            actual_request = self.request.resolve(context)
        except template.VariableDoesNotExist:
            return ''

#        if not re.search(pattern, actual_request.path):
        if pattern != actual_request.path:
            output = """
<a href="%(url)s">%(text)s</a>
            """ % {
                'url': pattern,
                'text': output,
            }
        return output
