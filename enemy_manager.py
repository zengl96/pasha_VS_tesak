from enemy import Boss, Enemy
from random import uniform
import random

class EnemyManager:
    def __init__(self, player, terrain):
        self.subject = player
        self.terrain = terrain
        self.enemies = []
        self.boss = []

    def remove_enemy(enemy):
        """Удаляет врага или босса из игры."""
        if isinstance(enemy, Boss):
            boss.remove(enemy)  # Удалить из списка боссов
        else:
            enemies.remove(enemy)  # Удалить из списка врагов


    def update(self,shootables_parent, score_manager, game_state):
        if game_state == 'gameplay':

            if len(self.enemies) == 0 and score_manager.level < 5:
                self.enemies = [Enemy(score_manager=score_manager, on_death_callback=self.remove_enemy, player=self.subject,
                                shootables_parent=shootables_parent, lst_enemies=self.enemies, x=random.uniform(10, 100),
                                z=random.uniform(10, 100)) for _ in range(4)]
            elif score_manager.level == 5:
                if len(self.boss) == 0:
                    camera.enabled = False
                    gun.disable()
                    score_manager.alert_boss()
                    self.boss = [Boss(speed=0, score_manager=score_manager, on_death_callback=self.remove_enemy, player=self.subject,
                                shootables_parent=shootables_parent, x=random.uniform(10, 100), z=random.uniform(10, 100)) for
                            _ in
                            range(1)]
                    dialogs = Dialog(distance_max=100000, character=self.boss[0], player=self.subject, dialog_dict={'person_1':'Тесак: СУКА, красный гандон тоби пизда!','enemy_1':'Паша: Нет, я выебу тебя!','person_2':'Тесак: Тебе только парашу убирать!', 'enemy_2':'Паша: Мне пизда!'})

                if dialogs() == False:
                    return
                elif dialogs() == True:
                    gun.enable()
                    self.boss[0].speed = 1
                    
            if score_manager.score > 1000:
                Boss(speed=1, score_manager=score_manager, on_death_callback=self.remove_enemy, player=self.subject,
                    shootables_parent=shootables_parent, x=random.uniform(10, 100), z=random.uniform(10, 100))

