from django import template

register = template.Library()

@register.tag(name='ifcanedit')
def do_ifcanedit(parser, token):
    try:
        tag_name, user, obj_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            '%r tag requires two arguments' % token.contents.split()[0]
        )

    nodelist = parser.parse(('endifcanedit',))
    parser.delete_first_token()
    return IfcaneditNode(user, obj_name, nodelist)

class IfcaneditNode(template.Node):
    def __init__(self, user, obj_name, nodelist):
        self.user = template.Variable(user)
        self.obj = template.Variable(obj_name)
        self.nodelist = nodelist

    def render(self, context):
        try:
            actual_obj = self.obj.resolve(context)
            actual_user = self.user.resolve(context)
        except template.VariableDoesNotExist:
            return ''

        if actual_obj.can_edit(actual_user):
            return self.nodelist.render(context)
        else:
            return ''
