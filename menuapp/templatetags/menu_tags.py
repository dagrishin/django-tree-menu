from django import template
from django.urls import reverse

from menuapp.models import MenuItem

register = template.Library()


def get_menu_items(menu_name, current_url, parent=None):
    if parent:
        menu_items = MenuItem.objects.filter(menu_name=menu_name, parent=parent)
    else:
        menu_items = MenuItem.objects.filter(menu_name=menu_name)
    result = []
    for item in menu_items:
        is_active = current_url == item.url or (item.url and current_url.startswith(item.url))
        result.append({
            'title': item.title,
            'url': item.url if item.url else reverse(item.named_url) if item.named_url else '',
            'is_active': is_active,
            'children': get_menu_items(menu_name, current_url, item.id)
        })
    return result


def render_menu(menu_items):
    if not menu_items:
        return ''

    items_html = ''
    for item in menu_items:
        children_html = render_menu(item['children'])
        active_class = 'active' if item['is_active'] else ''
        url = item['url']
        item_html = f'<li class="{active_class}"><a href="{url}">{item["title"]}</a>{children_html}</li>'
        items_html += item_html

    return f'<ul>{items_html}</ul>'


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    current_url = context['request'].path
    menu_items = get_menu_items(menu_name, current_url)
    return render_menu(menu_items)
