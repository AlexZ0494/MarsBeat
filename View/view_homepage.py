# -*- coding: utf-8 -*-
import yaml
import time
import random

import kivy
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.clock import Clock
from kivymd.app import MDApp
from kivy.core.window import Window

from Modules.playing import Sound
from View.list_cards import ListCard
from View.online_page import online_page
from Modules.db_commnads import get_favorites_genres

start = time.time()
Window.minimum_height = 810
Window.minimum_width = 1280


class Floating_Sphere(Widget):
    def __init__(self, **kwargs):
        super(Floating_Sphere, self).__init__(**kwargs)


class HomeApp(MDApp):
    def __init__(self, **kwargs):
        super(HomeApp, self).__init__(**kwargs)
        with open("Configs/user_config.yaml", encoding="utf-8") as conf:
            yaml_conf = yaml.safe_load(conf)
        self.theme_cls.theme_style = yaml_conf['theme_style']
        self.theme_cls.primary_palette = yaml_conf['primary_palette']
        self.path_kv: str = "View/templates/home.kv"
        self.screen = Builder.load_file(self.path_kv)
        self.path_db = yaml_conf['path_db']
        self.color_but = (1.0, 0.596078431372549, 0.0, 1.0)
        self.active_but = self.screen.ids.web
        self.spheres = [value for key, value in self.screen.ids.items() if key.find('sphere') == 0]
        self.sound = Sound(self.screen)

    def on_start(self):
        if not get_favorites_genres():
            ListCard(self.screen.ids.content, 'selected_genres')
        else:
            online_page(self.screen, self.sound)
        for obj in self.spheres:
            x_random = random.randint(-1, Window.size[0] // 100) * 100
            y_random = random.randint(-obj.size[1] // 100, Window.size[1] // 100) * 100
            obj.pos = (x_random, y_random)
            x_random = random.randint(-1, Window.size[0] // 100) * 100
            y_random = random.randint(-1, Window.size[1] // 100) * 100
            Animation(
                x=x_random,
                y=y_random,
                duration=30
            ).start(obj)
        Clock.schedule_interval(self.animation, 30)
        Clock.schedule_interval(self.animation, 30)

    def test_press(self, *args):
        print(args[1])
        if args[1] == 'web':
            print('web')
            online_page(self.screen, self.sound)
        print(args[0])
        self.active_but.text_color = (1, 1, 1, 1)
        args[0].text_color = self.color_but
        self.active_but = args[0]

    def play_pause(self, *args):
        self.sound.playing()

    def animation(self, time_out):
        for obj in self.spheres:
            x_random = random.randint(-1, Window.size[0] // 100) * 100
            y_random = random.randint(-1, Window.size[1] // 100) * 100
            Animation(
                x=x_random,
                y=y_random,
                duration=time_out
            ).start(obj)

    def build(self) -> kivy.uix.screenmanager.ScreenManager:
        return self.screen


def run_view() -> None:
    Window.size = (Window.minimum_width, Window.minimum_height)
    HomeApp().run()


def test(*args):
    time.sleep(10)
    print(args)
    return args
    # print('Testing')
