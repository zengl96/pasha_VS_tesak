
from ursina import *



class MapUpdate:

    def __init__(self, subject, terrain, count,grass_audio, water_swim, pX, pZ):
        self.subject = subject
        self.terrain = terrain
        self.count = count
        self.grass_audio = grass_audio
        self.water_swim = water_swim
        self.pX = pX
        self.pZ = pZ

    def update_map(self):

        self.count += 1
        if self.count == 4:
            self.count = 0
            self.terrain.update(self.subject.position, camera)

        # Change subset position based on self.subject position.
        if abs(self.subject.x - self.pX) > 1 or abs(self.subject.z - self.pZ) > 1:
            self.pX = self.subject.x
            self.pZ = self.subject.z

            if self.subject.y >= 0 and self.grass_audio.playing == False:
                self.grass_audio.pitch = random.random() + 0.7
                self.grass_audio.play()
            elif self.subject.y < 0 and self.water_swim.playing == False:
                self.water_swim.pitch = random.random() + 0.3
                self.water_swim.play()

        blockFound = False
        height = 1.76

        x = floor(self.subject.x + 0.5)
        z = floor(self.subject.z + 0.5)
        y = floor(self.subject.y + 0.5)
        for step in range(-2, 2):
            if self.terrain.td.get((x, y + step, z)) == "t":
                # ***
                # Now make sure there isn't a block on top...
                if self.terrain.td.get((x, y + step + 1, z)) != "t":
                    target = y + step + height
                    blockFound = True
                    break
                else:
                    target = y + step + height + 1
                    blockFound = True
                    break
        if blockFound == True:
            self.subject.y = lerp(self.subject.y, target, 6 * time.dt)
        else:
            self.subject.y -= 9.8 * time.dt




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