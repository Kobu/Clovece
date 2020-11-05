

def make_abs(coords):
    return [abs(coord) for coord in coords]


def add(coords1, coords2):
    return [coords1[i] + coords2[i] for i in range(len(coords2))]


# NOTE - COMPARES ABSOLUTE VALUES
def change_lower(coords, amount):
    x, y = coords
    abs_x, abs_y = make_abs(coords)

    return [x, y + amount] if abs_x > abs_y else [x + amount, y]


# NOTE - COMPARES ABSOLUTE VALUES
def change_higher(coords, amount):
    x, y = coords
    abs_x, abs_y = make_abs(coords)

    return [x, y + amount] if abs_x < abs_y else [x + amount, y]


def change_one_direction(coords, other_coord, template):
    x = coords[0] + other_coord[0] if template[0] else coords[0]
    y = coords[1] + other_coord[1] if template[1] else coords[1]

    return [x, y]


def translate_to_negative(coords, floored_size):
    x, y = coords
    return [x - floored_size, y - floored_size]


def translate_to_normal(coords, floored_size):
    x, y = coords
    return [x + floored_size, y + floored_size]
