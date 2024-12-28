from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

from enemy import Boss, Enemy
from gun import Gun
from score_and_lvl import ScoreManager
from terrain import MeshTerrain
from random import random
from landscale import Map
from UrsinaLighting import LitDirectionalLight, LitPointLight, LitSpotLight, LitObject, LitInit
from ursina.shaders import lit_with_shadows_shader
from player import create_player
import random
from dialog import Dialog
from gamestate import game_state
import map_update
from Menu import Main_Menu

if __name__ == '__main__': app = Ursina()

lit = LitInit()  # Загружаем свет

subject = create_player() # Создаем игрока (там нехуй менять)


# координаты
pX = subject.x 
pZ = subject.z


# сцена
scene.fog_density = (0, 95)
scene.fog_color = color.gray


# загружаем аудио
Audio('assets/thykier-the-limit.mp3', True)
grass_audio = Audio('assets/step.ogg', autoplay=False, loop=False)
water_swim = Audio('assets/water-swim.mp3', autoplay=False, loop=False)
arm_texture = load_texture('assets/arm_texture.png')
skyboxTexture = Texture("textures/skybox.jpg")

# Генерим карту
map = Map(1371)
terrain = MeshTerrain(map.landscale_mask)

skybox = Sky(model="sphere", double_sided=True, texture=skyboxTexture, rotation=(0, 90, 0))
water = LitObject(position=(floor(terrain.subWidth / 2), -0.1, floor(terrain.subWidth / 2)), scale=terrain.subWidth,
                  water=True, cubemapIntensity=0.75, collider='box', texture_scale=(terrain.subWidth, terrain.subWidth),
                  ambientStrength=0.5)


# Объект очков и уровня (тут тоже нехуй менять)
score_manager = ScoreManager()



# Создания первого оружия (тут тоже нехуй менять)
gun = Gun(parent=camera, model='assets/uploads_files_2614590_Shotgun_Model.obj',
          texture=r'textures\Shotgun_HDRP_BaseMap.png', rotationz=1, rotation_delay=0.05, delay_shoot=0.05)
gun.activate_flash()


# Добавление вспышки при выстреле
shootables_parent = Entity()
mouse.traverse_target = shootables_parent




def remove_enemy(enemy):
    """Удаляет врага или босса из игры."""
    """Новые типы врагов сюда заноси что они могли удалиться"""
    if isinstance(enemy, Boss):
        boss.remove(enemy)  # Удалить из списка боссов
    else:
        enemies.remove(enemy)  # Удалить из списка врагов


# Создание врагов
enemies = []
boss = []
dialogs = []


# Существует объект или нет
def destroy_or_not(objects):
    try:
        print(objects)
        return False
    except:
        return True



# Создаем меню
menu = Main_Menu()



def pause_input(key):
    global menu
    if key == 'escape' and destroy_or_not(menu.menu_parent):
        """Если esc нажат игра ставиться на паузу и генериться меню"""
        application.pause()
        menu = Main_Menu()


# pause_handler = Entity(ignore_paused=True, input=pause_input)
pause_handler = Entity(ignore_paused=True, input=pause_input)
print('424242')
print('fdsfsdds')
count = 0

def update():
    global enemies, boss, dialogs, game_state, men_count, menu
    global count, pX, pZ

    # Обновление карты(тут нехуй менять)
    map_update.update(subject,terrain, count,grass_audio, water_swim, pX, pZ)


    # Если у нас открыто меню, то игра дальше не продолжается
    if menu() == False:
        return

    
    if game_state == 'dialog':

        if score_manager.score == 0:
            # Проверку выше надо будет поменять
            gun.disable() # Скрываем оружие
            if enemies == []:
                # Если на карте нету никого создаем врага
                camera.enabled = False
                gun.disable()
                enemies = [Enemy(speed=0, score_manager=score_manager, on_death_callback=remove_enemy, player=subject,
                                shootables_parent=shootables_parent, lst_enemies=enemies,x=60,z=60)] # Создание врага, можешь создавать любого(можно дохуя че поменять там внутри класса)
                dialogs = Dialog(character=enemies[0], player=subject, dialog_dict={'person_1':'Тесак: Паша, ты пидорас!','enemy_1':'Паша: Нет, я гандон!','person_2':'Тесак: отсоси мой член сучка', 'enemy_2':'Паша: Я хочу', 'person_3':'Тесак: окрыляй педофиляй'})
                # Создаем диалог(внутри класса тоже дохуя аттрибутов)
            

            dialogs.update() # обновляем диалог
            if dialogs() == False:
                return  # Если диалог еще идет то дальше игра не идет
            elif dialogs() == True:
                game_state = 'gameplay' # Меняем режим на игру
                destroy(enemies[0]) # Удаляем персонажа
                enemies = [] # Чистим список
                gun.enable() # Показываем оружие


    if game_state == 'gameplay':

        if len(enemies) == 0 and score_manager.level < 5:
            enemies = [Enemy(score_manager=score_manager, on_death_callback=remove_enemy, player=subject,
                            shootables_parent=shootables_parent, lst_enemies=enemies, x=random.uniform(10, 100),
                            z=random.uniform(10, 100)) for _ in range(4)] # просто создаем 4 врагов пока уровень не будет 5
        elif score_manager.level == 5:
            if len(boss) == 0:
                # если босса нет на карте
                camera.enabled = False 
                gun.disable() # Скрываем оружие
                score_manager.alert_boss() # Вызываем надпись босс
                boss = [Boss(speed=0, score_manager=score_manager, on_death_callback=remove_enemy, player=subject,
                            shootables_parent=shootables_parent, x=random.uniform(10, 100), z=random.uniform(10, 100)) for
                        _ in range(1)]  # Создаем босса, так же как Enemy
                dialogs = Dialog(distance_max=100000, character=boss[0], player=subject, dialog_dict={'person_1':'Тесак: СУКА, красный гандон тоби пизда!','enemy_1':'Паша: Нет, я выебу тебя!','person_2':'Тесак: Тебе только парашу убирать!', 'enemy_2':'Паша: Мне пизда!'})
                # Создаем диалог который будет вызваться сразу из за distance_max=100000

            dialogs.update() # ОБновляем наш диалог
            if dialogs() == False:
                return # Если диалог еще идет то дальше игра не идет
            elif dialogs() == True: # Если диалог закончился
                gun.enable()  # Возращаем оружие
                boss[0].speed = 1 # Даем боссу скорость, что бы он двигался
                
        if score_manager.score > 1000:
            Boss(speed=1, score_manager=score_manager, on_death_callback=remove_enemy, player=subject,
                shootables_parent=shootables_parent, x=random.uniform(10, 100), z=random.uniform(10, 100))


# Принятие входяящих клавиш с клавиатуры
# pause_handler = Entity(ignore_paused=True, input=pause_input)
terrain.genTerrain()




if __name__ == '__main__': app.run()