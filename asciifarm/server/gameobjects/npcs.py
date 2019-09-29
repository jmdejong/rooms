

from ..entity import Entity

from ..components import StaticSerializer as Static
from ..components import Loot, Trap
from ..datacomponents import Fighter, Move, Attackable, AI

from .. import faction

entities = {}


entities["rabbit"] = lambda: Entity(
    sprite="rabbit", name="bunny", height=1, components={"serialize": Static("rabbit")}, dataComponents={"ai": AI(moveChance=0.05), "move": Move(slowness=4)})


entities["goblin"] = lambda home=None: Entity(sprite="goblin", height=1.2, components={
        "loot": Loot([("sword", .05), ("club", .1), ("radishes", .25)])
    }, dataComponents={
        "faction": faction.EVIL,
        "ai": AI(viewDist=8, moveChance=0.02, home=home),
        "move": Move(slowness=3),
        "attackable": Attackable(maxHealth=15),
        "fighter": Fighter(strength=5, slowness=8)
    }
)

entities["troll"] = lambda home=None: Entity(sprite="troll", height=1.8, components={
        "loot": Loot([("stone", 1), ("stone", .3), ("pebble", .5), ("pebble", .5), ("pebble", .5)])
    }, dataComponents={
        "faction": faction.EVIL,
        "ai": AI(viewDist=8, moveChance=0.01, home=home),
        "move": Move(slowness=4),
        "attackable": Attackable(maxHealth=75),
        "fighter": Fighter(strength=15, slowness=10)
    }
)

entities["rat"] = lambda home=None: Entity(sprite="rat", height=1, components={
        "loot": Loot([("radishseed", 0.9), ("radishseed", 0.3)])
    }, dataComponents={
        "faction": faction.EVIL,
        "ai": AI(viewDist=3, moveChance=0.08, home=home, homesickness=0.1),
        "move": Move(slowness=3),
        "attackable": Attackable(maxHealth=8),
        "fighter": Fighter(strength=2, slowness=6)
    }
)




entities["dummy"] = lambda: Entity(
    sprite="dummy", height=1, flags={"occupied"}, dataComponents={
        "attackable": Attackable(maxHealth=20),
        "faction": faction.NONE
    })

entities["spiketrap"] = lambda damage=15: Entity(sprite="spikes", height=1, flags={"occupied"}, components={
        "collision": Trap(),
        "serialize": Static("spiketrap")
    }, dataComponents={
        "fighter": Fighter(strength=damage, slowness=20)
    }
)
