from ursina import *
import math


from ursina import *


class Dialog(Entity):

    DialogTrigger  = False
    EndDialog = False

    def __init__(self, character, player, dialog_dict, distance_max=5):
        # super().__init__()
        self.character = character
        self.player = player
        self.dialog_dict = dialog_dict
        self.dialog_index = -1
        self.player = player
        self.camera = camera
        self._ = True
        self.next_dialog = True
        self.distance_max = distance_max


    def show_dialog_window(self):
        self.player.speed = 0
        self.player.camera_pivot.z = -5.5  
        self.player.camera_pivot.y = 5.5 
        self.player.camera_pivot.x = 5.5 
        self.camera.enabled = False
        self.button = Button(scale=(1.5,.2), position=(0, -0.35), text='')
        self.velocity_y = 0

        self.side_texture = Entity(
            parent=self.button,
            model='quad',
            texture=self.character.texture, 
            scale=(0.1, 0.8), 
            position=(-0.4, 0)  
        )
        self.side_texture2 = Entity(
            parent=self.button,
            model='quad',
            texture=self.player.texture,  
            scale=(0.1, 0.8), 
            position=(0.4, 0)  
        )


    def animate_text(self, text):
        for i in range(len(text)):
            invoke(setattr, self.button, 'text', text[:i+1], delay=i * 0.05)
        invoke(setattr, self, 'next_dialog', True, delay=len(text) * 0.051)



    def show_next_dialog(self):
        if self.dialog_index < len(self.dialog_dict):
            en_or_pers = list(self.dialog_dict.keys())[self.dialog_index]
            if 'person' in en_or_pers:
                self.side_texture.disable()
                self.side_texture2.enable()
            else:
                self.side_texture2.disable()
                self.side_texture.enable()

            text_to_display = list(self.dialog_dict.values())[self.dialog_index]
            self.animate_text(text_to_display)

        else:
            return self.end_dialog()  

    def end_dialog(self):

        destroy(self.button)
        self.player.camera_pivot.z = 0  
        self.player.camera_pivot.y = 2 
        self.player.camera_pivot.x = 0 
        self.camera.enabled = True
        self.player.speed = 8
        self.EndDialog = True

        return ''

    def update(self):

        if self.EndDialog == False:

            distance = ((self.player.x - self.character.x)**2 + (self.player.z - self.character.z)**2)**0.5
            if distance < self.distance_max:

                if self.DialogTrigger == False:
                    self.show_dialog_window()
                    self.DialogTrigger = True

                if held_keys['left mouse'] and self._ == True and self.next_dialog == True:
                    self.next_dialog = False
                    self.dialog_index += 1
                    self._ = False
                    return self.show_next_dialog()
                if not held_keys['left mouse']:
                    self._ = True


    def __call__(self):
        return self.EndDialog