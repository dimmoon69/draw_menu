from django.template import RequestContext
from django.templatetags.cache import register

from backend.menubar.models import MenuItem
from backend.menubar.utils import NodeMenuHtmlRender, NodeMenu, path_element


@register.inclusion_tag('menu.html', takes_context=True)
def draw_menu(context: RequestContext, menu_name: str) -> dict:

    elements = path_element(context['request'])
    element_html = f'<a href="/{menu_name}">{menu_name}</a></br>'

    if elements and menu_name in elements:
        menu_items = MenuItem.objects.select_related(
            'menu', 'parent'
        ).filter(menu__name=menu_name)

        new_menu_items = []
        for menu_item in menu_items:
            if menu_item.menu.name == elements[0]:
                if str(menu_item.parent) in elements or menu_item.parent is None:
                    new_menu_items.append(menu_item)

        roots = NodeMenu().get_item(new_menu_items)
        result = NodeMenuHtmlRender(roots)
        return {'menu': element_html, 'menu_items': result.tree()}
    return {'menu_items': element_html}
