from ursina import Text, color
from enemy import Enemy


class ScoreManager:
    def __init__(self):
        self.score = 0
        self.level = 1
        self.score_text = Text(f'Score: {self.score}', position=(-0.85, 0.45), scale=2, color=color.white)
        self.level_text = Text(f'Level: {self.level}', position=(-0.85, 0.4), scale=2, color=color.white)

    def update_score(self, points):
        # обновляем очки, т.е. добавляем к общим очкам points
        self.score += points
        self.score_text.text = f'Score: {self.score}'
        self.check_level_up() # Вызываем проверку уровня

    def check_level_up(self):
        # првоерка повышения уровня
        if self.score >= self.level * 100:
            self.level_up() # Повышаем уровень

    def level_up(self):
        # Повышаем уровень
        self.level += 1
        self.level_text.text = f'Level: {self.level}'
        self.increase_enemy_speed() # Ускоряем противников

    def alert_boss(self):
        # Вызываем надпись босс
        alert_text = Text(f'Босс!!', position=(0, 0.4), scale=2, color=color.red)
        alert_text.fade_out(duration=3)

        
    def increase_enemy_speed(self):
        # При переходе за 100 очков повышаем скорость врагам, из метода level_up
        Enemy.speed *= 1.5
