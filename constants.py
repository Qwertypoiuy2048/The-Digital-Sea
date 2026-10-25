"""Easy-to-edit visual and prototype settings for The Digital Sea."""

# Window settings
WINDOW_SIZE = (1000, 800)
WINDOW_TITLE = "The Digital Sea - Network Screen"
FRAME_RATE = 60

# Camera settings
STARTING_CAMERA = (250, 0)
STARTING_ZOOM = 0.62
MIN_ZOOM = 0.35
MAX_ZOOM = 1.8
ZOOM_STEP = 1.12
NETWORK_CENTER = (360, 640)
NETWORK_LAYER_SPACING = 190

# Main colors. Alpha values are used when drawing onto transparent surfaces.
BACKGROUND_COLOR = (7, 20, 33)  # SVG background-gradient's darkest blue
GRID_COLOR = BACKGROUND_COLOR
BACKGROUND_TOP_COLOR = (7, 20, 33)  # #071421
BACKGROUND_BOTTOM_COLOR = (17, 24, 42)  # #11182a
CURRENT_LINE_COLOR = (111, 200, 207, 14)  # #6fc8cf at low opacity
CURRENT_GLOW_COLOR = (61, 217, 208, 16)  # #3dd9d0, intentionally subtle
CURRENT_GLOW_STEPS = 20

# Network connections, based on the SVG mockup.
CURRENT_COLOR = (78, 200, 210)
CONNECTION_COLOR = (120, 146, 183, 166)  # #7892b7 at 65% opacity
PLAYER_CONNECTION_COLOR = (67, 228, 214, 242)  # #43e4d6 at 95% opacity
PLAYER_CONNECTION_CORE_COLOR = (178, 255, 247, 204)  # #b2fff7 at 80% opacity
UNSTABLE_CONNECTION_COLOR = (212, 168, 90, 230)  # #d4a85a at 90% opacity
MONITORED_CONNECTION_COLOR = (168, 94, 224, 235)
MONITORED_NODE_STROKE = (191, 110, 241, 240)
MONITORED_NODE_FILL = (93, 46, 125, 155)
MONITOR_MARKER_COLOR = (214, 130, 255, 255)
LOCK_COLOR = (240, 92, 108, 240)

# Node colors, based on the SVG active/cached device layers.
CACHED_NODE_FILL = (135, 146, 163, 107)  # #8792a3 at 42% opacity
CACHED_NODE_STROKE = (167, 176, 189, 107)  # #a7b0bd at 42% opacity
CACHED_NODE_MARKER = (196, 204, 214, 180)  # #c4ccd6
ACTIVE_NODE_GLOW = (43, 217, 207, 41)  # #2bd9cf at 16% opacity
ACTIVE_NODE_STROKE = (77, 246, 231, 255)  # #4df6e7
ACTIVE_NODE_CORE = (18, 59, 73, 255)  # #123b49
ACTIVE_NODE_INNER = (40, 188, 183, 204)  # #28bcb7 at 80% opacity
ACTIVE_NODE_CENTER = (201, 255, 251, 255)  # #c9fffb
PRIMARY_NODE_RING = (131, 255, 242, 220)  # Extra primary-device circle
SECONDARY_NODE_GLOW = (50, 122, 131, 51)  # #327a83 at 20% opacity
SECONDARY_NODE_STROKE = (104, 182, 189, 184)  # #68b6bd at 72% opacity
SECONDARY_NODE_CORE = (27, 59, 74, 184)  # #1b3b4a at 72% opacity
SECONDARY_NODE_INNER = (76, 142, 152, 184)  # #4c8e98 at 72% opacity
SECONDARY_NODE_CENTER = (192, 231, 229, 184)  # #c0e7e5 at 72% opacity
SELECTED_NODE_COLOR = (245, 249, 255, 255)

TEXT_COLOR = (184, 217, 216)  # #b8d9d8
MUTED_TEXT_COLOR = (133, 158, 169)
PANEL_COLOR = (8, 29, 43, 235)

# Node sizes in world-space pixels.
NODE_RADII = {
    "small": 25,
    "medium": 36,
    "large": 48,
}

# Connection widths in world-space pixels.
STRONG_CONNECTION_WIDTH = 7
WEAK_CONNECTION_WIDTH = 3

# Input settings
CONNECTION_SELECTION_DISTANCE = 12
LOCK_MARKER_SIZE = 9


def node_radius(size: str) -> float:
    """Return the world-space radius for a node size label."""
    return NODE_RADII.get(size, 30)
