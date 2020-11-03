# change_lower
# change_higher
# add to coord
# abs


class Coords:

    def __init__(self, x=None, y=None, value: list = None):
        self._x = x
        self._y = y

        if value:
            self.value = value
        else:
            self.value = [x, y]

    def __abs__(self):
        return Coords(abs(self._x), abs(self._y))

    def __add__(self, other):
        if isinstance(other, Coords):
            first_value = self.value[0] + other.value[0]
            second_value = self.value[1] + other.value[1]
            return Coords(first_value, second_value)
        else:
            raise TypeError()

    def __str__(self):
        return str(self.value)

    def __iter__(self):
        return iter((self._x, self._y))

    # TODO keep in mind it COMPARES ABSOLUTE VALUES
    def change_lower(self, amount):
        abs_coords = abs(self)
        return Coords(self._x, self._y + amount) if abs_coords._x > abs_coords._y else Coords(self._x + amount, self._y)

    def change_higher(self, amount):
        abs_coords = abs(self)
        return Coords(self._x, self._y + amount) if abs_coords._x < abs_coords._y else Coords(self._x + amount, self._y)

    # TODO add this to coord_system
    def change_one_direction(self, other_coord, template):
        x = self._x + other_coord._x if template[0] else self._x
        y = self._y + other_coord._y if template[1] else self._y

        return Coords(x, y)

    def translate_to_negative(self, floored_size):
        x, y = self
        return Coords(x - floored_size, y - floored_size)

    def translate_to_normal(self, floored_size):
        x, y = self
        return Coords(x + floored_size, y + floored_size)
