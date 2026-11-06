import asyncio
import base64
from threading import Thread

from kivy.clock import mainthread
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.label import MDLabel
from kivy.core.window import Window

from kivymd.uix.spinner import MDSpinner

from View.card import Card
from View.online_page import online_page
from Modules.parce import parse_genres
from Modules.db_commnads import get_all_genres, add_update_favorite_genres
from Configs.config import list_favorites


class ListCard:
    def __init__(self, obj, title: str | None = None):
        self.obj = obj
        match title:
            case 'selected_genres':
                obj.add_widget(
                    MDLabel(
                        text='Selected please favorite genres',
                        halign="left",
                        valign='top',
                        font_style='H3',
                        font_name="View/fonts/Nunito/static/Nunito-Regular.ttf",
                        font_size="12px",
                        theme_text_color="Primary"
                    )
                )
                obj.add_widget(
                    MDSpinner(
                        size_hint=(.45, 3.2),
                        size=(Window.minimum_width / 2, Window.minimum_height / 2),
                        pos_hint={'center_x': .5, 'center_y': .5},
                        active=True,
                        palette=[
                            [0.28627450980392155, 0.8431372549019608, 0.596078431372549, 1],
                            [0.3568627450980392, 0.3215686274509804, 0.8666666666666667, 1],
                            [0.8862745098039215, 0.36470588235294116, 0.592156862745098, 1],
                            [0.8784313725490196, 0.9058823529411765, 0.40784313725490196, 1],
                        ]
                    )
                )
                if not get_all_genres():
                    Thread(target=self.async_parse_genre, daemon=True).start()
                else:
                    self.set_data(get_all_genres())
            case 'get_all_genres':
                ...
            case _:
                ...

    def async_parse_genre(self):
        datas = asyncio.run(parse_genres('https://rur.hitmotop.com/genres'))
        self.set_data(datas)

    @mainthread
    def set_data(self, datas: list):
        self.obj.clear_widgets()
        title = MDBoxLayout(padding=75, orientation='horizontal')
        done = MDFillRoundFlatButton(
            pos_hint={"center_y": .5},
            font_style='H5',
            text="Done",
            theme_text_color="Primary",
            on_press=self.press_done,
            disabled=True
        )
        # done = btn_done
        title.add_widget(
            MDLabel(
                pos_hint={"center_y": .5},
                text='Selected please favorite genres',
                font_style='H2',
                font_name="View/fonts/Nunito/static/Nunito-Regular.ttf",
                font_size="36px",
                theme_text_color="Primary"
            )
        )
        title.add_widget(done)
        self.obj.add_widget(title)
        scroll = ScrollView(size_hint=(1, 6), size=(Window.width, Window.height))
        stack = StackLayout(padding=15, spacing=15, size_hint_y=None)
        stack.bind(minimum_height=stack.setter('height'))
        for genres in datas:
            stack.add_widget(
                Card(done).card(
                    text=genres['name'],
                    image=genres['img'],
                    url=genres['url'],
                    size=(170, 180),
                    round=30,
                    padding=10,
                    hover=(255 / 255, 170 / 255, 29 / 255, 0.5),
                    color=(40 / 255, 35 / 255, 41 / 255, 0.3)
                )
            )
        scroll.add_widget(stack)
        self.obj.add_widget(scroll)

    def press_done(self):
        add_update_favorite_genres(list_favorites)
        online_page(self.obj)

