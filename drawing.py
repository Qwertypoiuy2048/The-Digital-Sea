"""Reusable Pygame drawing helpers shared by game screens."""

from __future__ import annotations

import math

import pygame

import constants


def draw_transparent_line(surface, color, start, end, width=2):
    """Draw an RGBA line by compositing it onto the destination surface."""
    layer = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    pygame.draw.line(layer, color, start, end, width)
    surface.blit(layer, (0, 0))


def draw_dashed_line(surface, color, start, end, width=2, dash_length=10):
    """Draw a transparent dashed line between two points."""
    start = pygame.Vector2(start)
    end = pygame.Vector2(end)
    direction = end - start
    length = direction.length()
    if length == 0:
        return
    direction.normalize_ip()
    distance = 0
    layer = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    while distance < length:
        segment_end = min(distance + dash_length, length)
        pygame.draw.line(layer, color, start + direction * distance,
                         start + direction * segment_end, width)
        distance += dash_length * 2
    surface.blit(layer, (0, 0))


def draw_transparent_circle(surface, color, center, radius, width=0):
    """Draw an RGBA circle by compositing it onto the destination surface."""
    radius = max(1, round(radius))
    layer = pygame.Surface((radius * 2 + 2, radius * 2 + 2), pygame.SRCALPHA)
    pygame.draw.circle(layer, color, (radius + 1, radius + 1), radius, width)
    surface.blit(layer, (center[0] - radius - 1, center[1] - radius - 1))


def draw_fuzzy_glow(surface, color, center, radius, steps):
    """Draw a subtle radial glow with a soft, non-circular edge."""
    red, green, blue, alpha = color
    for step in range(steps, 0, -1):
        amount = step / steps
        current_radius = max(1, round(radius * amount))
        current_alpha = max(1, round(alpha * (1 - amount) ** 2))
        draw_transparent_circle(
            surface,
            (red, green, blue, current_alpha),
            center,
            current_radius,
        )


def draw_cubic_curve(surface, color, points, width=1, steps=36):
    """Draw a smooth cubic curve from four control points."""
    curve_points = []
    for index in range(steps + 1):
        t = index / steps
        inverse = 1 - t
        point = (
            inverse**3 * pygame.Vector2(points[0])
            + 3 * inverse**2 * t * pygame.Vector2(points[1])
            + 3 * inverse * t**2 * pygame.Vector2(points[2])
            + t**3 * pygame.Vector2(points[3])
        )
        curve_points.append(point)
    layer = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    pygame.draw.lines(layer, color, False, curve_points, width)
    surface.blit(layer, (0, 0))


def draw_lock(surface, center, scale=1.0):
    """Draw a small red lock marker for an encrypted connection."""
    size = max(5, round(constants.LOCK_MARKER_SIZE * scale))
    layer = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    body = pygame.Rect(round(center[0] - size), round(center[1] - size * 0.05),
                       size * 2, round(size * 1.45))
    pygame.draw.rect(layer, constants.LOCK_COLOR, body,
                     border_radius=max(2, size // 3))
    shackle = pygame.Rect(round(center[0] - size * 0.65),
                          round(center[1] - size * 0.85),
                          round(size * 1.3), round(size * 1.25))
    pygame.draw.arc(layer, constants.LOCK_COLOR, shackle, math.pi,
                    2 * math.pi, max(2, round(size * 0.25)))
    pygame.draw.circle(
        layer,
        constants.BACKGROUND_COLOR,
        (round(center[0]), round(center[1] + size * 0.55)),
        max(1, round(size * 0.16)),
    )
    surface.blit(layer, (0, 0))


def draw_background(surface):
    """Draw the shared Digital Sea gradient, glow, and current field."""
    width, height = surface.get_size()
    gradient = pygame.Surface((width, height))
    for y in range(height):
        amount = y / max(1, height - 1)
        color = tuple(round(
            constants.BACKGROUND_TOP_COLOR[channel] * (1 - amount)
            + constants.BACKGROUND_BOTTOM_COLOR[channel] * amount
        ) for channel in range(3))
        pygame.draw.line(gradient, color, (0, y), (width, y))
    surface.blit(gradient, (0, 0))

    atmosphere = pygame.Surface((width, height), pygame.SRCALPHA)
    for center, radius in [
        ((width * 0.25, height * 0.35), 250),
        ((width * 0.75, height * 0.7), 290),
    ]:
        draw_fuzzy_glow(
            atmosphere,
            constants.CURRENT_GLOW_COLOR,
            center,
            radius,
            constants.CURRENT_GLOW_STEPS,
        )
    for y in range(-height, height * 2, 120):
        draw_cubic_curve(
            atmosphere,
            constants.CURRENT_LINE_COLOR,
            [
                (-80, y),
                (width * 0.25, y - 80),
                (width * 0.7, y + 90),
                (width + 80, y - 10),
            ],
            1,
        )
    surface.blit(atmosphere, (0, 0))


def draw_help(surface, font):
    """Draw the shared interaction hint used by map-like screens."""
    text = "LEFT: inspect   WHEEL: zoom   MIDDLE/RIGHT DRAG: pan"
    label = font.render(text, True, constants.MUTED_TEXT_COLOR)
    surface.blit(label, (18, surface.get_height() - label.get_height() - 18))
