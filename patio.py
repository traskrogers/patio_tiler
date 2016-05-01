#!/usr/bin/python
import sys

"""
Everything here is done in 'units'.  In this particular case it's going to be
6" which is the least common factor in the tiles from which we can choose.
"""


class PatioTile(object):
    def __init__(self, name, x, y):
        self.name = name   # for easy identification in reports
        self.x = x         # one side in 'units'
        self.y = y         # the other side in 'units'


class Patio(object):
    """
    Patio: primarily a 2-dimensional array of PatioSpace objects.
    x_max and y_max represent the rectangular bounding box
    which contains all of the patio.  The (0, 0) location is the
    upper left and "X" proceeds to the right and "Y" proceeds down.
    patio_map: 2d array of PatioSpace objects (or None if there is no patio there)
        (must have equal number of elements per row)
    tile_choices: array of PatioTile objects to choose from
    """
    def __init__(self, patio_map, tile_choices):
        self.patio_map = patio_map
        self.max_x = len(patio_map[0])
        self.max_y = len(patio_map)
        self.tile_choices = tile_choices

    def __str__(self):
        me = ''
        for row in self.patio_map:
            for tile_space in row:
                if tile_space is None:
                    me += '_'
                else:
                    if tile_space.is_covered:
                        me += 'X'
                    else:
                        me += 'O'
            me += '\n'  # new row
        return me


class PatioSpace(object):
    def __init__(self):
        self.is_covered = False


simple_patio_space_map = [[None, PatioSpace(), PatioSpace(), PatioSpace()],
                          [PatioSpace(), PatioSpace(), PatioSpace()],
                          [PatioSpace(), PatioSpace(), None, None]]

tile_a = PatioTile('12x12', 2, 2)
tile_b = PatioTile('12x24', 2, 4)
tile_c = PatioTile('24x36', 4, 6)
tile_d = PatioTile('18x24', 3, 4)
tile_e = PatioTile('24x24', 4, 4)
tile_f = PatioTile('18x36', 3, 6)
simple_tile_choices = [tile_a, tile_b, tile_c, tile_d, tile_e, tile_f]

foo = Patio(simple_patio_space_map, simple_tile_choices)
print foo

# class SquarePatioTile(PatioTile):
#     def __init__(self, x):
#         super(self.__class__, self).__init__(x, x)
