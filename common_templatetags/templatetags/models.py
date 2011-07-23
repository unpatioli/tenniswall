from django import template

register = template.Library()

@register.tag(name='ifcan')
def do_ifcan(parser, token):
    try:
        tag_name, user, action, obj_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            '%r tag requires three arguments' % token.contents.split()[0]
        )
    if not(action[0] == action[-1] and action[0] in ('"', "'")):
        raise template.TemplateSyntaxError(
            "%r tag's argument should be in quotes" % tag_name
        )

    nodelist = parser.parse(('endifcan',))
    parser.delete_first_token()
    return IfcanNode(user, action[1:-1], obj_name, nodelist)

class IfcanNode(template.Node):
    def __init__(self, user, action, obj_name, nodelist):
        self.user = template.Variable(user)
        self.action = action
        self.obj = template.Variable(obj_name)
        self.nodelist = nodelist

    def render(self, context):
        try:
            actual_obj = self.obj.resolve(context)
            actual_user = self.user.resolve(context)
        except template.VariableDoesNotExist:
            return ''

        can = getattr(actual_obj, 'can_' + self.action)
        if can(actual_user):
            return self.nodelist.render(context)
        else:
            return ''
