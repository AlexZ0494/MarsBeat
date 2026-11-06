from Modules import filemanager

from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.fitimage.fitimage import FitImage

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.button import MDRoundFlatIconButton
from kivy.uix.scrollview import ScrollView


class Genres:
    def __init__(self, box_content):
        self.content_block = box_content

    def create_box_selected(self) -> bool:
        # self.content_block.clear_widgets()
        print(Window.size)
        cols: int = ((Window.size[0] - 80) // (64*2))
        spacing: float = (((Window.size[0] - 80) % 64) / (100*2))
        list_genre: list = None
        while list_genre is None:
            list_genre: list = webparse.WebParse().parse_genre()
        scroll = ScrollView(size_hint=(1, 1), do_scroll_y=True, do_scroll_x=False)
        genres = GridLayout(cols=cols, spacing=spacing, size_hint=(None, None), width=500)
        genres.bind(minimum_height=genres.setter('height'))
        for _list in list_genre:
            if _list.url is not None:
                content = MDBoxLayout(orientation="vertical",
                                      adaptive_width=True,
                                      adaptive_height=True)
                if not _list.img:
                    icon = MDIcon(icon="image-off-outline", pos_hint={'center_x': .5, 'center_y': .5})
                    icon.id = _list.title
                    icon.bind(on_press=lambda x: print(x.id))
                    content.add_widget(icon)
                else:
                    icon = FitImage(source=_list.img)
                    icon.id = _list.title
                    icon.bind(on_press=lambda x: print(x.id))
                    content.add_widget(icon)
                # content.add_widget(name_genres)
                genres.add_widget(content)
                # print(self.content_block.text, icon.id)
                # genres.add_widget(MDFlatButton(text=_list.title, theme_text_color="Custom"))
        scroll.add_widget(genres)
        self.content_block.add_widget(
            MDLabel(text='Selected please favorite genres', halign="center", theme_text_color="Primary",
                    size_hint=(1, .1)))
        self.content_block.add_widget(scroll)

        return True


class Selected_Path:
    def __init__(self, box_content):
        self.box = box_content

    def create_button(self):
        con = MDBoxLayout(size_hint_x=None, pos_hint={"center_x": 0.4})
        but = MDRoundFlatIconButton(text="Select path from database", icon="folder", pos_hint={"center_y": 0.5})
        but.bind(on_press=lambda a: filemanager.Selected_directory(self.box).file_manager_open())
        con.add_widget(but)
        self.box.add_widget(con)
