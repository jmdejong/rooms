
import random
import ground
import gameobjects
import grid
import event
import entity


class Room:
    
    
    def __init__(self, name, data):
        self.name = name
        self.width = data["width"]
        self.height = data["height"]
        #self.updateEvent = event.Event()
        self.entrance = tuple(data["spawn"])
        
        self.events = {
            "update": event.Event(),
            "control": event.Event()
            }
        
        self.places = data.get("places", {})
        
        self.field = {}
        
        g = grid.fromDict(data)
        for x in range(g.width):
            for y in range(g.height):
                val = g.get(x, y)
                if not isinstance(val, list) :
                    val = [val]
                for obj in val:
                    if isinstance(obj, str):
                        objtype = obj
                        args = []
                        kwargs = {}
                    elif isinstance(obj, dict):
                        objtype = obj["type"]
                        args = obj.get("args", [])
                        kwargs = obj.get("kwargs", {})
                    else:
                        continue
                    self.addObj((x, y), self.makeObject(objtype, *args, **kwargs))
        
    
    def getEntrance(self):
        return self.entrance
    
    def update(self):
        self.events["control"].trigger(1)
        self.events["update"].trigger()
    
    def getSprite(self, pos):
        return self._getGround(pos).getTopObj().getSprite()
    
    def isValidPos(self, pos):
        x, y = pos
        return x >= 0 and y >= 0 and x < self.width and y < self.height
    
    def _getGround(self, pos):
        if pos not in self.field and self.isValidPos(pos):
            groundPatch = ground.GroundPatch(self, pos)
            self.field[pos] = groundPatch
        return self.field.get(pos)
    
    def get(self, pos):
        if isinstance(pos, str):
            pos = self.places.get(pos)
        if pos:
            return self._getGround(pos)
        return None
    
    def makeObject(self, objtype, *args, **kwargs):
        return gameobjects.makeEntity(objtype, self.events, *args, **kwargs)
    
    def makeEntity(self, *args, **kwargs):
        return entity.Entity(self.events, *args, **kwargs)
    
    def addObj(self, pos, obj):
        obj.place(self.get(pos))
    
    def removeObj(self, pos, obj):
        self._getGround(pos).removeObj(obj)

