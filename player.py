from ursina import Entity, color
from ursina.collider import BoxCollider
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina import *

def create_player():
    subject = FirstPersonController(
        model='cube',
        x=50, 
        z=50,
        color=color.orange,
        origin_y=-.5,
        speed=8,
        collider='box',
        texture=r'textures\t.jpeg'
    )


    subject.collider = BoxCollider(subject, Vec3(0, 1, 0), Vec3(1, 2, 1))

    subject.gravity = 0.0

    return subject