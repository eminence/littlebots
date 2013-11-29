import json
import sys

import rg

def recv():
    return json.loads(input())

def send(o):
    print(json.dumps(o))

def debug(*args):
    print(*args, file=sys.stderr)

def runrobot(factory):
    r = factory()
    
    worldinfo = recv()
    width = worldinfo['width']
    height = worldinfo['height']
    blocks = worldinfo['blocks']
    spawns = worldinfo['spawns']
    settings = worldinfo['settings']
    settings.update({
        "spawn_coords": spawns,
        "obstacles": blocks,
        "width": width,
        "height": height,
        })

    rg.set_settings(settings)

    
    rg.CENTER_POINT = (int(width / 2), int(height / 2))
    
    while True:
        world = recv()
        
        robots = {}
        for bot in world['robots']:
            bot['location'] = tuple(bot['location'])
            robots[tuple(bot['location'])] = rg.AttrDict(bot)
        world['robots'] = robots
        
        for attr, val in world['local'].items():
            setattr(r, attr, val)
        r.location = tuple(r.location)
        
        result = r.act(rg.AttrDict(world))
        send(result)
