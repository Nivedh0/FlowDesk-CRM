from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Get item from dictionary by key"""
    if dictionary is None:
        return None
    return dictionary.get(key)


@register.filter
def split(value, delimiter='\n'):
    """Split a string by delimiter"""
    if value is None:
        return []
    if delimiter in ('\n', '\\n', '\r\n', '\\r\\n'):
        return value.splitlines()
    return value.split(delimiter)


@register.filter
def alpha_label(value):
    """Convert 1-based index to alphabetic label: 1 -> A, 2 -> B"""
    try:
        index = int(value)
    except (TypeError, ValueError):
        return value

    if index < 1:
        return value

    output = ''
    while index > 0:
        index -= 1
        output = chr(65 + (index % 26)) + output
        index //= 26
    return output
