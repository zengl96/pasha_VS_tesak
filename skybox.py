from ursina import Sky, Texture

def setup_skybox():
    skybox_texture = Texture("textures/skybox.jpg")
    Sky(model="sphere", double_sided=True, texture=skybox_texture, rotation=(0, 90, 0))
