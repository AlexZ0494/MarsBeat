import io

import pygame.mixer_music as sound
import pygame.mixer as mixer
import requests
from kivy.clock import Clock
from kivymd.uix.boxlayout import MDBoxLayout
from Configs.config import header

mixer.init()

# mixer.Channel()

l_music: list = []


class Sound:
    def __init__(self, window: MDBoxLayout):
        self.__nl_music = None
        self.__m_index = None
        self.__check_pos = None
        self.__window: MDBoxLayout = window
        self.url_playing = None
        self.state_playing: bool = False
        self.__btn = None

    def load(self, url: str, name_track: str):
        if self.url_playing != url:
            self.__window.ids.name_track.text = name_track
            response = requests.get(url=url, headers=header)
            res = io.BytesIO(response.content)
            sound.load(res)
            self.url_playing = url

    def playing(self, btn=None):
        if self.url_playing != btn and btn is not None:
            self.__window.ids.name_track.text = f"{btn.autor_name} - {btn.name_track}"
            response = requests.get(url=btn.url, headers=header)
            res = io.BytesIO(response.content)
            sound.load(res)
            sound.play()
            # print(mixer.Sound(res).get_length())
            self.state_playing = True
            self.__window.ids.play_pause.icon = 'pause'
            self.url_playing = btn
            self.__btn = btn
            self.__nl_music: list = [mus[1] for mus in enumerate(l_music[0][int(btn.id)+1:]) if mus[0] < 3]
            self.__m_index: str = int(btn.id) + 2
            self.__check_pos: int = 0
            Clock.schedule_once(self.queue)
            Clock.schedule_interval(callback=self.next_music, timeout=1 / 10_000)
            # for item in l_music[int(btn.id)+1:]:
            #
            #     response = requests.get(url=item.get('file'), headers=header)
            #     res = io.BytesIO(response.content)
            #     sound.queue(res)

            # self.__btn.md_bg_color = (1, 0, 0, .3)
        else:
            if self.state_playing is False and self.url_playing is not None:
                self.__window.ids.play_pause.icon = 'pause'
                sound.unpause()
                self.state_playing = True
            else:
                sound.pause()
                self.state_playing = False
                self.__window.ids.play_pause.icon = 'play'

    def set_list_music(self, list_music: list) -> None:
        l_music.append(list_music)

    def queue(self, dt):
        print(self.__nl_music)
        for item in self.__nl_music:
            response = requests.get(url=item['file'], headers=header)
            res = io.BytesIO(response.content)
            sound.queue(res)

    def next_music(self, dt):
        if sound.get_pos() < self.__check_pos != 0:
            if len(self.__nl_music) > 1:
                self.__window.ids.name_track.text = f"{self.__nl_music[0]['autor']} - {self.__nl_music[0]['name']}"
                self.__nl_music.pop(0)
            else:
                self.__window.ids.name_track.text = f"{self.__nl_music[0]['autor']} - {self.__nl_music[0]['name']}"
                self.__nl_music.append([mus[1] for mus in enumerate(l_music[0][self.__m_index+1:]) if mus[0] < 3])
                self.__m_index = self.__m_index + 2
                Clock.schedule_once(self.queue)
            self.__check_pos = sound.get_pos()
        else:
            self.__check_pos = sound.get_pos()
