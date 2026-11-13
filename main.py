
from drafter import *
from dataclasses import dataclass
from bakery import assert_equal
import math


@dataclass
class State:
    message: str = ""


def calculate_bridge(length: float, width: str,
                     configuration: str, reinforced: bool) -> dict:

    # Work out how many 10-metre panels are needed.
    panels = math.ceil(length / 10)

    panel_multipliers = {
        "SS": 2, "DS": 4, "TS": 6, "QS": 8,
        "DD": 8, "TD": 12, "QD": 16
    }

    # AB1: Panels
    ab1 = panels * panel_multipliers[configuration]

    # AB2: Rakers and transoms
    transoms = panels * 2
    ab2 = transoms * 2

    # AB3 and AB4: Bracing frames
    bracing_frames = 0

    if configuration in ["DS", "TS", "QS"]:
        bracing_frames = max((3 * panels - 1) * 2, 0)
    elif configuration in ["DD", "TD", "QD"]:
        bracing_frames = max((5 * panels - 1) * 2, 0)

    ab3 = 0
    ab4 = 0

    if configuration in ["DS", "TS", "DD", "TD"]:
        ab3 = bracing_frames
    elif configuration in ["QS", "QD"]:
        ab4 = bracing_frames

    # AB5 and AB6: End posts
    end_post_amounts = {
        "SS": 2, "DS": 4, "TS": 6, "QS": 6,
        "DD": 4, "TD": 6, "QD": 6
    }

    ab5 = end_post_amounts[configuration] if panels > 0 else 0
    ab6 = ab5

    # AB7 and AB8: Bearings
    bearing_amounts = {
        "SS": (4, 0), "DS": (8, 0), "TS": (4, 4),
        "QS": (0, 8), "DD": (8, 0), "TD": (4, 4),
        "QD": (0, 8)
    }

    ab7 = bearing_amounts[configuration][0] if panels > 0 else 0
    ab8 = bearing_amounts[configuration][1] if panels > 0 else 0

    # AB9: Baseplates
    ab9 = 4 if panels > 0 else 0

    # AB10: Chord reinforcement
    reinforcement_multipliers = {
        "SS": 2, "DS": 2, "TS": 3, "QS": 4,
        "DD": 2, "TD": 3, "QD": 4
    }

    ab10 = 0

    if reinforced:
        multiplier = reinforcement_multipliers[configuration]
        ab10 = max((panels - 1) * multiplier +
                   (panels - 2) * multiplier, 0)

    # AB13: Swaybraces (regular pattern)
    ab13 = 0

    if panels > 0:
        if width == "1":
            ab13 = max((2 * panels - 3) * 2, 0)
            ab13 += 4 if panels == 1 else 8
        else:
            ab13 = max((2 * panels - 3) * 4, 0)
            ab13 += 8 if panels == 1 else 16

    # AB51: Panel pins
    pin_multipliers = {
        "SS": 2, "DS": 4, "TS": 6, "QS": 8,
        "DD": 4, "TD": 6, "QD": 8
    }

    multiplier = pin_multipliers[configuration]
    ab51 = 0

    if panels > 0:
        if configuration in ["SS", "DS", "TS", "QS"]:
            ab51 = (panels * 2 + 2) * multiplier
        else:
            ab51 = ((panels - 1) * 4 + 6) * multiplier

        if reinforced:
            ab51 += max((panels - 2) * multiplier +
                        (panels - 3) * multiplier, 0)

    # AB52: Safety clips
    ab52 = ab51 * 2

    # AB53: Bracing bolts
    bolt_multipliers = {
        "DS": 4, "TS": 6, "QS": 8,
        "DD": 4, "TD": 6, "QD": 8
    }

    ab53 = 0

    if configuration in bolt_multipliers:
        multiplier = bolt_multipliers[configuration]

        if reinforced and configuration == "QD":
            multiplier = 6

        ab53 = bracing_frames * multiplier

    # AB54: Raker bolts
    ab54 = ab2 * 2

    # AB55: Transom bolts
    transom_bolts = {
        "SS": 4, "DS": 8, "TS": 12, "QS": 16,
        "DD": 8, "TD": 12, "QD": 16
    }

    ab55 = transoms * transom_bolts[configuration]

    # AB57: Chord bolts
    chord_bolts = {"DD": 4, "TD": 6, "QD": 8}
    ab57 = 0

    if configuration in chord_bolts:
        ab57 = panels * 4 * chord_bolts[configuration]

    if reinforced:
        ab57 += ab10 * 4

    # AB63: Swaybrace bolts
    ab63 = ab13 * 2

    # Width determines the transom and deck quantities.
    if width == "1":
        transom_part = "AB301"
        clamp_multiplier = 12
        deck_multiplier = 3
    else:
        transom_part = "AB306"
        clamp_multiplier = 24
        deck_multiplier = 8

    # Other components
    ab309 = (transoms + 1) * clamp_multiplier if panels > 0 else 0
    ab310 = (panels * 2 + 1) * deck_multiplier if panels > 0 else 0
    ab311 = panels * 2 + 1 if panels > 0 and width == "2" else 0
    ab312 = (panels * 2 + 1) * 2 if panels > 0 else 0

    return {
        "Panels": panels,
        "AB1 - Panels": ab1,
        "AB2 - Rakers": ab2,
        "AB3 - Bracing Frames": ab3,
        "AB4 - Bracing Frames": ab4,
        "AB5 - End Posts": ab5,
        "AB6 - End Posts": ab6,
        "AB7 - Bearings": ab7,
        "AB8 - Bearings": ab8,
        "AB9 - Baseplates": ab9,
        "AB10 - Chord Reinforcement": ab10,
        "AB13 - Swaybraces": ab13,
        "AB51 - Panel Pins": ab51,
        "AB52 - Safety Clips": ab52,
        "AB53 - Bracing Bolts": ab53,
        "AB54 - Raker Bolts": ab54,
        "AB55 - Transom Bolts": ab55,
        "AB57 - Chord Bolts": ab57,
        "AB63 - Swaybrace Bolts": ab63,
        transom_part + " - Transoms": transoms,
        "AB309 - Stringer Clamps": ab309,
        "AB310 - Deck Units": ab310,
        "AB311 - Central Deck Units": ab311,
        "AB312 - Kerb Units": ab312
    }


@route
def index(state: State) -> Page:
    return Page(state, [
        Header("Bridge Component Calculator"),
        "Enter the bridge details below.",
        "Bridge span in metres:",
        TextBox("length", "100"),
        "Number of lanes:",
        SelectBox("width", ["1", "2"], "1"),
        "Bridge configuration:",
        SelectBox(
            "configuration",
            ["SS", "DS", "TS", "QS", "DD", "TD", "QD"],
            "DS"
        ),
        "Is the bridge reinforced?",
        CheckBox("reinforced", False),
        Button("Calculate Bridge", "calculate")
    ])


@route
def calculate(state: State, length: float, width: str,
              configuration: str, reinforced: bool) -> Page:

    if length < 0:
        return Page(state, [
            Header("Invalid Length"),
            "Please enter a length that is zero or greater.",
            Button("Go Back", "index")
        ])

    results = calculate_bridge(
        length, width, configuration, reinforced
    )

    result_lines = []

    for part in results:
        result_lines.append(part + ": " + str(results[part]))

    return Page(state, [
        Header("Bridge Calculation Results"),
        "Bridge length: " + str(length) + " metres",
        "Width: " + ("Single" if width == "1" else "Double"),
        "Configuration: " + configuration,
        "Reinforced: " + str(reinforced),
        "Swaybrace pattern: Regular",
        HorizontalRule(),
        Header("Required Components", 2),
        BulletedList(result_lines),
        Button("Calculate Another Bridge", "index")
    ])


# TEST 1: Check panel calculations and rounding

def test_panel_calculations():
    result = calculate_bridge(100, "1", "SS", False)
    assert_equal(result["Panels"], 10)

    result = calculate_bridge(11, "1", "SS", False)
    assert_equal(result["Panels"], 2)

    result = calculate_bridge(10, "1", "SS", False)
    assert_equal(result["Panels"], 1)


# TEST 2: Check single-width and double-width bridges

def test_bridge_widths():
    single = calculate_bridge(100, "1", "SS", False)
    double = calculate_bridge(100, "2", "SS", False)

    assert_equal(single["AB301 - Transoms"], 20)
    assert_equal(double["AB306 - Transoms"], 20)

    assert_equal(single["AB310 - Deck Units"], 63)
    assert_equal(double["AB310 - Deck Units"], 168)

    assert_equal(single["AB311 - Central Deck Units"], 0)
    assert_equal(double["AB311 - Central Deck Units"], 21)


# TEST 3: Check reinforcement

def test_reinforcement():
    normal = calculate_bridge(100, "1", "DS", False)
    reinforced = calculate_bridge(100, "1", "DS", True)

    assert_equal(normal["AB10 - Chord Reinforcement"], 0)
    assert_equal(reinforced["AB10 - Chord Reinforcement"], 34)

    assert_equal(normal["AB57 - Chord Bolts"], 0)
    assert_equal(reinforced["AB57 - Chord Bolts"], 136)

    assert_equal(normal["AB51 - Panel Pins"], 48)
    assert_equal(reinforced["AB51 - Panel Pins"], 148)


# TEST 4: Check all seven configurations

def test_configurations():
    ss = calculate_bridge(100, "1", "SS", False)
    ds = calculate_bridge(100, "1", "DS", False)
    ts = calculate_bridge(100, "1", "TS", False)
    qs = calculate_bridge(100, "1", "QS", False)
    dd = calculate_bridge(100, "1", "DD", False)
    td = calculate_bridge(100, "1", "TD", False)
    qd = calculate_bridge(100, "1", "QD", False)

    assert_equal(ss["AB1 - Panels"], 20)
    assert_equal(ds["AB1 - Panels"], 40)
    assert_equal(ts["AB1 - Panels"], 60)
    assert_equal(qs["AB1 - Panels"], 80)
    assert_equal(dd["AB1 - Panels"], 80)
    assert_equal(td["AB1 - Panels"], 120)
    assert_equal(qd["AB1 - Panels"], 160)

    assert_equal(ds["AB3 - Bracing Frames"], 58)
    assert_equal(qs["AB4 - Bracing Frames"], 58)
    assert_equal(qd["AB4 - Bracing Frames"], 98)


# TEST 5: Check a short bridge

def test_short_bridge():
    result = calculate_bridge(10, "1", "TS", False)

    assert_equal(result["Panels"], 1)
    assert_equal(result["AB1 - Panels"], 6)
    assert_equal(result["AB7 - Bearings"], 4)
    assert_equal(result["AB8 - Bearings"], 4)


# TEST 6: Check zero-length bridge

def test_zero_length():
    result = calculate_bridge(0, "1", "DS", True)

    assert_equal(result["Panels"], 0)
    assert_equal(result["AB1 - Panels"], 0)
    assert_equal(result["AB3 - Bracing Frames"], 0)
    assert_equal(result["AB5 - End Posts"], 0)
    assert_equal(result["AB7 - Bearings"], 0)
    assert_equal(result["AB10 - Chord Reinforcement"], 0)
    assert_equal(result["AB51 - Panel Pins"], 0)


# Run all tests

test_panel_calculations()
test_bridge_widths()
test_reinforcement()
test_configurations()
test_short_bridge()
test_zero_length()



start_server(State())

