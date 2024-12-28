

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
    print(enemy.y)
    # Анимация движения вверх-вниз
    def update_mark():
        mark.y = 1.4 + 0.05 * math.sin(time.time() * 6)  # Колебания по оси Y

    # Добавляем обновление к анимации
    mark.update = update_mark
    return mark

# m = []
# for i in range(100):
#     t = 0.03*math.sin(time.time() * 2)
#     print(t)
#     time.sleep(0.1)