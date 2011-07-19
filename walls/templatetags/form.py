from django import template

register = template.Library()

@register.simple_tag
def formfield(field, id, label):
    return """
<li>
    %(errors)s
    <label for="%(id)s">
        %(label)s
    </label>
    %(field)s
</li>
    """ % {
        'errors': field.errors,
        'id': id,
        'label': label,
        'field': field,
    }
