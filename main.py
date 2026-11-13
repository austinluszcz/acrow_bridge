
from drafter import *
from dataclasses import dataclass, field
from bakery import assert_equal
import math


@dataclass
class Part:
    name: str
    quantity: int


@dataclass
class State:
    project_name: str = ""
    crossing_type: str = ""
    bridge_length: float = 0
    width: str = "1"
    configuration: str = "DS"
    reinforced: bool = False
    parts: list = field(default_factory=list)
    calculation_ready: bool = False


CONFIGURATIONS = {
    "Single-Single (SS)": "SS",
    "Double-Single (DS)": "DS",
    "Triple-Single (TS)": "TS",
    "Quadruple-Single (QS)": "QS",
    "Double-Double (DD)": "DD",
    "Triple-Double (TD)": "TD",
    "Quadruple-Double (QD)": "QD"
}


CONFIGURATION_NAMES = {
    "SS": "Single-Single",
    "DS": "Double-Single",
    "TS": "Triple-Single",
    "QS": "Quadruple-Single",
    "DD": "Double-Double",
    "TD": "Triple-Double",
    "QD": "Quadruple-Double"
}


def calculate_bridge(length, width, configuration, reinforced):

    panels = math.ceil(length / 10)

    panel_multipliers = {
        "SS": 2, "DS": 4, "TS": 6, "QS": 8,
        "DD": 8, "TD": 12, "QD": 16
    }

    ab1 = panels * panel_multipliers[configuration]

    transoms = panels * 2
    ab2 = transoms * 2

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

    end_post_amounts = {
        "SS": 2, "DS": 4, "TS": 6, "QS": 6,
        "DD": 4, "TD": 6, "QD": 6
    }

    ab5 = end_post_amounts[configuration] if panels > 0 else 0
    ab6 = ab5

    bearing_amounts = {
        "SS": (4, 0),
        "DS": (8, 0),
        "TS": (4, 4),
        "QS": (0, 8),
        "DD": (8, 0),
        "TD": (4, 4),
        "QD": (0, 8)
    }

    ab7 = bearing_amounts[configuration][0] if panels > 0 else 0
    ab8 = bearing_amounts[configuration][1] if panels > 0 else 0

    ab9 = 4 if panels > 0 else 0

    reinforcement_multipliers = {
        "SS": 2, "DS": 2, "TS": 3, "QS": 4,
        "DD": 2, "TD": 3, "QD": 4
    }

    ab10 = 0

    if reinforced and panels > 0:
        multiplier = reinforcement_multipliers[configuration]
        ab10 = max(
            (panels - 1) * multiplier +
            (panels - 2) * multiplier, 0
        )

    ab13 = 0

    if panels > 0:

        if width == "1":
            ab13 = max((2 * panels - 3) * 2, 0)
            ab13 += 4 if panels == 1 else 8

        else:
            ab13 = max((2 * panels - 3) * 4, 0)
            ab13 += 8 if panels == 1 else 16

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
            ab51 += max(
                (panels - 2) * multiplier +
                (panels - 3) * multiplier, 0
            )

    ab52 = ab51 * 2

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

    ab54 = ab2 * 2

    transom_bolts = {
        "SS": 4, "DS": 8, "TS": 12, "QS": 16,
        "DD": 8, "TD": 12, "QD": 16
    }

    ab55 = transoms * transom_bolts[configuration]

    chord_bolts = {
        "DD": 4, "TD": 6, "QD": 8
    }

    ab57 = 0

    if configuration in chord_bolts:
        ab57 = panels * 4 * chord_bolts[configuration]

    if reinforced:
        ab57 += ab10 * 4

    ab63 = ab13 * 2

    if width == "1":
        transom_part = "AB301"
        clamp_multiplier = 12
        deck_multiplier = 3

    else:
        transom_part = "AB306"
        clamp_multiplier = 24
        deck_multiplier = 8

    ab309 = (transoms + 1) * clamp_multiplier if panels > 0 else 0

    ab310 = (panels * 2 + 1) * deck_multiplier if panels > 0 else 0

    ab311 = (
        panels * 2 + 1
        if panels > 0 and width == "2"
        else 0
    )

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


def make_parts(results):

    parts = []

    for name, quantity in results.items():

        if name != "Panels":
            parts.append(Part(name, quantity))

    return parts


def reference_content(state, about=False):

    if about:

        return Page(state, [
            Header("About This Project"),
            "This program estimates the component quantities "
            "required for an Acrow bridge.",
            "The calculator uses bridge dimensions, configuration, "
            "width, and reinforcement selections.",
            "The calculations are based on the Acrow quantity "
            "reference information used to develop this project.",
            HorizontalRule(),
            Button("Return Home", "index")
        ])

    return Page(state, [
        Header("Acrow Parts Reference"),
        "The following components are included in the calculator:",
        BulletedList([
            "AB1 - Panels",
            "AB2 - Rakers",
            "AB3 / AB4 - Bracing Frames",
            "AB5 / AB6 - End Posts",
            "AB7 / AB8 - Bearings",
            "AB9 - Baseplates",
            "AB10 - Chord Reinforcement",
            "AB13 - Swaybraces",
            "AB51 - Panel Pins",
            "AB52 - Safety Clips",
            "AB53 - Bracing Bolts",
            "AB54 - Raker Bolts",
            "AB55 - Transom Bolts",
            "AB57 - Chord Bolts",
            "AB63 - Swaybrace Bolts",
            "AB301 / AB306 - Transoms",
            "AB309 - Stringer Clamps",
            "AB310 - Deck Units",
            "AB311 - Central Deck Units",
            "AB312 - Kerb Units"
        ]),
        Button("About This Project", "about"),
        Button("Return Home", "index")
    ])



@route
def index(state: State) -> Page:

    return Page(state, [
        Header("Acrow Bridge Component Calculator"),
        "Welcome to the Acrow Bridge Component Calculator.",
        "This program estimates the quantities of components "
        "required to construct an Acrow bridge.",
        HorizontalRule(),
        Header("Start a New Project", 2),
        "Enter a project name and crossing type to begin.",
        Button("Start Project", "project_details"),
        HorizontalRule(),
        Button("Parts Reference", "parts_reference"),
        Button("About This Project", "about")
    ])



@route
def project_details(state: State) -> Page:

    return Page(state, [
        Header("Project Details"),
        "Enter the basic project information.",
        "Project name:",
        TextBox("project_name", state.project_name),
        "Crossing type:",
        TextBox("crossing_type", state.crossing_type),
        Button("Continue to Bridge Inputs", "bridge_inputs"),
        Button("Return Home", "index")
    ])



@route
def bridge_inputs(state: State) -> Page:

    return Page(state, [
        Header("Bridge Configuration"),
        "Enter the bridge specifications below.",
        "Bridge length in feet:",
        TextBox("length", "100"),
        "Bridge width:",
        SelectBox(
            "width",
            ["Single", "Double"],
            "Single"
        ),
        "Bridge configuration:",
        SelectBox(
            "configuration_label",
            [
                "Single-Single (SS)",
                "Double-Single (DS)",
                "Triple-Single (TS)",
                "Quadruple-Single (QS)",
                "Double-Double (DD)",
                "Triple-Double (TD)",
                "Quadruple-Double (QD)"
            ],
            "Double-Single (DS)"
        ),
        "Is the bridge reinforced?",
        CheckBox("reinforced", False),
        Button("Calculate Bridge", "calculate"),
        Button("Project Details", "project_details"),
        Button("Return Home", "index")
    ])



@route
def calculate(
    state: State,
    length: float,
    width: str,
    configuration_label: str,
    reinforced: bool
) -> Page:

    if length < 0:

        return Page(state, [
            Header("Invalid Bridge Length"),
            "Bridge length cannot be negative.",
            Button("Go Back", "bridge_inputs")
        ])

    if configuration_label not in CONFIGURATIONS:

        return Page(state, [
            Header("Invalid Configuration"),
            "Please select a valid bridge configuration.",
            Button("Go Back", "bridge_inputs")
        ])

    if width not in ["Single", "Double"]:

        return Page(state, [
            Header("Invalid Width"),
            "Please select Single or Double width.",
            Button("Go Back", "bridge_inputs")
        ])

    width_code = "1" if width == "Single" else "2"

    configuration = CONFIGURATIONS[configuration_label]

    results = calculate_bridge(
        length,
        width_code,
        configuration,
        reinforced
    )

    state.bridge_length = length
    state.width = width
    state.configuration = configuration
    state.reinforced = reinforced
    state.parts = make_parts(results)
    state.calculation_ready = True

    return Page(state, [
        Header("Calculation Complete"),
        "Your bridge quantities have been calculated.",
        Button("View Results", "results"),
        Button("Change Bridge Inputs", "bridge_inputs")
    ])



@route
def results(state: State) -> Page:

    if not state.calculation_ready:

        return Page(state, [
            Header("No Calculation Available"),
            "Please enter bridge information first.",
            Button("Start Calculation", "bridge_inputs")
        ])

    result_lines = []

    for part in state.parts:

        result_lines.append(
            part.name + ": " + str(part.quantity)
        )

    return Page(state, [
        Header("Bridge Calculation Results"),
        Header(state.project_name, 2),
        state.project_name +
        " requires the following parts for an Acrow bridge "
        "to cross a " + state.crossing_type + ".",
        HorizontalRule(),
        "Bridge length: " + str(state.bridge_length) + " feet",
        "Bridge width: " + state.width,
        "Configuration: " +
        CONFIGURATION_NAMES[state.configuration] +
        " (" + state.configuration + ")",
        "Reinforced: " + str(state.reinforced),
        HorizontalRule(),
        Header("Required Components", 2),
        BulletedList(result_lines),
        Button("View Parts Reference", "parts_reference"),
        Button("Calculate Another Bridge", "bridge_inputs"),
        Button("Return Home", "index")
    ])


@route
def parts_reference(state: State) -> Page:

    return reference_content(state, False)


@route
def about(state: State) -> Page:

    return reference_content(state, True)


def test_panel_calculations():

    result = calculate_bridge(100, "1", "SS", False)
    assert_equal(result["Panels"], 10)

    result = calculate_bridge(11, "1", "SS", False)
    assert_equal(result["Panels"], 2)

    result = calculate_bridge(10, "1", "SS", False)
    assert_equal(result["Panels"], 1)


def test_configurations():

    expected = {
        "SS": 20,
        "DS": 40,
        "TS": 60,
        "QS": 80,
        "DD": 80,
        "TD": 120,
        "QD": 160
    }

    for configuration in expected:

        result = calculate_bridge(
            100, "1", configuration, False
        )

        assert_equal(
            result["AB1 - Panels"],
            expected[configuration]
        )


def test_bearings():

    result = calculate_bridge(100, "1", "TS", False)

    assert_equal(result["AB7 - Bearings"], 4)
    assert_equal(result["AB8 - Bearings"], 4)

    result = calculate_bridge(100, "1", "DS", False)

    assert_equal(result["AB7 - Bearings"], 8)
    assert_equal(result["AB8 - Bearings"], 0)


def test_zero_length():

    result = calculate_bridge(0, "1", "DS", True)

    assert_equal(result["Panels"], 0)
    assert_equal(result["AB1 - Panels"], 0)
    assert_equal(result["AB5 - End Posts"], 0)
    assert_equal(result["AB7 - Bearings"], 0)
    assert_equal(result["AB10 - Chord Reinforcement"], 0)
    assert_equal(result["AB51 - Panel Pins"], 0)

test_panel_calculations()
test_configurations()
test_bearings()
test_zero_length()

start_server(State())

