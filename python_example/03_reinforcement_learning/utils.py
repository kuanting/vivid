import numpy as np

def load_spawn_points(path):
    coords = []
    with open(path, 'r') as f:
        for l in f:
            coord = list(map(float, l.strip()[1:-1].split(',')))
            coords.append(coord)

    coords = np.array(coords, dtype=np.float)
    return coords
