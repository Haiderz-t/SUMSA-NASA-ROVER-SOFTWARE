from pathlib import Path
import xml.etree.ElementTree as ET

# ==========================================
# MAZE CONFIGURATION
# ==========================================

WORLD_SIZE = 18.0
WALL_HEIGHT = 1.5
WALL_THICKNESS = 0.3

# Each wall: (name, x, y, length, orientation)
# orientation = 0 for horizontal, 90 for vertical

walls = [
    # Outer boundaries
    ("north", 0, 9, 18, 0),
    ("south", 0, -9, 18, 0),
    ("east", 9, 0, 18, 90),
    ("west", -9, 0, 18, 90),

    # Internal maze walls
    ("wall_1", -3, -4.5, 5, 90),
    ("wall_2", -5, 2, 4, 0),
    ("wall_3", 3, 4, 6, 90),
    ("wall_4", 4.5, -3, 5, 0),
    ("wall_5", 0, 6, 4, 0),
    ("wall_6", 0, -0.5, 4, 90),
]

# Obstacles: (name, x, y, size_x, size_y, height)
boxes = [
    ("box_1", -5, 5, 1.0, 1.0, 1.0),
    ("box_2", 6, 5, 1.5, 1.5, 1.0),
    ("box_3", 0, -5, 1.0, 1.0, 1.2),
]

# Cylinders: (name, x, y, radius, height)
cylinders = [
    ("cylinder_1", 5, 0, 0.5, 1.2),
    ("cylinder_2", -6, -1, 0.4, 1.0),
]


# ==========================================
# XML HELPER FUNCTIONS
# ==========================================

def add_text(parent, tag, value):
    element = ET.SubElement(parent, tag)
    element.text = str(value)
    return element


def add_material(visual, colour):
    material = ET.SubElement(visual, "material")
    add_text(material, "ambient", colour)
    add_text(material, "diffuse", colour)


def add_box(name, x, y, sx, sy, sz, colour):
    model = ET.SubElement(world, "model", name=name)

    add_text(model, "static", "true")
    add_text(model, "pose", f"{x} {y} {sz/2} 0 0 0")

    link = ET.SubElement(model, "link", name="link")

    for element in ["collision", "visual"]:
        part = ET.SubElement(link, element, name=element)
        geometry = ET.SubElement(part, "geometry")
        box = ET.SubElement(geometry, "box")

        add_text(box, "size", f"{sx} {sy} {sz}")

        if element == "visual":
            add_material(part, colour)


def add_cylinder(name, x, y, radius, height):
    model = ET.SubElement(world, "model", name=name)

    add_text(model, "static", "true")
    add_text(model, "pose", f"{x} {y} {height/2} 0 0 0")

    link = ET.SubElement(model, "link", name="link")

    for element in ["collision", "visual"]:
        part = ET.SubElement(link, element, name=element)
        geometry = ET.SubElement(part, "geometry")
        cylinder = ET.SubElement(geometry, "cylinder")

        add_text(cylinder, "radius", radius)
        add_text(cylinder, "length", height)

        if element == "visual":
            add_material(part, "0.8 0.3 0.15 1")


# ==========================================
# CREATE SDF WORLD
# ==========================================

sdf = ET.Element("sdf", version="1.9")
world = ET.SubElement(sdf, "world", name="maze_world")

add_text(world, "gravity", "0 0 -9.81")

# Gazebo plugins
plugins = [
    ("gz-sim-physics-system",
     "gz::sim::systems::Physics"),

    ("gz-sim-user-commands-system",
     "gz::sim::systems::UserCommands"),

    ("gz-sim-scene-broadcaster-system",
     "gz::sim::systems::SceneBroadcaster"),

    ("gz-sim-sensors-system",
     "gz::sim::systems::Sensors"),

    ("gz-sim-imu-system",
     "gz::sim::systems::Imu"),
]

for filename, name in plugins:
    plugin = ET.SubElement(
        world, "plugin", filename=filename, name=name
    )

    if "Sensors" in name:
        add_text(plugin, "render_engine", "ogre2")


# Lighting
light = ET.SubElement(
    world, "light", name="sun", type="directional"
)

add_text(light, "pose", "0 0 10 0 0 0")
add_text(light, "diffuse", "0.9 0.9 0.9 1")
add_text(light, "specular", "0.2 0.2 0.2 1")
add_text(light, "direction", "-0.5 0.1 -0.9")


# Ground
add_box(
    "ground",
    0, 0,
    WORLD_SIZE, WORLD_SIZE, 0.2,
    "0.55 0.55 0.55 1"
)

# Walls
for name, x, y, length, orientation in walls:

    if orientation == 0:
        sx, sy = length, WALL_THICKNESS
    else:
        sx, sy = WALL_THICKNESS, length

    add_box(
        name, x, y,
        sx, sy, WALL_HEIGHT,
        "0.2 0.4 0.8 1"
    )

# Box obstacles
for name, x, y, sx, sy, height in boxes:
    add_box(
        name, x, y,
        sx, sy, height,
        "0.8 0.3 0.15 1"
    )

# Cylinder obstacles
for name, x, y, radius, height in cylinders:
    add_cylinder(
        name, x, y, radius, height
    )


# ==========================================
# SAVE WORLD
# ==========================================

ET.indent(sdf, space="  ")

output = Path("worlds/maze_world.sdf")
output.parent.mkdir(exist_ok=True)

ET.ElementTree(sdf).write(
    output,
    encoding="utf-8",
    xml_declaration=True
)

print(f"Created {output}")