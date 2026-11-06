# -*- coding: utf-8 -*-

import os
import yaml

from Modules import databases_service
from View import selected_genres


from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast


class Selected_directory:
    def __init__(self, box):
        self.box_content = box
        self.file_name: str = "/user_database.db"
        with open("Configs/user_config.yaml") as conf:
            self.yaml_conf = yaml.safe_load(conf)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager, select_path=self.select_path
        )

    def file_manager_open(self):
        self.file_manager.show(os.getcwd())  # output manager to the screen
        self.manager_open = True

    def select_path(self, path: str):
        self.yaml_conf['path_db'] = path + self.file_name
        with open("Configs/user_config.yaml", "w", encoding="utf-8") as conf:
            yaml.safe_dump(self.yaml_conf, conf, allow_unicode=True)
        databases_service.Config(path + self.file_name).create_tables()
        toast(f"File save from {path + self.file_name}")
        self.exit_manager()

    def exit_manager(self, *args):
        self.manager_open = False
        with open("Configs/user_config.yaml", "r", encoding="utf-8") as conf:
            if yaml.safe_load(conf)['path_db'] != "None":
                self.file_manager.close()
                self.box_content.clear_widgets()
                selected_genres.Genres(self.box_content).create_box_selected()
            else:
                self.file_manager.close()
                toast("File not found")
