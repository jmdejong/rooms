
from ..datacomponents import Input, Fighter, Move, Faction, Interact, Inventory, Attackable
from ..system import system

@system([Input, Fighter, Move])
def control(obj, roomData, input, fighter, *_args):
    action = input.action
    if action:
        input.target = None
    input.action = None
    if action is not None:
        executeAction(obj, roomData, action)
    if input.target:
        fighter.target = input.target

def executeAction(obj, roomData, action):
    
    kind = action[0]
    if len(action) > 1:
        arg = action[1]
    else:
        arg = None
    try:
        handler = handlers.get(kind)
    except TypeError:
        handler = None
    if handler is None:
        print("invalid action", action)
        return
    handler(obj, roomData, arg)

def do_move(obj, roomData, direction):
    if direction not in {"north", "south", "east", "west"}:
        return
    roomData.getComponent(obj, Move).direction = direction

def do_take(obj, roomData, rank):
    inventory = roomData.getComponent(obj, Inventory)
    if inventory is None or len(inventory.items) >= inventory.capacity:
        # can't take anything if there is no inventory or if it's full
        return
    objects = obj.getNearObjects()
    if rank is not None:
        if rank not in range(len(objects)):
            return
        objects = [objects[rank]]
    for item in objects:
        if item.getComponent("item") is not None:
            inventory.add(item)
            obj.trigger("inventorychange")
            item.unPlace()
            break

def do_drop(obj, roomData, rank):
    inventory = roomData.getComponent(obj, Inventory)
    if inventory is None:
        return False
    if rank is None:
        rank = 0
    if rank not in range(len(inventory.items)):
        return False
    item = inventory.items[rank]
    inventory.items.remove(item)
    obj.trigger("inventorychange")
    #item.construct(roomData, preserve=True)
    item.place(obj.getGround())
    return True
    
def do_use(obj, roomData, rank):
    items = roomData.getComponent(obj, Inventory).items
    if rank is None:
        rank = 0
    if rank not in range(len(items)):
        return
    item = items[rank]
    item.getComponent("item").use(obj)

def do_unequip(obj, roomData, rank):
    inventory = roomData.getComponent(obj, Inventory)
    if inventory is None or len(inventory.items) >= inventory.capacity:
        # can't unequip anything if there is place in the inventory
        return
    slots = sorted(obj.getComponent("equipment").getSlots().items())
    if rank is not None:
        if rank not in range(len(slots)):
            return
        slots = [slots[rank]]
    for (slot, item) in slots:
        if item is not None:
            obj.getComponent("equipment").unEquip(slot)
            inventory.add(item)
            obj.trigger("take", item)

def do_interact(obj, roomData, directions):
    objects = _getNearbyObjects(obj, directions)
    for other in objects:
        if roomData.getComponent(other, Interact) is not None:
            for component in roomData.getComponent(other, Interact).components:
                roomData.addComponent(other, component)
            break
        if other.getComponent("interact") is not None:
            other.getComponent("interact").interact(obj)
            break

def do_attack(obj, roomData, directions):
    objects = _getNearbyObjects(obj, directions)
    if roomData.getComponent(obj, Input).target in objects:
        objects = {roomData.getComponent(obj, Input).target}
    fighter = roomData.getComponent(obj, Fighter)
    alignment = roomData.getComponent(obj, Faction) or Faction.NONE
    for other in objects:
        if fighter.inRange(obj, other) and alignment.isEnemy(roomData.getComponent(other, Faction) or Faction.NONE) and roomData.getComponent(other, Attackable):
            fighter.target = other
            roomData.getComponent(obj, Input).target = other
            break

def do_say(obj, roomData, text):
    if type(text) != str:
        return
    roomData.makeSound(obj, text)

def do_pick(obj, roomData, option):
    selected = obj.getComponent("select").getSelected()
    if selected is None:
        return
    optionmenu = selected.getComponent("options")
    if optionmenu is None:
        return
    optionmenu.choose(option, obj)

def _getNearbyObjects(obj, directions):
    nearPlaces = obj.getGround().getNeighbours()
    if not isinstance(directions, list):
        directions = [directions]
    objects = []
    for direction in directions:
        if direction is None:
            objects += obj.getNearObjects()
        elif isinstance(direction, str) and direction in nearPlaces:
            objects += nearPlaces[direction].getObjs()
    return objects
    

handlers = {
    "move": do_move,
    "take": do_take,
    "drop": do_drop,
    "use": do_use,
    "unequip": do_unequip,
    "interact": do_interact,
    "attack": do_attack,
    "say": do_say,
    "pick": do_pick
}
