from ursina import *
from random import randint
from player import create_player



class MenuButton(Button):
    def __init__(self, text='',scale=(.25, .075), **kwargs):
        super().__init__(text, scale=scale, highlight_color=color.azure, z=-1, **kwargs)

        for key, value in kwargs.items():
            setattr(self, key ,value)

class Main_Menu:
    def __init__(self):
        
        self.player = create_player()
        self.skins = ['textures/t.jpeg', 'textures/6.jpg', 'textures/ars.png', 'textures/art.png']
        self.MenuBool = False
        mouse.locked = False # Разблокируем курсор
        self.menu_parent = Entity(parent=camera.ui, y=.1, z=-1, ignore_paused=True)  # Установить z ближе к камере
        self.main_menu = Entity(parent=self.menu_parent, z=-1, ignore_paused=True)  # Тоже установить ближе
        self.options_menu = Entity(parent=self.menu_parent, z=-1, ignore_paused=True)

        self.state_handler = Animator({
            'main_menu' : self.main_menu,
            'options_menu' : self.options_menu,
            }
        )

        self.main_menu.buttons = [
            MenuButton('start', on_click=Sequence(Wait(.01), Func(self.start_game), 'warning')),
            MenuButton('options', on_click=Func(setattr, self.state_handler, 'state', 'options_menu')),
            MenuButton('quit', on_click=Func(application.quit)),
        ] 


        button_spacing = .075 * 1.25
        for i, e in enumerate(self.main_menu.buttons):
            e.parent = self.main_menu
            e.y = (-i - 2) * button_spacing
            e.z = -1  # Кнопки тоже ближе к камере

        review_text = Text(parent=self.options_menu, y=.25, text='Настрйоки', origin=(-.5,0), z=-1)
        review_text.ignore_paused = True
        for t in [e for e in scene.entities if isinstance(e, Text)]:
            t.original_scale = t.scale

        text_scale_slider = Slider(0, 2, default=1, step=.1, dynamic=True, text='Text Size:', parent=self.options_menu,x=-.25, z=-1)
        text_scale_slider.ignore_paused = True
        text_scale_slider.knob.ignore_paused = True
        def set_text_scale():
            for t in [e for e in scene.entities if isinstance(e, Text) and hasattr(e, 'original_scale')]:
                t.scale = t.original_scale * text_scale_slider.value
        text_scale_slider.on_value_changed = set_text_scale



        volume_slider = Slider(0, 1, default=Audio.volume_multiplier, step=.1, text='Master Volume:',ignore_paused=True, parent=self.options_menu, x=-.25, z=-1)
        volume_slider.ignore_paused = True
        volume_slider.knob.ignore_paused = True
        def set_volume_multiplier():
            Audio.volume_multiplier = volume_slider.value
        volume_slider.on_value_changed = set_volume_multiplier

        options_back = MenuButton(parent=self.options_menu, text='Back', x=-.25, origin_x=-.5, on_click=Func(setattr, self.state_handler, 'state', 'main_menu'))
        options_back.ignore_paused = True
        for i, e in enumerate((text_scale_slider, volume_slider, options_back)):
            e.y = -i * button_spacing

        self.your_skin = Entity(parent=self.options_menu, texture=self.player.texture, model='cube',x=-.6, y=-0.1, ignore_paused = True, z=-1, scale=(0.3,0.3,0.3))

        self.triangle_next = MenuButton(parent=self.options_menu, model=Cone(2), scale=(0.1, 0.1),rotation=(0, 0, 90), position=(-0.5, -0.4))
        self.triangle_next.on_click = self.switched_skins_next

        self.triangle_prev = MenuButton(parent=self.options_menu, model=Cone(2), scale=(0.1, 0.1),rotation=(0, 0, -90), position=(-0.7, -0.4))
        self.triangle_prev.on_click = self.switched_skins_perv 


        # Создаем бэкграунд
        background = Entity(
            parent=self.menu_parent, 
            model='cube', 
            texture=f'textures/{randint(1, 5)}.jpg', 
            scale=(camera.aspect_ratio, 1), 
            world_y=0,
            z=-1.1  # Задний фон чуть дальше кнопок
        )


    def switched_skins_next(self):

        try:
            text_pl = self.player.texture
            count = -1
            for i in self.skins:
                count += 1
                if str(text_pl) in i:
                    break
            self.player.texture = self.your_skin.texture = self.skins[count+1]
        except: pass

    def switched_skins_perv(self):

        try:
            text_pl = self.player.texture
            count = -1
            for i in self.skins:
                count += 1
                if str(text_pl) in i:
                    break
            self.player.texture = self.your_skin.texture = self.skins[count-1]
        except: pass

    def start_game(self):

        application.resume()
        self.menu_parent.disable()
        mouse.locked = True
        self.MenuBool = True

    def enable_menu(self):

        application.pause()
        self.menu_parent.enable()
        mouse.locked = False
        self.MenuBool = False 

    def __call__(self):
        return self.MenuBool




# for i in application.sequences:
#     if i.args[-1] != 'warning':
#         print(i)
#         i.pause()