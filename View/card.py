from kivy.properties import StringProperty, BooleanProperty, ColorProperty
from kivymd.uix.card import MDCard
from kivymd.uix.fitimage import FitImage
from kivymd.uix.label import MDLabel, MDIcon

from Configs.config import list_favorites

selected_objects = []


class MD3Card(MDCard):
    """Implements a material design v3 card."""
    id = StringProperty()
    _state = BooleanProperty()
    text = id
    url = StringProperty()
    image = StringProperty()
    orientation = StringProperty('vertical')
    hover = ColorProperty()
    color = ColorProperty()
    round = 0


class Card:
    def __init__(self, btn_done=None):
        self.btn_done = btn_done

    def card(self, text: str, image: str, size: tuple, url: str, padding=0, orientation='vertical', hover=None,
             color=(0, 0, 0, 0), round=0):
        def click(obj):
            if obj._state is False:
                obj.md_bg_color = (255 / 255, 170 / 255, 29 / 255, 0.5)
                obj.unfocus_color = (255 / 255, 170 / 255, 29 / 255, 0.5)
                obj.focus_behavior = False
                obj._state = True
                list_favorites.append({
                    'name': obj.id,
                    'url': obj.url
                })
            else:
                obj._state = False
                obj.md_bg_color = (40 / 255, 35 / 255, 41 / 255, 0.3)
                obj.unfocus_color = (40 / 255, 35 / 255, 41 / 255, 0.3)
                obj.focus_behavior = True
                list_favorites.remove(
                    {
                        'name': obj.id,
                        'url': obj.url
                    }
                )
            if self.btn_done is not None:
                if list_favorites:
                    self.btn_done.disabled = False
                else:
                    self.btn_done.disabled = True

        if hover is not None:
            _card = MD3Card(
                id=text,
                _state=False,
                url=url,
                padding=padding,
                spacing=padding,
                orientation=orientation,
                size_hint=(None, None),
                size=size,
                ripple_behavior=True,
                focus_behavior=True,
                focus_color=hover,
                unfocus_color=color,
                md_bg_color=color,
                radius=(round, round, round, round),
                on_press=click
            )
        else:
            _card = MD3Card(
                id=text,
                _state=False,
                padding=padding,
                spacing=padding,
                orientation=orientation,
                size_hint=(None, None),
                size=size,
                ripple_behavior=True,
                md_bg_color=color,
                radius=(round, round, round, round),
                on_press=click
            )
        if image != 'NULL':
            _card.add_widget(
                FitImage(
                    source=image,
                    radius=round + 10
                )
            )
        else:
            _card.add_widget(
                MDIcon(
                    icon='image-off-outline',
                    pos_hint={"center_x": .5, "center_y": .5},
                    font_size='15dp'
                )
            )
        _card.add_widget(
            MDLabel(
                text=text,
                adaptive_size=True,
                halign="center",
                font_name="View/fonts/Nunito/static/Nunito-Regular.ttf",
                font_size="14sp",
                theme_text_color="Primary",
                pos_hint={'center_x': .5}
            )
        )
        return _card
