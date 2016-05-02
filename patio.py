#!/usr/bin/python
import sys
from random import shuffle

"""
Everything here is done in 'units'.  In this particular case it's going to be
6" which is the least common factor in the tiles from which we can choose.
"""


class PatioTile(object):
    def __init__(self, short_name, name, x, y):
        self.short_name = short_name
        self.name = name   # for easy identification in reports
        self.x = x         # one side in 'units'
        self.y = y         # the other side in 'units'


class Patio(object):
    """
    Patio: primarily a 2-dimensional array of PatioSpace objects.
    x_max and y_max represent the rectangular bounding box
    which contains all of the patio.  The (0, 0) location is the
    upper left and "X" proceeds to the right and "Y" proceeds down.
    patio_map: 2d array of True/False/Nones (tile present; tile not present; not part of patio)
        (must have equal number of elements per row)
    tile_choices: array of PatioTile objects to choose from
    """
    def __init__(self, patio_map, tile_choices):
        self.patio_map = patio_map
        self.max_x = len(patio_map[0])
        self.max_y = len(patio_map)

        # Make a rotation of every tile and save that to the list;
        # This is simpler than handling the logic elsewhere.  There will be 2
        # tiles of the same name in the list for every one we initially add.  One for
        # the inital orientation and one with a 90 degree rotation.
        tc = tile_choices[:]
        for tile in tile_choices:
            new_tile = PatioTile(tile.short_name, tile.name, tile.y, tile.x)
            tc.append(new_tile)
        self.tile_choices = tc

    def __str__(self):
        me = ''
        for row in self.patio_map:
            for tile_space in row:
                if tile_space is None:
                    me += '_'
                else:
                    if tile_space:
                        me += tile_space
                    else:
                        me += 'O'
            me += '\n'  # new row
        return me

    def add_randomly(self):
        # find first free space
        space = self.first_free_space()

        # shuffle tiles and try to add until we try all
        for tile in shuffle(self.tile_choices):
            if self.tile_will_fit(space, tile):
                return self.add_tile(space, tile)
        return False

    def first_free_space(self):
        # Returns an (x, y) tuple of the first available space to put a tile
        for x, row in enumerate(self.patio_map):
            for y, tile_space in enumerate(row):
                if tile_space is not None and not tile_space:
                    return (x, y)
        return None

    def patio_complete(self):
        if self.first_free_space() is None:
            return True
        return False

    def add_tile(self, space, tile):
        for (xvalue, yvalue) in spaces_tile_would_cover(space, tile):
            self.patio_map[xvalue][yvalue] = tile.short_name

    def tile_will_fit(self, space, tile):
        (x, y) = space

        # first make sure we're on the map at all
        if x > self.max_x or y > self.max_y:
            return None

        # now see if the tile will fit in the bounds of the patio whether or not
        # there is already a tile in the way
        if x+tile.x > self.max_x or y+tile.y > self.max_y:
            return False

        # now check to see if all the spaces are free that the tile would occupy
        for (xvalue, yvalue) in spaces_tile_would_cover(space, tile):
                if self.patio_map[xvalue][yvalue] is None or self.patio_map[xvalue][yvalue]:
                    return False
        # we didn't run into trouble, it's fine!
        return True

    def spaces_tile_would_cover(space, tile):
        (x, y) = space
        spaces_would_cover = ()
        for xvalue in range(x, x+tile.x+1):
            for yvalue in range(y, y+tile.y+1):
                spaces_would_cover.append((xvalue, yvalue))
        return spaces_would_cover


simple_patio_space_map = [[None, False, False, False],
                          [False, False, False],
                          [False, False, None, None]]

tile_a = PatioTile('A', '12x12', 2, 2)
tile_b = PatioTile('B', '12x24', 2, 4)
tile_c = PatioTile('C', '24x36', 4, 6)
tile_d = PatioTile('D', '18x24', 3, 4)
tile_e = PatioTile('E', '24x24', 4, 4)
tile_f = PatioTile('F', '18x36', 3, 6)
simple_tile_choices = [tile_a, tile_b, tile_c, tile_d, tile_e, tile_f]

foo = Patio(simple_patio_space_map, simple_tile_choices)
print foo

while(not foo.patio_complete):
    foo.add_randomly

print foo


# class SquarePatioTile(PatioTile):
#     def __init__(self, x):
#         super(self.__class__, self).__init__(x, x)
