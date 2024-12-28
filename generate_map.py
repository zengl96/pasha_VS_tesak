
from landscale import Map
from terrain import MeshTerrain

terrain = ''
def generate_map():
    global terrain

    if terrain == '':
        map = Map(1371)
        terrain = MeshTerrain(map.landscale_mask)

    return terrain