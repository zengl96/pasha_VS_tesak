from ursina import *
from ursina.shaders import lit_with_shadows_shader


class Gun(Entity):

    muzzle_flash = False

    def __init__(self,parent, texture, model,damage=34, rotation=Vec3(0, 85, 4),position=Vec3(0.35, -0.6, 1),scale=1.5,rotationz=15,rotation_delay=0.2,delay_shoot=0.5, **kwargs):
        super().__init__(parent=parent, **kwargs)
        self.is_shooting = False
        self.bob_amplitude = 0.005
        self.bob_frequency = 4
        self.rotationz = rotationz
        self.rotation_delay = rotation_delay
        self.delay_shoot = delay_shoot
        self.damage = damage

        self.arm = Entity(
            parent=parent,
            model=model,
            texture=texture,
            rotation=rotation,
            position=position,
            scale=scale,
            shader=lit_with_shadows_shader,
            fllipped_faces=True,
            double_sided=False,
            on_cooldown=False
        )


    def activate_flash(self):
        # можно выключить этот желтый квадрат по центру
        self.muzzle_flash = Entity(parent=self, z=1, world_scale=.05, model='quad', color=color.yellow, enabled=False)

    def active(self):
        self.arm.position = self.arm.position

    def shoot(self):
        # Выстрел
        self.arm.rotation_z += self.rotationz # При выстреле меняем координату по z, как будто совершен удар
        if self.muzzle_flash:
            self.muzzle_flash.enabled = True # Включаем вспышку
            invoke(self.muzzle_flash.disable, delay=0.05) # Выключаем вспышку через 0.05с
        invoke(lambda: setattr(self.arm, 'rotation_z', self.arm.rotation_z - self.rotationz), delay=self.rotation_delay) # Поварачиваем оружие по z обратно
        invoke(setattr, self, 'is_shooting', False, delay=self.delay_shoot) # Задержка выстрела
 
    def update(self):

        if held_keys['left mouse'] and not self.is_shooting: # Если левая мышь и задержка прошла
            self.is_shooting = True # Задержка
            self.shoot() # выстрел

            # Если наш курсор на враге и у врага есть атрибуд hp, то наносим даман
            if mouse.hovered_entity and hasattr(mouse.hovered_entity, 'hp'):
                if mouse.hovered_entity.hp > 0:
                    mouse.hovered_entity.hp -= self.damage
                    mouse.hovered_entity.blink(color.red)

        # Анимация
        t = time.time() * self.bob_frequency
        self.arm.rotation_z += sin(t) * self.bob_amplitude * 10
        self.arm.rotation_x += cos(t) * self.bob_amplitude * 5

        # Если идем анимация становиться быстрее и сильнее
        if any(held_keys[k] for k in ['w', 'a', 's', 'd']):
            self.bob_amplitude = 0.03
            self.active()
        else:
            self.bob_amplitude = 0.005

