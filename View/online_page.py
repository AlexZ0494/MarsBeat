import asyncio
from threading import Thread

from kivy.clock import mainthread
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.uix.fitimage import FitImage
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.list import TwoLineAvatarIconListItem
from kivymd.uix.spinner import MDSpinner

from Modules.db_commnads import get_favorites_genres, get_rand_music, get_music
from Modules.parce import parse_tracks
from Modules.playing import Sound


class Cell(TwoLineAvatarIconListItem):
    name_track = StringProperty()
    autor_name = StringProperty()
    img = StringProperty()
    time = StringProperty()
    url = StringProperty()
    id = StringProperty()


def online_page(obj: MDBoxLayout, player: Sound):

    def get_tracks():
        asyncio.run(parse_tracks([item['url'] for item in get_favorites_genres()]))
        container_recomend_tracks(content.ids.music_list)

    def press_button(self):
        print(self.id)
        content.ids.online_content.clear_widgets()

    obj.ids.content.clear_widgets()
    content = Builder.load_file('View/templates/online_page.kv')
    container_fgenres(content.ids.scroll_genres, press_button)
    if not get_music():
        content.ids.music_list.add_widget(
            MDSpinner(
                size_hint=(.45, .45),
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
        Thread(target=get_tracks, daemon=True).start()
    container_recomend_tracks(content.ids.music_list, player)
    obj.ids.content.add_widget(content)


def container_fgenres(self, press_button):
    count_fgenres: int = 0
    for item in get_favorites_genres():
        count_fgenres += 1
        card = MDCard(
            id=item['url'],
            orientation='vertical',
            padding=15,
            md_bg_color=(0, 0, 0, 0),
            focus_behavior=True,
            focus_color=(255 / 255, 170 / 255, 29 / 255, 0.5),
            unfocus_color=(0, 0, 0, 0),
            radius=(15, 15, 15, 15),
            on_press=press_button
        )
        card.add_widget(
            FitImage(source=item['img'], radius=15, size_hint=(None, None), pos_hint={'center_x': .5, 'center_y': .5})
        )
        card.add_widget(
            MDLabel(text=item['name'], halign="center", font_name='View/fonts/Nunito/static/Nunito-Regular.ttf')
        )
        self.add_widget(card)
    self.size_hint = (count_fgenres / 10, .9)
    self.pos_hint = {'center_x': .5, 'center_y': .5}


def container_albums(self):
    ...


@mainthread
def container_recomend_tracks(self, player):
    list_music = get_rand_music()
    data_tables = Builder.load_file('View/templates/table.kv')
    player.set_list_music(list_music)
    for ind, item in enumerate(list_music):
        data_tables.ids.tab.add_widget(
            Cell(
                id=str(ind),
                url=item['file'],
                name_track=item['name'],
                autor_name=item['autor'],
                img=item['img'],
                time=item['_time'],
                on_press=player.playing
            )
        )
    self.add_widget(data_tables)
