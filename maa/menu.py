from typing import Callable

from ursina import Entity, camera, application, Button, color, destroy


VERTICAL = 0
HORIZONTAL = 1

def get_align(align, what):
    if align is None:
        return 'center'

    if isinstance(align, str):
        return align

    if len(align) == 2:
        return align[what]

    raise ValueError('align needs to be None, an integer, or a tuple')

TOP = 0
RIGHT = 1
BOTTOM = 2
LEFT = 3

def get_margin(margin, what):
    if margin is None:
        return 0

    if isinstance(margin, (int,float)):
        return margin

    if len(margin) == 2:
        if what in (TOP, BOTTOM):
            return margin[TOP]
        if what in (RIGHT, LEFT):
            return margin[RIGHT]

    if len(margin) == 4:
        return margin[what]

    raise ValueError('margin needs to be None, tuple(top, right) or tuple(top, right, bottom, left)')


class Widget(Entity):
    default_widget_values = {
        'position_hint':    'relative',
        'width_hint':       'relative',
        'height_hint':      'relative',
        'min_width':        None,
        'max_width':        None,
        'min_height':       None,
        'max_height':       None,
        'margin':           (0, 0, 0, 0),
        'align':            ('center', 'center'),
    }

    def __init__(self, *args, **kwargs):
        for key, default_value in self.default_widget_values.items():
            if key in kwargs:
                setattr(self, key, kwargs.pop(key))
            elif not hasattr(self, key):
                setattr(self, key, default_value)
            print(self, getattr(self, key))

        super().__init__(*args, **kwargs)

    def on_destroy(self):
        print('destroyed', self, self.children)


class Form(Widget):
    def __init__(
        self,
        parent_form: Entity = None,
        on_close: Callable = None,
        layout: tuple = (),
        *args,
        **kwargs
    ):
        kwargs.setdefault('parent', camera.ui)

        super().__init__(*args, **kwargs)

        self.parent_form = parent_form
        self.on_close = on_close

        for child in layout:
            child.parent = self

        self.enabled = False

    def open(self):
        self.enabled = True

        if self.parent_form:
            self.parent_form.enabled = False

        p = self
        while p != None:
            print('parent', p, getattr(p, 'enabled', 'N/A'))
            p = p.parent

    def close(self):
        if self.parent_form:
            self.parent_form.enabled = True

        if self.on_close:
            self.on_close()

        print('destroy', self)
        destroy(self)


class Panel(Widget):
    def __init__(self, child=None, **kwargs):
        super().__init__(**kwargs)

        if child:
            child.parent = self

        self.background = Entity(
            parent=self,
            model='quad',
            texture='shore',
            scale=(1, 1, 1),
            color=color.white,
            z=1,
            x=0,
            y=0
        )


class Container(Widget):
    children_spacing = 0.05
    align = 'top'
    padding = (0.01, 0.01, 0.01, 0.01)
    margin = 0.01

    def __init__(
        self,
        *children,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.children = list(children)

        self.scale = self.get_scale()

        print(self, self.position, self.scale, self.world_position, self.world_scale)

        for i, e in enumerate(children[::-1]):
            e.parent = self

            self.set_entity_position_and_scale(i, e)
            print('MEMBER', e, getattr(e, 'text', 'xx'), e.position, e.scale, e.world_position, e.world_scale)

        match get_align(self.align, VERTICAL):
            case 'top':
                self.y = 0.5 - (self.scale.y/2) - get_margin(self.padding, TOP)
            case 'center':
                self.y = 0
            case 'bottom':
                self.y = - 0.5 + (self.scale.y/2) + get_margin(self.padding, BOTTOM)

        match get_align(self.align, HORIZONTAL):
            case 'left':
                self.x = 0.5 - (self.scale.x/2) - get_margin(self.padding, LEFT)
            case 'center':
                self.x = 0
            case 'right':
                self.x = - 0.5 + (self.scale.x/2) + get_margin(self.padding, RIGHT)

        self.x += get_margin(self.margin, LEFT)

        self.background = Entity(
            parent=self,
            model='quad',
            texture='shore',
            scale=(1, 1, 1),
            color=color.white,
            z=1,
            x=0,
            y=0
        )



class VerticalContainer(Container):
    def get_scale(self):
        return (
            1 - get_margin(self.margin, LEFT) - get_margin(self.margin, RIGHT),
            sum([child.scale.y for child in self.children]) +
            sum([self.children_spacing for child in self.children[:-1]]) +
            get_margin(self.margin, TOP) + get_margin(self.margin, BOTTOM)
        )

    def set_entity_position_and_scale(self, i, e):
        e.scale = (
            1 - get_margin(self.margin, LEFT)
              - get_margin(self.padding, LEFT)
              - get_margin(self.margin, RIGHT)
              - get_margin(self.padding, RIGHT),
            e.scale[1] / self.scale[1]
        )
        e.y = (i * e.scale[1] + self.children_spacing*i/2) - e.scale[1]/2


class HorizontalContainer(Container):
    def get_scale(self):
        return (
            sum([child.scale.x for child in self.children]) +
            sum([self.children_spacing for child in self.children[:-1]]) +
            get_margin(self.margin, LEFT) + get_margin(self.margin, RIGHT),
            1 - get_margin(self.margin, TOP) - get_margin(self.margin, BOTTOM),
        )

    def set_entity_position_and_scale(self, i, e):
        e.scale = (
            e.scale[0] / self.scale[0],
            1 - get_margin(self.margin, TOP)
              - get_margin(self.padding, TOP)
              - get_margin(self.margin, BOTTOM)
              - get_margin(self.padding, BOTTOM),
        )
        e.x = (i * e.scale[0] + self.children_spacing*i/2) - e.scale[0]/2


class MenuButton(Button):
    def __init__(self, text='', **kwargs):
        super().__init__(text=text, scale=(1, .075), highlight_color=color.azure, **kwargs)

        for key, value in kwargs.items():
            setattr(self, key ,value)


class EditorMapSelectionMenu(Form):
    def __init__(self, parent_form):
        super().__init__(
            parent_form,
            layout=(
                HorizontalContainer(
                    Panel(),
                    VerticalContainer(
                        MenuButton('Back', on_click=self.close),
                        align='right',
                    ),
                ),
            ),
        )


class MainMenu(Form):
    def __init__(self):
        super().__init__(
            layout=(
                Panel(
                    VerticalContainer(
                        MenuButton('Editor', on_click=self.on_editor),
                        MenuButton('Exit', on_click=self.on_exit),
                        align='center',
                    ),
                ),
            ),
        )

    def on_editor(self):
        EditorMapSelectionMenu(self).open()

    def on_exit(self):
        application.quit()
