"""Layout calculations for the read-only Code screen."""

from __future__ import annotations

import pygame


DESIGN_SIZE = (1440, 810)


def scale_rect(rect, surface_size):
    """Scale a design-space rectangle to the current surface size."""
    design_width, design_height = DESIGN_SIZE
    width, height = surface_size
    x, y, rect_width, rect_height = rect
    return pygame.Rect(
        round(x * width / design_width),
        round(y * height / design_height),
        round(rect_width * width / design_width),
        round(rect_height * height / design_height),
    )


def screen_rects(surface_size):
    """Return the major Code screen regions in display coordinates."""
    return {
        "telemetry": scale_rect((20, 18, 1400, 78), surface_size),
        "library": scale_rect((20, 126, 248, 560), surface_size),
        "workspace": scale_rect((286, 126, 858, 560), surface_size),
        "state": scale_rect((1162, 126, 258, 560), surface_size),
        "program": scale_rect((330, 215, 790, 450), surface_size),
    }


def telemetry_rects(surface_size):
    """Return the four top telemetry cards."""
    return [
        scale_rect((20, 18, 330, 78), surface_size),
        scale_rect((370, 18, 330, 78), surface_size),
        scale_rect((720, 18, 330, 78), surface_size),
        scale_rect((1070, 18, 350, 78), surface_size),
    ]
