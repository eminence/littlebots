
from littlebots import World, Bot
from littlebots import TILE_BLOCKED, TILE_SPAWN

import rg

#0  1   2   3   4   5   6   7   8   9   10  11  12  13  14  15  16  17  18
state_a = """
XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX 
XXX XXX XXX XXX XXX --- --- --- --- --- --- --- --- --- XXX XXX XXX XXX XXX 
XXX XXX XXX XXX --- ---                             --- --- XXX XXX XXX XXX 
XXX XXX XXX ---         a50                     a48         --- XXX XXX XXX 
XXX XXX ---     a50                                             --- XXX XXX 
XXX --- ---                                                 b50 --- --- XXX 
XXX ---     b05                                                     --- XXX 
XXX ---                                                             --- XXX 
XXX ---                                                             --- XXX 
XXX ---                                                     b50     --- XXX 
XXX ---                                                     b50     --- XXX 
XXX ---                                                             --- XXX 
XXX ---                                                             --- XXX 
XXX --- ---                                                     --- --- XXX 
XXX XXX ---     a50                                             --- XXX XXX 
XXX XXX XXX ---                                             --- XXX XXX XXX 
XXX XXX XXX XXX --- ---                             --- --- XXX XXX XXX XXX 
XXX XXX XXX XXX XXX --- --- --- --- --- --- --- --- --- XXX XXX XXX XXX XXX 
XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX 
"""


def parse_state_image(img):
    world = {}
    bots = {}
    row = 0

    for line in img.splitlines():
        col = 0
        if line == '':
            continue
        # read 3 chars at a time
        start = 0
        while start < len(line):
            cell = line[start:start+3]
            if cell == "XXX":
                world[(col, row)] = TILE_BLOCKED
            elif cell == "---":
                world[(col, row)] = TILE_SPAWN
            elif cell[0] in ("a", "b"):
                player_id = {"a":1, "b":2}[cell[0]]
                bot = Bot(prot=None, player_id=player_id, hp=int(cell[1:]))
                bot.location = (col, row)
                bots[(col, row)] = bot
            start += 4
            col += 1
        row += 1


    return world, bots

def test_parse_state():
    "Make sure that we can correctly parse a textual gamestate"
    world, bots = parse_state_image(state_a)
    assert world[(0,0)] == TILE_BLOCKED
    assert world[(8,0)] == TILE_BLOCKED
    assert world[(8,1)] == TILE_SPAWN
    assert world[(14,16)] == TILE_SPAWN
    assert world[(14,17)] == TILE_BLOCKED
    assert world[(14,18)] == TILE_BLOCKED
    assert bots[(6,3)].player_id == 1
    assert bots[(6,3)].hp == 50
    assert bots[(12,3)].player_id == 1
    assert bots[(12,3)].hp == 48
    assert bots[(3,6)].player_id == 2
    assert bots[(3,6)].hp == 5

class TestRG:
    def setup_class(cls):
        world_map, bots = parse_state_image(state_a)
        settings = {
            'spawn_coords': [loc for loc, tile in world_map.items() if tile == TILE_SPAWN],
            'obstacles': [loc for loc, tile in world_map.items() if tile == TILE_BLOCKED],
            "width": 19,
            "height": 19,
            }
        rg.set_settings(rg.AttrDict(settings))
    def test_dist(self):
        p1 = (0,0)
        p2 = (3,4)
        d = rg.dist(p1, p2)
        assert d == 5

    def test_wdist(self):
        p1 = (0,0)
        p2 = (3,4)
        d = rg.wdist(p1, p2)
        assert d == 7

    def test_loctypes(self):
        assert rg.loc_types((0,0)) == set(["normal", "obstacle"])
        assert rg.loc_types((-1,0)) == set(["invalid"])
        assert rg.loc_types((0,-1)) == set(["invalid"])
        assert rg.loc_types((6,0)) == set(["normal", "obstacle"])
        assert rg.loc_types((6,1)) == set(["normal", "spawn"])
        assert rg.loc_types((6,2)) == set(["normal"])
        assert rg.loc_types((6,3)) == set(["normal"])

    def test_locs_around(self):
        locs = set(rg.locs_around((0,0)))
        assert locs == set(((0, 1), (1, 0), (0, -1), (-1, 0)))
        
        locs = set(rg.locs_around((10, 100)))
        assert locs == set(((10, 101), (11, 100), (10, 99), (9, 100)))
        
        locs = set(rg.locs_around((0,0), filter_out=["invalid"]))
        assert locs == set(((0, 1), (1, 0)))

    def test_toward(self):
        me = (10,10)
        dest = (0,0)
        toward = rg.toward(me, dest)
        assert toward in [(9,10), (10,9)]

        dest = (10,12)
        toward = rg.toward(me, dest)
        assert toward == (10,11)
        
        dest = (10,10)
        toward = rg.toward(me, dest)
        assert toward == (10,10)




        
