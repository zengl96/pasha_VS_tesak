
from ursina import *


def update(subject,terrain, count,grass_audio, water_swim, pX, pZ):

    count += 1
    if count == 4:
        count = 0
        terrain.update(subject.position, camera)

    # Change subset position based on subject position.
    if abs(subject.x - pX) > 1 or abs(subject.z - pZ) > 1:
        pX = subject.x
        pZ = subject.z

        if subject.y >= 0 and grass_audio.playing == False:
            grass_audio.pitch = random.random() + 0.7
            grass_audio.play()
        elif subject.y < 0 and water_swim.playing == False:
            water_swim.pitch = random.random() + 0.3
            water_swim.play()

    blockFound = False
    height = 1.76

    x = floor(subject.x + 0.5)
    z = floor(subject.z + 0.5)
    y = floor(subject.y + 0.5)
    for step in range(-2, 2):
        if terrain.td.get((x, y + step, z)) == "t":
            # ***
            # Now make sure there isn't a block on top...
            if terrain.td.get((x, y + step + 1, z)) != "t":
                target = y + step + height
                blockFound = True
                break
            else:
                target = y + step + height + 1
                blockFound = True
                break
    if blockFound == True:
        subject.y = lerp(subject.y, target, 6 * time.dt)
    else:
        subject.y -= 9.8 * time.dt




def update_for_enemy(subject, terrain, count, pX, pZ):

    count += 1
    if count == 4:
        count = 0
        terrain.update(subject.position, camera)

    # Change subset position based on subject position.
    if abs(subject.x - pX) > 1 or abs(subject.z - pZ) > 1:
        pX = subject.x
        pZ = subject.z



    blockFound = False
    height = 1

    x = floor(subject.x + 0.5)
    z = floor(subject.z + 0.5)
    y = floor(subject.y + 0.5)
    for step in range(-2, 2):
        if terrain.td.get((x, y + step, z)) == "t":
            # ***
            # Now make sure there isn't a block on top...
            if terrain.td.get((x, y + step + 1, z)) != "t":
                target = y + step + height
                blockFound = True
                break
            else:
                target = y + step + height + 1
                blockFound = True
                break
    if blockFound == True:
        subject.y = lerp(subject.y, target, 6 * time.dt)
    else:
        subject.y -= 9.8 * time.dt