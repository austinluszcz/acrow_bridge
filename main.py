from bakery import assert_equal
from drafter import *
from dataclasses import dataclass
import math


@dataclass
class Bridge:
    length: float
    width: str
    configuration: str
    reinforced: bool
    parts: list


@dataclass
class Part:
    name: str
    quantity: int
    unit: str
    description: str


def nominal_length(length):
    if length < 0:
        return "length does not apply"
    elif length == 0:
        return 0
    else:
        nominal = 0
        while nominal < length:
            nominal += 10
        return nominal

assert_equal(nominal_length(-1), "length does not apply")
assert_equal(nominal_length(0), 0)
assert_equal(nominal_length(4), 10)
assert_equal(nominal_length(200.1), 210)


def reinforcement(x: bool) -> str:
    if type(x) != bool:
        return "Invalid Input"
    elif x:
        return "Reinforced"
    else:
        return "Not Reinforced"


def bridge_width(width: str) -> str:
    if width == "1":
        return "Single Width"
    elif width == "2":
        return "Double Width"
    else:
        return "Invalid Width"

def bridge_configuration(config: str) -> str:
    if config == "SS":
        return "SS"
    elif config == "DS":
        return "DS"
    elif config == "TS":
        return "TS"
    elif config == "QS":
        return "QS"
    elif config == "DD":
        return "DD"
    elif config == "TD":
        return "TD"
    elif config == "QD":
        return "QD"
    else:
        return "Invalid Configuration"
    

length = float(input("How far must the bridge span? "))
width = input("How many lanes? (1 or 2): ")
config = input("Choose bridge configuration (SS, DS, TS, QS, DD, TD, QD): ")
reinforced = input("Is the bridge reinforced? (Y or N): ")

if reinforced == "Y":
    reinforced = True
elif reinforced == "N":
    reinforced = False
else:
    reinforced = "Invalid"
    
    


print(nominal_length(length))
print(bridge_width(width))
print(bridge_configuration(config))
print(reinforcement(reinforced))



def calculate_panel_count(length):
    if length <= 0:
        return 0

    return math.ceil(length/10)

    

def calculate_panel_quantity(panels, configuration):
    if configuration == "SS":
        return panels * 2
    elif configuration == "DS":
        return panels * 4
    elif configuration == "TS":
        return panels * 6
    elif configuration == "QS":
        return panels * 8
    elif configuration == "DD":
        return panels * 8
    elif configuration == "TD":
        return panels * 12
    elif configuration == "QD":
        return panels * 16
    else:
        return "Invalid Configuration"

assert_equal(calculate_panel_quantity(10, "TS"), 60)
assert_equal(calculate_panel_quantity(10, "SS"), 20)
assert_equal(calculate_panel_quantity(10, "QD"), 160)


def calculate_bridge(length, width, configuration, reinforced):
    panels = calculate_panel_count(length)
    ab1 = calculate_panel_quantity(panels, configuration)

    return ab1

assert_equal(calculate_bridge(150, "2", "TS", False), 90)



def calculate_bracing_frame(panels, configuration):
    if configuration in ["DS", "TS"]:
        return max(6 * panels - 2, 0)
    elif configuration in ["DD", "TD"]:
        return max(10 * panels - 2, 0)
    else:
        return 0


assert_equal(calculate_bracing_frame(15, "TS"), 88)
assert_equal(calculate_bracing_frame(15, "DS"), 88)
assert_equal(calculate_bracing_frame(15, "DD"), 148)
assert_equal(calculate_bracing_frame(15, "SS"), 0)



def calculate_bracing_frame_4(panels, configuration):
    if configuration == "QS":
        return max(6 * panels - 2, 0)
    elif configuration == "QD":
        return max(10 * panels - 2, 0)
    else:
        return 0
    
    
assert_equal(calculate_bracing_frame_4(15, "QS"), 88)
assert_equal(calculate_bracing_frame_4(15, "QD"), 148)
assert_equal(calculate_bracing_frame_4(15, "TS"), 0)



def calculate_raker_quantity(transoms):
    return transoms * 2

assert_equal(calculate_raker_quantity(10), 20)
assert_equal(calculate_raker_quantity(0), 0)
assert_equal(calculate_raker_quantity(25), 50)




def calculate_end_post_quantity(panels):
    if panels == 0:
        return 0
    else:
        return 6
    
assert_equal(calculate_end_post_quantity(0), 0)
assert_equal(calculate_end_post_quantity(1), 6)
assert_equal(calculate_end_post_quantity(15), 6)



def calculate_bearings(configuration, panels):
    if panels == 0:
        return {"AB7": 0, "AB8": 0}
    elif configuration == "SS":
        return {"AB7": 4, "AB8": 0}
    elif configuration == "DS":
        return {"AB7": 8, "AB8": 0}
    elif configuration == "TS":
        return {"AB7": 4, "AB8": 4}
    elif configuration == "QS":
        return {"AB7": 0, "AB8": 8}
    elif configuration == "DD":
        return {"AB7": 8, "AB8": 0}
    elif configuration == "TD":
        return {"AB7": 4, "AB8": 4}
    elif configuration == "QD":
        return {"AB7": 0, "AB8": 8}
    else:
        return "Invalid Configuration"
    
    
assert_equal(calculate_bearings("SS", 15), {"AB7": 4, "AB8": 0})
assert_equal(calculate_bearings("TS", 15), {"AB7": 4, "AB8": 4})
assert_equal(calculate_bearings("QS", 15), {"AB7": 0, "AB8": 8})
assert_equal(calculate_bearings("TD", 15), {"AB7": 4, "AB8": 4})
assert_equal(calculate_bearings("QD", 15), {"AB7": 0, "AB8": 8})
assert_equal(calculate_bearings("TS", 0), {"AB7": 0, "AB8": 0})
    
    
def calculate_baseplate_quantity(panels):
    if panels == 0:
        return 0
    else:
        return 4
    
def calculate_panel_pins(panels, configuration):
    if panels == 0:
        return 0
    elif configuration == "SS":
        return (panels * 2 + 2) * 2
    elif configuration == "DS":
        return (panels * 2 + 2) * 4
    elif configuration == "TS":
        return (panels * 2 + 2) * 6
    elif configuration == "QS":
        return (panels * 2 + 2) * 8
    elif configuration == "DD":
        return ((panels - 1) * 4 + 6) * 4
    elif configuration == "TD":
        return ((panels - 1) * 4 + 6) * 6
    elif configuration == "QD":
        return ((panels - 1) * 4 + 6) * 8
    else:
        return "Invalid Configuration"
    
    
    
def calculate_safety_clips(panel_pins):
    return panel_pins * 2



def calculate_raker_bolts(rakers):
    return rakers * 2


    
assert_equal(calculate_panel_pins(15, "SS"), 64)
assert_equal(calculate_panel_pins(15, "TS"), 192)
assert_equal(calculate_panel_pins(15, "DD"), 248)
assert_equal(calculate_panel_pins(0, "TS"), 0)

assert_equal(calculate_safety_clips(64), 128)
assert_equal(calculate_raker_bolts(20), 40)



def calculate_bracing_bolts(end_posts, configuration):
    if configuration == "SS":
        return 0
    elif configuration == "DS":
        return end_posts * 4
    elif configuration == "TS":
        return end_posts * 6
    elif configuration == "QS":
        return end_posts * 8
    elif configuration == "DD":
        return end_posts * 4
    elif configuration == "TD":
        return end_posts * 6
    elif configuration == "QD":
        return end_posts * 8
    else:
        return "Invalid Configuration"
    
    
assert_equal(calculate_bracing_bolts(4, "DS"), 16)
assert_equal(calculate_bracing_bolts(6, "TS"), 36)
assert_equal(calculate_bracing_bolts(6, "QD"), 48)
assert_equal(calculate_bracing_bolts(0, "TS"), 0)


def calculate_transom_bolts(transoms, configuration):
    if configuration == "SS":
        return transoms * 4
    elif configuration == "DS":
        return transoms * 8
    elif configuration == "TS":
        return transoms * 12
    elif configuration == "QS":
        return transoms * 16
    elif configuration == "DD":
        return transoms * 8
    elif configuration == "TD":
        return transoms * 12
    elif configuration == "QD":
        return transoms * 16
    else:
        return "Invalid Configuration"
    
    
assert_equal(calculate_transom_bolts(30, "SS"), 120)
assert_equal(calculate_transom_bolts(30, "DS"), 240)
assert_equal(calculate_transom_bolts(30, "TS"), 360)
assert_equal(calculate_transom_bolts(30, "QD"), 480)



def calculate_chord_bolts(panels, configuration):
    if configuration == "DD":
        return panels * 4 * 4
    elif configuration == "TD":
        return panels * 4 * 6
    elif configuration == "QD":
        return panels * 4 * 8
    elif configuration in ["SS", "DS", "TS", "QS"]:
        return 0
    else:
        return "Invalid Configuration"
    
    
assert_equal(calculate_chord_bolts(15, "DD"), 240)
assert_equal(calculate_chord_bolts(15, "TD"), 360)
assert_equal(calculate_chord_bolts(15, "QD"), 480)
assert_equal(calculate_chord_bolts(15, "TS"), 0)



def swaybrace_pattern(pattern):
    if pattern == "1":
        return "Regular"
    elif pattern == "2":
        return "X Pattern"
    else:
        return "Invalid Pattern"
    
    
assert_equal(swaybrace_pattern("1"), "Regular")
assert_equal(swaybrace_pattern("2"), "X Pattern")
assert_equal(swaybrace_pattern("3"), "Invalid Pattern")


pattern = input("Choose swaybrace pattern (1 = Regular, 2 = X Pattern): ")


print(swaybrace_pattern(pattern))



def calculate_swaybraces(panels, width, pattern):
    if panels == 0:
        return 0

    if width == "1":
        if pattern == "1":
            return max((2 * panels - 3) * 2, 0) + (4 if panels == 1 else 8)
        elif pattern == "2":
            return max((2 * panels - 1) * 4, 0)

    elif width == "2":
        if pattern == "1":
            return max((2 * panels - 3) * 4, 0) + (8 if panels == 1 else 16)
        elif pattern == "2":
            return max((2 * panels - 1) * 8, 0)

    return "Invalid Input"



assert_equal(calculate_swaybraces(15, "1", "1"), 62)
assert_equal(calculate_swaybraces(15, "1", "2"), 116)
assert_equal(calculate_swaybraces(15, "2", "1"), 124)
assert_equal(calculate_swaybraces(15, "2", "2"), 232)
assert_equal(calculate_swaybraces(0, "1", "1"), 0)



def calculate_swaybrace_bolts(swaybraces):
    return swaybraces * 2



assert_equal(calculate_swaybrace_bolts(62), 124)
assert_equal(calculate_swaybrace_bolts(116), 232)
assert_equal(calculate_swaybrace_bolts(0), 0)


def calculate_transoms(panels):
    return panels * 2



def calculate_stringer_clamps(transoms, width):
    if transoms == 0:
        return 0
    elif width == "1":
        return (transoms + 1) * 12
    elif width == "2":
        return (transoms + 1) * 24
    else:
        return "Invalid Width"
    
    
def calculate_deck_units(panels, width):
    if panels == 0:
        return 0
    elif width == "1":
        return ((panels * 2) + 1) * 3
    elif width == "2":
        return ((panels * 2) + 1) * 8
    else:
        return "Invalid Width"
    
    
    
def calculate_kerb_units(panels):
    if panels == 0:
        return 0
    else:
        return ((panels * 2) + 1) * 2
    
    
def calculate_central_deck_units(panels, width):
    if panels == 0 or width == "1":
        return 0
    elif width == "2":
        return (panels * 2) + 1
    else:
        return "Invalid Width"
    
    
    
assert_equal(calculate_transoms(15), 30)

assert_equal(calculate_stringer_clamps(30, "1"), 372)
assert_equal(calculate_stringer_clamps(30, "2"), 744)

assert_equal(calculate_deck_units(15, "1"), 93)
assert_equal(calculate_deck_units(15, "2"), 248)

assert_equal(calculate_kerb_units(15), 62)

assert_equal(calculate_central_deck_units(15, "1"), 0)
assert_equal(calculate_central_deck_units(15, "2"), 31)




def calculate_panel_count(length):
    if length <= 0:
        return 0
    return math.ceil(length / 10)


def calculate_panel_quantity(panels, configuration):
    multipliers = {
        "SS": 2,
        "DS": 4,
        "TS": 6,
        "QS": 8,
        "DD": 8,
        "TD": 12,
        "QD": 16
    }

    if configuration not in multipliers:
        return "Invalid Configuration"

    return panels * multipliers[configuration]


def calculate_bracing_frames(panels, configuration):
    if configuration in ["DS", "TS", "QS"]:
        return max(((panels * 2) + (panels - 1)) * 2, 0)

    elif configuration in ["DD", "TD", "QD"]:
        return max(((panels * 4) + (panels - 1)) * 2, 0)

    return 0


def calculate_end_posts(panels, configuration):
    if panels == 0:
        return 0

    quantities = {
        "SS": 2,
        "DS": 4,
        "TS": 6,
        "QS": 6,
        "DD": 4,
        "TD": 6,
        "QD": 6
    }

    return quantities[configuration]


def calculate_bearings(panels, configuration):
    if panels == 0:
        return {"AB7": 0, "AB8": 0}

    quantities = {
        "SS": (4, 0),
        "DS": (8, 0),
        "TS": (4, 4),
        "QS": (0, 8),
        "DD": (8, 0),
        "TD": (4, 4),
        "QD": (0, 8)
    }

    ab7, ab8 = quantities[configuration]

    return {"AB7": ab7, "AB8": ab8}


def calculate_chord_reinforcement(panels, configuration, reinforced):
    if not reinforced or panels == 0:
        return 0

    multipliers = {
        "SS": 2,
        "DS": 2,
        "TS": 3,
        "QS": 4,
        "DD": 2,
        "TD": 3,
        "QD": 4
    }

    multiplier = multipliers[configuration]

    return max(
        (panels - 1) * multiplier +
        (panels - 2) * multiplier,
        0
    )


def calculate_swaybraces(panels, width, pattern):
    if panels == 0:
        return 0

    if width == "1":
        if pattern == "1":
            return max((2 * panels - 3) * 2, 0) + (
                4 if panels == 1 else 8
            )
        elif pattern == "2":
            return max((2 * panels - 1) * 4, 0)

    elif width == "2":
        if pattern == "1":
            return max((2 * panels - 3) * 4, 0) + (
                8 if panels == 1 else 16
            )
        elif pattern == "2":
            return max((2 * panels - 1) * 8, 0)

    return "Invalid Input"


def calculate_panel_pins(panels, configuration, reinforced):
    if panels == 0:
        return 0

    multipliers = {
        "SS": 2,
        "DS": 4,
        "TS": 6,
        "QS": 8,
        "DD": 4,
        "TD": 6,
        "QD": 8
    }

    multiplier = multipliers[configuration]

    if not reinforced:
        if configuration in ["SS", "DS", "TS", "QS"]:
            return ((panels * 2) + 2) * multiplier
        else:
            return (((panels - 1) * 4) + 6) * multiplier

    if configuration in ["SS", "DS", "TS", "QS"]:
        return max(
            ((panels * 2) + 2) * multiplier +
            (panels - 2) * multiplier +
            (panels - 3) * multiplier,
            0
        )

    return max(
        (((panels - 1) * 4) + 6) * multiplier +
        (panels - 2) * multiplier +
        (panels - 3) * multiplier,
        0
    )


def calculate_chord_bolts(panels, configuration,
                          chord_reinforcement, reinforced):
    multipliers = {
        "DD": 4,
        "TD": 6,
        "QD": 8
    }

    quantity = 0

    if configuration in multipliers:
        quantity = panels * 4 * multipliers[configuration]

    if reinforced:
        quantity += chord_reinforcement * 4

    return quantity


def calculate_bridge(length, width, configuration,
                     reinforced, pattern):

    valid_configurations = ["SS", "DS", "TS", "QS",
                            "DD", "TD", "QD"]

    if length < 0:
        return "Invalid Length"

    if width not in ["1", "2"]:
        return "Invalid Width"

    if configuration not in valid_configurations:
        return "Invalid Configuration"

    if type(reinforced) != bool:
        return "Invalid Reinforcement Input"

    if pattern not in ["1", "2"]:
        return "Invalid Swaybrace Pattern"

    panels = calculate_panel_count(length)

    # AB1 - Panels
    ab1 = calculate_panel_quantity(panels, configuration)

    # AB2 - Rakers
    transoms = panels * 2
    rakers = transoms * 2

    # AB3 / AB4 - Bracing Frames
    bracing_frames = calculate_bracing_frames(
        panels, configuration
    )

    ab3 = 0
    ab4 = 0

    if configuration in ["DS", "TS", "DD", "TD"]:
        ab3 = bracing_frames
    elif configuration in ["QS", "QD"]:
        ab4 = bracing_frames

    # AB5 / AB6 - End Posts
    end_posts = calculate_end_posts(panels, configuration)

    # AB7 / AB8 - Bearings
    bearings = calculate_bearings(panels, configuration)

    # AB9 - Baseplates
    ab9 = 4 if panels > 0 else 0

    # AB10 - Chord Reinforcement
    ab10 = calculate_chord_reinforcement(
        panels, configuration, reinforced
    )

    # AB13 - Swaybraces
    ab13 = calculate_swaybraces(panels, width, pattern)

    # AB51 / AB52 - Panel Pins and Safety Clips
    ab51 = calculate_panel_pins(
        panels, configuration, reinforced
    )
    ab52 = ab51 * 2

    # AB53 - Bracing Bolts
    bracing_bolt_multipliers = {
        "DS": 4,
        "TS": 6,
        "QS": 8,
        "DD": 4,
        "TD": 6,
        "QD": 8
    }

    ab53 = 0

    if configuration in bracing_bolt_multipliers:
        multiplier = bracing_bolt_multipliers[configuration]

        # The QDR workbook currently specifies 6.
        if reinforced and configuration == "QD":
            multiplier = 6

        ab53 = bracing_frames * multiplier

    # AB54 - Raker Bolts
    ab54 = rakers * 2

    # AB55 - Transom Set Bolts
    transom_bolt_multipliers = {
        "SS": 4,
        "DS": 8,
        "TS": 12,
        "QS": 16,
        "DD": 8,
        "TD": 12,
        "QD": 16
    }

    ab55 = transoms * transom_bolt_multipliers[configuration]

    # AB57 - Chord Bolts
    ab57 = calculate_chord_bolts(
        panels, configuration, ab10, reinforced
    )

    # AB63 - Swaybrace Bolts
    ab63 = ab13 * 2

    # Transom part number depends on width
    if width == "1":
        transom_part = "AB301"
        clamp_multiplier = 12
        deck_multiplier = 3
    else:
        transom_part = "AB306"
        clamp_multiplier = 24
        deck_multiplier = 8

    # AB309 - Stringer Clamp Assembly
    ab309 = (transoms + 1) * clamp_multiplier if panels > 0 else 0

    # AB310 - Deck Units
    ab310 = ((panels * 2) + 1) * deck_multiplier if panels > 0 else 0

    # AB311 - Central Deck Units
    ab311 = ((panels * 2) + 1) if panels > 0 and width == "2" else 0

    # AB312 - Kerb Units
    ab312 = ((panels * 2) + 1) * 2 if panels > 0 else 0

    return {
        "Panels": panels,
        "AB1": ab1,
        "AB2": rakers,
        "AB3": ab3,
        "AB4": ab4,
        "AB5": end_posts,
        "AB6": end_posts,
        "AB7": bearings["AB7"],
        "AB8": bearings["AB8"],
        "AB9": ab9,
        "AB10": ab10,
        "AB13": ab13,
        "AB51": ab51,
        "AB52": ab52,
        "AB53": ab53,
        "AB54": ab54,
        "AB55": ab55,
        "AB57": ab57,
        "AB63": ab63,
        transom_part: transoms,
        "AB309": ab309,
        "AB310": ab310,
        "AB311": ab311,
        "AB312": ab312
    }




result = calculate_bridge(100, "2", "DS", True, "1")

assert_equal(result["Panels"], 10)
assert_equal(result["AB1"], 40)
assert_equal(result["AB3"], 58)
assert_equal(result["AB10"], 34)
assert_equal(result["AB13"], 84)
assert_equal(result["AB51"], 148)
assert_equal(result["AB57"], 136)
assert_equal(result["AB306"], 20)



print(result)


assert_equal(
    calculate_bridge(150, "2", "TS", False, "1")["AB1"],
    90
)


start_server(State())
