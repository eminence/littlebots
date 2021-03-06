# users will import rg to be able to use robot game functions
from math import sqrt
from collections import MutableMapping

settings = None

# constants

CENTER_POINT = None

class AttrDict(MutableMapping):
    def __init__(self, *args, **kwargs):
        self.__dict__.update(*args, **kwargs)
    def __getitem__(self, key):
        return self.__getattribute__(key)
    def __setitem__(self, key, val):
        self.__setattr__(key, val)
    def __delitem__(self, key):
        self.__delattr__(key)
    def __iter__(self):
        return iter(self.__dict__)
    def __repr__(self):
        return repr(self.__dict__)
    def __len__(self):
        return len(self.__dict__)


def set_settings(s):
    global settings
    if not isinstance(s, AttrDict):
        s = AttrDict(s)
    settings = s

##############################

def dist(p1, p2):
    return sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

def wdist(p1, p2):
    return abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])

def memodict(f):
    """ Memoization decorator for a function taking a single argument """
    class memodict(dict):
        def __missing__(self, key):
            ret = self[key] = f(key)
            return ret
    return memodict().__getitem__

@memodict
def loc_types(loc):
    if not (0 <= loc[0] < settings.width):
        return set(['invalid'])
    if not (0 <= loc[1] < settings.height):
        return set(['invalid'])
    types = set(['normal'])
    if loc in settings.spawn_coords:
        types.add('spawn')
    if loc in settings.obstacles:
        types.add('obstacle')
    return types

@memodict
def _locs_around(loc):
    x, y = loc
    offsets = ((0, 1), (1, 0), (0, -1), (-1, 0))
    return [(x+dx, y+dy) for dx, dy in offsets]

def locs_around(loc, filter_out=None):
    filter_out = set(filter_out or [])
    return [loc for loc in _locs_around(loc) if
            len(filter_out & loc_types(loc)) == 0]

def toward(curr, dest):
    if curr == dest:
        return curr

    x0, y0 = curr
    x, y = dest
    x_diff, y_diff = x - x0, y - y0

    if abs(x_diff) < abs(y_diff):
        return (x0, y0 + y_diff / abs(y_diff))
    return (x0 + x_diff / abs(x_diff), y0)
