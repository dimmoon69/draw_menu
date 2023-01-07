from django.utils.text import slugify as django_slugify


alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh',
            'з': 'z', 'и': 'i', 'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o',
            'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts',
            'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'i', 'э': 'e', 'ю': 'yu', 'я': 'ya'}


def slugify(s):
    """
    Переопределение django slugify, которое также позволяет использовать русские слова.
    """
    return django_slugify(''.join(alphabet.get(w, w) for w in s.lower()))


def path_element(request):
    return list(filter(None, request.path.split('/')))


class NodeMenu:
    __slots__ = 'children', 'item', 'item_slug', 'objects', 'roots'

    def __init__(self, children=None, item=None, item_slug=None):
        self.objects = {}
        self.roots = []
        self.item = item
        self.item_slug = item_slug
        self.children = children

    def get_item(self, menu_items):
        for item in menu_items:
            # получить или создать новый узел
            if item.pk in self.objects:
                elem = self.objects[elem]
                elem.item = item
            else:
                elem = NodeMenu(children=[], item=item, item_slug=item.slug)
                self.objects[item.pk] = elem

            if item.parent is None:
                # если элемент является корневым (без родительского элемента)
                self.roots.append(elem)
            else:
                # если у элемента есть родительский
                if item.parent_id in self.objects:
                    # если родительский элемент уже есть
                    parent_elem = self.objects[item.parent_id]
                else:
                    # если еще нет
                    parent_elem = NodeMenu(children=[], item=item, item_slug=item.slug)
                parent_elem.children.append(elem)
        return self.roots


class NodeMenuHtmlRender:
    __slots__ = 'html_result', 'roots'

    def __init__(self, roots):
        self.html_result = None
        self.roots = roots

    def tree(self):
        self.html_result = "<ul>"
        for root in self.roots:
            self.tree_recursion(root, 0)
        self.html_result += "</ul>"
        return self.html_result

    def tree_recursion(self, root, level=0):
        self.html_result += f"<li><a href='{root.item.slug}'>{root.item}</a>"
        if len(root.children) > 0:
            self.html_result += "<ul>"
            for node in root.children:
                self.tree_recursion(node, level + 1)
            self.html_result += "</ul>"
        self.html_result += "</li>"
