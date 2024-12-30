

from ursina import *

def activatemark(enemy):

    # print(enemy.world_position)
    # Создаем метку в виде перевернутой пирамиды
    mark = Entity(
        parent=enemy,
        model=Cone(3),           # Модель конуса
        color=color.green,      # Цвет зелёный
        rotation=(180, 0, 0),    # Переворачиваем конус вверх ногами
        world_scale=(1.5,1,1)
    )
    # Анимация движения вверх-вниз
    def update_mark():
        mark.y = 1.4 + 0.05 * math.sin(time.time() * 6)  # Колебания по оси Y

    # Добавляем обновление к анимации
    mark.update = update_mark
    return mark


def black_screen(text, duration):
    application.pause()

    # Создаем черный экран
    black_screen = Entity(model='quad',parent=camera.ui, color=color.black, scale=(10, 10), alpha=0, z=-1)
    label = Text(text=text, origin=(0, 0), scale=2, color=color.white, alpha=0, z=-1.1)

    # Плавное появление черного экрана
    black_screen.animate('alpha', 1, duration=1)
    
    invoke(label.animate, 'alpha', 1, duration=duration/2,delay=duration)


    # Плавное исчезновение через заданное время
    def fade_out():
        black_screen.animate('alpha', 0, duration=duration)
        label.animate('alpha', 0, duration=duration)

    # Задержка перед исчезновением
    invoke(fade_out, delay=duration+1)
    invoke(application.resume, delay=duration*1.5+1.2)