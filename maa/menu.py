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
            print(p, getattr(p, 'enabled', 'N/A'))
            p = p.parent

    def close(self):
        destroy(self)
        if self.parent_form:
            self.parent_form.enabled = True

        if self.on_close:
            self.on_close()


class Panel(Widget):
    pass


class HorizontalContainer(Widget):
    def __init__(
        self,
        *children,
        align='center',
        margin=0,
        **kwargs,
    ):
        super().__init__(**kwargs)

    def parent_setter(self, parent):
        super().parent_setter(parent)

        for n, child in enumerate(self.children):
            child.parent = parent
            if child.height_hint == 'relative':
                child.height = self.height


class VerticalContainer(Widget):
    def __init__(
        self,
        *children,
        align='top',
        **kwargs
    ):
        super().__init__(**kwargs)


    def update_positions(self):
        for i, e in enumerate(self.children):
            e.parent = self
            e.y = (-i-2) * self.button_spacing



class VerticalMenu(Widget):
    button_spacing = 0.05
    align = 'top'
    padding = (0.01, 0.01, 0.01, 0.01)
    margin = 0.01

    def __init__(
        self,
        *buttons,
        **kwargs
    ):
        super().__init__(**kwargs)

        self.scale = (
            1 - get_margin(self.margin, LEFT) - get_margin(self.margin, RIGHT),
            sum([button.scale.y for button in buttons]) +
            sum([self.button_spacing for button in buttons[:-1]]) +
            get_margin(self.margin, TOP) + get_margin(self.margin, BOTTOM)
        )
        buttons_height = sum([button.scale.y for button in buttons])

        print(self, self.position, self.scale, self.world_position, self.world_scale)

        for i, e in enumerate(buttons[::-1]):
            e.parent = self
            e.scale = (
                1 - get_margin(self.margin, LEFT) - get_margin(self.padding, LEFT) - get_margin(self.margin, RIGHT) - get_margin(self.padding, RIGHT),
                e.scale[1] / self.scale[1]
            )
            e.y = (i * e.scale[1] + self.button_spacing*i/2) - e.scale[1]/2
            print('BUTTON', e, e.text, e.position, e.scale, e.world_position, e.world_scale)

        match get_align(self.align, VERTICAL):
            case 'top':
                self.y = 0.5 - (self.scale.y/2) - get_margin(self.padding, TOP)
            case 'center':
                self.y = 0
            case 'bottom':
                self.y = - 0.5 + (self.scale.y/2) + get_margin(self.padding, BOTTOM)

        self.x += get_margin(self.margin, LEFT)

        self.background = Entity(parent=self, model='quad', texture='shore', scale=(1, 1, 1), color=color.white, z=1, x=0, y=0)



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
                    VerticalMenu(
                        MenuButton('Back', on_click=self.close),
                    ),
                ),
            ),
        )


class MainMenu(Form):
    def __init__(self):
        super().__init__(
            layout=(
                VerticalMenu(
                    MenuButton('Editor', on_click=self.on_editor),
                    MenuButton('Exit', on_click=self.on_exit),
                ),
            ),
        )

    def on_editor(self):
        EditorMapSelectionMenu(self).open()

    def on_exit(self):
        application.quit()
