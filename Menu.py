from ursina import *
from random import randint

class MenuButton(Button):
    def __init__(self, text='', **kwargs):
        super().__init__(text=text, scale=(.25, .075), highlight_color=color.azure, **kwargs)
        for key, value in kwargs.items():
            setattr(self, key, value)

class Main_Menu:
    def __init__(self):

        self.MenuBool = False
        mouse.locked = False # Разблокируем курсор
        self.menu_parent = Entity(parent=camera.ui, y=.1, z=-1)  # Установить z ближе к камере
        self.main_menu = Entity(parent=self.menu_parent, z=-1)  # Тоже установить ближе

        self.main_menu.buttons = [
            MenuButton('start', on_click=Sequence(Wait(.01), Func(self.start_game))),
            MenuButton('quit', on_click=Sequence(Wait(.01), Func(application.quit))),
        ] # Добавляем кнопки в меню

        button_spacing = .075 * 1.25
        for i, e in enumerate(self.main_menu.buttons):
            e.parent = self.main_menu
            e.y = (-i - 2) * button_spacing
            e.z = -1  # Кнопки тоже ближе к камере

        # Создаем бэкграунд
        background = Entity(
            parent=self.menu_parent, 
            model='cube', 
            texture=f'textures/{randint(1, 5)}.jpg', 
            scale=(camera.aspect_ratio, 1), 
            world_y=0,
            z=-1.1  # Задний фон чуть дальше кнопок
        )

    def start_game(self):
        application.resume() # Продолжаем игру
        destroy(self.menu_parent) # Удаляем меню
        mouse.locked = True # блокируем курсор
        self.MenuBool = True # Оповещаем что меню закрыто

    def __call__(self):
        return self.MenuBool
