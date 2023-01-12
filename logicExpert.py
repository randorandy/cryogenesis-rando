from typing import ClassVar

from connection_data import area_doors_unpackable
from door_logic import canOpen
from item_data import items_unpackable
from loadout import Loadout
from logicInterface import AreaLogicType, LocationLogicType, LogicInterface
from logic_shortcut import LogicShortcut

# TODO: There are a bunch of places where where Expert logic needed energy tanks even if they had Varia suit.
# Need to make sure everything is right in those places.
# (They will probably work right when they're combined like this,
#  but they wouldn't have worked right when casual was separated from expert.)

# TODO: There are also a bunch of places where casual used icePod, where expert only used Ice. Is that right?

(
    CraterR, SunkenNestL, RuinedConcourseBL, RuinedConcourseTR, CausewayR,
    SporeFieldTR, SporeFieldBR, OceanShoreR, EleToTurbidPassageR, PileAnchorL,
    ExcavationSiteL, WestCorridorR, FoyerR, ConstructionSiteL, AlluringCenoteR,
    FieldAccessL, TransferStationR, CellarR, SubbasementFissureL,
    WestTerminalAccessL, MezzanineConcourseL, VulnarCanyonL, CanyonPassageR,
    ElevatorToCondenserL, LoadingDockSecurityAreaL, ElevatorToWellspringL,
    NorakBrookL, NorakPerimeterTR, NorakPerimeterBL, VulnarDepthsElevatorEL,
    VulnarDepthsElevatorER, HiveBurrowL, SequesteredInfernoL,
    CollapsedPassageR, MagmaPumpL, ReservoirMaintenanceTunnelR, IntakePumpR,
    ThermalReservoir1R, GeneratorAccessTunnelL, ElevatorToMagmaLakeR,
    MagmaPumpAccessR, FieryGalleryL, RagingPitL, HollowChamberR, PlacidPoolR,
    SporousNookL, RockyRidgeTrailL, TramToSuziIslandR
) = area_doors_unpackable

(
    Missile, Super, PowerBomb, Morph, Springball, Bombs, HiJump,
    DeepSuit, Wave, SpeedBooster, Spazer, Ice, Grapple,
    Plasma, Screw, Chrage, SpaceJump, Energy, Meteorite
) = items_unpackable


exitSpacePort = LogicShortcut(lambda loadout: (
    True
    # TODO: Why did one definition have somethings different?
    # (Morph in loadout) or (Missile in loadout) or (Super in loadout) or (Wave in loadout)
))
canBomb = LogicShortcut(lambda loadout: (
    (Morph in loadout) and loadout.has_any(Bombs, PowerBomb)
))
# TODO: I think there may be places where canBomb is used for bomb jumping
# even though it might only have PBs

canFly = LogicShortcut(lambda loadout: (
    (SpaceJump in loadout) or loadout.has_all(Morph, Bombs)
))
missileDamage = LogicShortcut(lambda loadout: (
    loadout.has_any(Missile, Super)
))
pinkDoor = LogicShortcut(lambda loadout: (
    missileDamage in loadout
))
pastShip = LogicShortcut(lambda loadout: (
    (Morph in loadout) and (pinkDoor in loadout)
))
pastShipBombable = LogicShortcut(lambda loadout: (
    (pastShip in loadout) and (canBomb in loadout)
))
iceBath = LogicShortcut(lambda loadout: (
    (DeepSuit in loadout) or
    (Grapple in loadout) or
    (HiJump in loadout) or
    (Ice in loadout)
))
topPirates = LogicShortcut(lambda loadout: (
    (canFly in loadout) and
    (pinkDoor in loadout) and
    (
        (Spazer in loadout) or
        (Plasma in loadout) or
        (Ice in loadout) or
        (Wave in loadout) or
        (Screw in loadout)
        )
))
voidEngine = LogicShortcut(lambda loadout: (
    (pastShip in loadout) and
    (canBomb in loadout) and
    (
        (iceBath in loadout) or
        (topPirates in loadout)
        )
))
superRoute = LogicShortcut(lambda loadout: (
    (
        (Morph in loadout) and
        (Super in loadout) and
        (
            (HiJump in loadout) or
            (DeepSuit in loadout) or
            (Springball in loadout)
            )
        ) or
    (voidEngine in loadout)
))
meteorHouse = LogicShortcut(lambda loadout: (
    (voidEngine in loadout) and (Meteorite in loadout)
))
kraidShip = LogicShortcut(lambda loadout: (
    (pastShipBombable in loadout) and
    (
        (Springball in loadout) or
        (SpeedBooster in loadout) or
        (DeepSuit in loadout)
        )
))
kraid = LogicShortcut(lambda loadout: (
    (voidEngine in loadout) and
    (
        (DeepSuit in loadout) or
        (Ice in loadout)
        )
))

area_logic: AreaLogicType = {
    "Early": {
        # using SunkenNestL as the hub for this area, so we don't need a path from every door to every other door
        # just need at least a path with sunken nest to and from every other door in the area
        ("CraterR", "SunkenNestL"): lambda loadout: (
            True
        ),
        ("SunkenNestL", "CraterR"): lambda loadout: (
            True
        ),
        ("SunkenNestL", "RuinedConcourseBL"): lambda loadout: (
            True
        ),
        ("SunkenNestL", "RuinedConcourseTR"): lambda loadout: (
            True
            # TODO: Expert needs energy and casual doesn't? And Casual can do it with supers, but expert can't?
        ),   
    },
}

location_logic: LocationLogicType = {
    "Power Bomb": lambda loadout: (
        (voidEngine in loadout) and
        (
            (
                (Meteorite in loadout) and
                (SpeedBooster in loadout) and
                (DeepSuit in loadout)
                ) or
            (PowerBomb in loadout)
            )
    ),
    "Left of Ship Missile": lambda loadout: (
        (canBomb in loadout) or
        (
            (Morph in loadout) and
            (pinkDoor in loadout)
            )
    ),
    "Screw Missile": lambda loadout: (
        (voidEngine in loadout) and
        (
            (PowerBomb in loadout) or
            (Meteorite in loadout)
            )
    ),
    "Meteorite Drop Top Missile": lambda loadout: (
        (voidEngine in loadout) and
        (
            (PowerBomb in loadout) or
            (Meteorite in loadout)
            )
    ),
    "Kraid Missile Right of Save": lambda loadout: (
        kraidShip in loadout
    ),
    "Gaflun Jungle Left Missile": lambda loadout: (
        superRoute in loadout
    ),
    "Void Engine Ascent Missile": lambda loadout: (
        voidEngine in loadout
    ),
    "Morph Missile": lambda loadout: (
        canBomb in loadout
    ), 
    "Below Ship Missile": lambda loadout: (
        (pastShip in loadout) and
        (Meteorite in loadout)
    ),
    "Wave Missile": lambda loadout: (
        (voidEngine in loadout) and
        (
            (DeepSuit in loadout) or
            (Ice in loadout) or
            (HiJump in loadout) or
            (Bombs in loadout)
            )
    ),
    "Underwater Missile Above Kraid Ship": lambda loadout: (
        pastShipBombable in loadout
    ),
    "Spazer Missile": lambda loadout: (
        (voidEngine in loadout) and
        (
            (canFly in loadout) or
            (HiJump in loadout)
            )
    ),
    "Missile Below Meteorite Warehouse": lambda loadout: (
        meteorHouse in loadout
    ),
    "Top Red Tower Missile": lambda loadout: (
        pastShipBombable in loadout
    ),
    "Right of Ship Tube Missile": lambda loadout: (
        (Morph in loadout) and
        (Meteorite in loadout)
    ),
    "Ice Bridge Missile": lambda loadout: (
        (pastShip in loadout) and
        (
            (Screw in loadout) or
            (canBomb in loadout)
            )
    ),
    "Draygon Missile": lambda loadout: (
        (voidEngine in loadout) and
        (
            (SpeedBooster in loadout) or
            (Meteorite in loadout)
            )
    ),
    "Right of Ship Glacier Missile": lambda loadout: (
        (canBomb in loadout) or
        (
            (Morph in loadout) and
            (Screw in loadout)
            )
    ),
    "Void Engine Entry Bottom Missile": lambda loadout: (  # front
        voidEngine in loadout
    ), 
    "Plunge Right Missile": lambda loadout: (
        voidEngine in loadout
    ),
    "Grapple Tutorial Top Missile": lambda loadout: (
        pastShipBombable in loadout
    ),
    "Bomb Torizo": lambda loadout: (
        True
    ),
    "Meteorite Warehouse Missile": lambda loadout: (
        meteorHouse in loadout
    ),
    "Chrage Hidden Missile": lambda loadout: (
        (pastShipBombable in loadout) and
        (Super in loadout)
    ),
    "Plunge Left Missile": lambda loadout: (
        pastShipBombable in loadout
    ),
    "Meteorite Missile": lambda loadout: (
        meteorHouse in loadout
    ),
    "Teranul Map Missile": lambda loadout: (
        pastShipBombable in loadout
    ),
    "HiJump Missile": lambda loadout: (
        (voidEngine in loadout) and
        (
            (DeepSuit in loadout) or
            (Grapple in loadout)
            )
    ),
    "Outside Springball Missile": lambda loadout: (
        (pastShipBombable in loadout)
    ),
    "Left of Meteorite Drop Missile": lambda loadout: (
        (voidEngine in loadout)
    ),
    "Void Engine Entry Hidden Missile": lambda loadout: (
        voidEngine in loadout
    ),
    "Springball Missile": lambda loadout: (
        (pastShipBombable in loadout) and
        (Super in loadout)
    ),
    "Gaflun Jungle Hidden Missile": lambda loadout: (
        (superRoute in loadout)
    ),
    "Grapple Tutorial Bottom Missile": lambda loadout: (
        pastShip in loadout
    ),
    "Turbine Missile": lambda loadout: (
        (meteorHouse in loadout)
    ),
    "Kraid Warehouse Missile": lambda loadout: (
        (pastShip in loadout) and
        (
            (canBomb in loadout) or
            (Screw in loadout)
            )
    ),
    "Morph Ball": lambda loadout: (
        (Morph in loadout)
    ),
    "Meteorite Drop Super": lambda loadout: (
        (meteorHouse in loadout) or
        (
            (voidEngine in loadout) and
            (PowerBomb in loadout) and
            (Screw in loadout)
            )
    ),
    "Super Above Kraid Ship": lambda loadout: (
        (pastShipBombable in loadout) and
        (
            (Bombs in loadout) or
            ((Springball in loadout) and (Screw in loadout))
            )
    ),
    "Outside Springball Supers": lambda loadout: (
        (pastShipBombable in loadout) and
        (
            (Meteorite in loadout) or
            (SpeedBooster in loadout)
            )
    ),
    "Void Engine Ascent Super": lambda loadout: (
        (voidEngine in loadout) and
        (Screw in loadout)
    ),
    "Botwoon Supers": lambda loadout: (
        (superRoute in loadout)
    ),
    "Kraid Elevator Supers": lambda loadout: (
        (kraid in loadout) or
        (
            (pastShipBombable in loadout) and
            (
                (canFly in loadout) or
                (Grapple in loadout) or
                (Super in loadout)
                )
            )
    ),
    "Grapple Tutorial Supers": lambda loadout: (
        (pastShip in loadout) and
        (PowerBomb in loadout)
    ),
    "Springball Super": lambda loadout: (
        (pastShipBombable in loadout) and
        (Super in loadout)
    ),
    "Crater Supers": lambda loadout: (
        (Morph in loadout) and
        (Super in loadout)
    ),
    "Kraid Crate Supers": lambda loadout: (
        (kraidShip in loadout) 
    ),
    "Kraid Cargo Maze": lambda loadout: (
        (kraid in loadout) or
        (
            (pastShipBombable in loadout) and
            (
                (canFly in loadout) or
                (Grapple in loadout) or
                (Super in loadout)
                )
            )
    ),
        
    "Screw Supers Above Kraid": lambda loadout: (
        (pastShip in loadout) and
        (Screw in loadout)
    ),
    "Sand Supers": lambda loadout: (
        (voidEngine in loadout)  
    ),
    "Top Red Tower Super": lambda loadout: (  # TODO: check an area door, don't assume we start in this area
        (pastShip in loadout) and
        (PowerBomb in loadout)
    ),
    "Grapple": lambda loadout: (
        (pastShip in loadout) and
        (Grapple in loadout)
    ),
    "Bombs": lambda loadout: (
        (pastShip in loadout) and
        (
            (Grapple in loadout) or
            (HiJump in loadout) or
            (canFly in loadout)
            )
    ),
    "Dead Guy E-Tank": lambda loadout: (  # (4 = letter Omega)
        pastShip in loadout
    ),
    "Plunge E-Tank": lambda loadout: (
        pastShipBombable in loadout
    ),
    "Botwoon E-Tank": lambda loadout: (
        (pastShipBombable in loadout) and
        (Chrage in loadout)
    ),
    "Turbine E-Tank": lambda loadout: (
        meteorHouse in loadout
    ),
    "Void Engine Entry E-Tank": lambda loadout: (  
        voidEngine in loadout
    ),
    "Wave E-Tank": lambda loadout: (
        voidEngine in loadout
    ),
    "Crater E-Tank": lambda loadout: (
        (canBomb in loadout) or
        (Screw in loadout)
    ),
    "Springball E-Tank": lambda loadout: (
        (pastShipBombable in loadout) and
        (Super in loadout)
    ),
    "Kraid E-Tank Right of Save": lambda loadout: (
        (kraidShip in loadout) and
        (Super in loadout)
    ), 
    "HiJump Boots": lambda loadout: (
        (voidEngine in loadout) and
        (
            (DeepSuit in loadout) or
            (Grapple in loadout)
            )
    ),
    "Space Jump": lambda loadout: (
        (pastShip in loadout) and
        (PowerBomb in loadout) and
        (Chrage in loadout) and
        (Super in loadout) and
        (Energy in loadout) and
        (DeepSuit in loadout)
    ),
    "Springball": lambda loadout: (
        (pastShipBombable in loadout) and
        (Super in loadout)
    ),
    "Screw Attack": lambda loadout: (
        (
            (meteorHouse in loadout) and
            (Screw in loadout)
            ) or
        (
            (voidEngine in loadout) and
            (PowerBomb in loadout)
            )
    ),
    "Wave Beam": lambda loadout: (
        (voidEngine in loadout) and
        (
            (canFly in loadout) or
            (HiJump in loadout)
            )
    ),
    "Spazer": lambda loadout: (
        (voidEngine in loadout) and
        (
            (canFly in loadout) or
            (HiJump in loadout)
            )
    ),
    "Deep Suit": lambda loadout: (
        (voidEngine in loadout)
    ),
    "Ice Beam": lambda loadout: (  # TODO: check an area door, don't assume that we start by vulnar
        (pastShipBombable in loadout)
    ),
    "Chrage Beam": lambda loadout: (  # back
        (pastShipBombable in loadout) and
        (Super in loadout)
    ),
    "Meteorite": lambda loadout: (
        meteorHouse in loadout
    ),
}


class Expert(LogicInterface):
    area_logic: ClassVar[AreaLogicType] = area_logic
    location_logic: ClassVar[LocationLogicType] = location_logic

    @staticmethod
    def can_fall_from_spaceport(loadout: Loadout) -> bool:
        return True
