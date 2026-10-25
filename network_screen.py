"""Interactive network-map screen."""

from __future__ import annotations

import pygame

import constants
from drawing import (
    draw_dashed_line,
    draw_background,
    draw_help,
    draw_lock,
    draw_transparent_circle,
    draw_transparent_line,
)
from network_layout import compute_node_positions
from screen import Screen


def distance_to_segment(point, start, end) -> float:
    """Return the shortest distance from a point to a line segment."""
    point = pygame.Vector2(point)
    start = pygame.Vector2(start)
    segment = pygame.Vector2(end) - start
    if segment.length_squared() == 0:
        return point.distance_to(start)
    projection = max(0, min(1, (point - start).dot(segment) / segment.length_squared()))
    return point.distance_to(start + segment * projection)


class NetworkScreen(Screen):
    def __init__(self, state: dict):
        self.state = state
        self.player = state["player"]
        cache = state["network_cache"]
        self.nodes = {node["id"]: node for node in cache["nodes"]}
        self.connections = cache["connections"]
        active_nodes = self.player.get("activeNodes", {})
        self.primary_node = active_nodes.get("primary")
        self.secondary_nodes = set(active_nodes.get("secondary", []))
        # Temporary compatibility with the earlier player-file key.
        if not self.primary_node and self.player.get("activeDevices"):
            self.primary_node = self.player["activeDevices"][0]
            self.secondary_nodes = set(self.player["activeDevices"][1:])
        positions = compute_node_positions(cache["nodes"], self.connections, self.primary_node)
        for node_id, node in self.nodes.items():
            node["position"] = positions[node_id]
        self.monitored_nodes = {
            node["id"] for node in cache["nodes"] if node.get("monitored", False)
        }
        self.camera = pygame.Vector2(constants.STARTING_CAMERA)
        self.zoom = constants.STARTING_ZOOM
        self.dragging = False
        self.last_mouse = pygame.Vector2(0, 0)
        self.selected = None
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 19)

    def world_to_screen(self, position):
        return pygame.Vector2(position) * self.zoom + self.camera

    def screen_to_world(self, position):
        return (pygame.Vector2(position) - self.camera) / self.zoom

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button in (2, 3):
                self.dragging = True
                self.last_mouse = pygame.Vector2(event.pos)
            elif event.button == 1:
                self.select_at(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP and event.button in (2, 3):
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            current = pygame.Vector2(event.pos)
            self.camera += current - self.last_mouse
            self.last_mouse = current
        elif event.type == pygame.MOUSEWHEEL:
            mouse = pygame.Vector2(pygame.mouse.get_pos())
            before_zoom = self.screen_to_world(mouse)
            self.zoom = max(
                constants.MIN_ZOOM,
                min(constants.MAX_ZOOM, self.zoom * (constants.ZOOM_STEP ** event.y)),
            )
            self.camera = mouse - before_zoom * self.zoom

    def select_at(self, position):
        world_position = self.screen_to_world(position)
        for node_id, node in self.nodes.items():
            if world_position.distance_to(node["position"]) <= constants.node_radius(node["size"]):
                self.selected = ("node", node_id)
                return

        closest = None
        closest_distance = constants.CONNECTION_SELECTION_DISTANCE / self.zoom
        for index, connection in enumerate(self.connections):
            start = self.nodes[connection["from"]]["position"]
            end = self.nodes[connection["to"]]["position"]
            distance = distance_to_segment(world_position, start, end)
            if distance < closest_distance:
                closest = index
                closest_distance = distance
        self.selected = ("connection", closest) if closest is not None else None

    def draw(self, surface):
        self.draw_background(surface)
        for index, connection in enumerate(self.connections):
            self.draw_connection(surface, connection, index)
        for node in self.nodes.values():
            self.draw_node(surface, node)
        self.draw_help(surface)
        if self.selected:
            self.draw_readout(surface)

    def draw_background(self, surface):
        draw_background(surface)

    def draw_connection(self, surface, connection, index):
        start = self.world_to_screen(self.nodes[connection["from"]]["position"])
        end = self.world_to_screen(self.nodes[connection["to"]]["position"])
        selected = self.selected == ("connection", index)
        if connection.get("monitored", False):
            color = constants.MONITORED_CONNECTION_COLOR
        else:
            color = (constants.UNSTABLE_CONNECTION_COLOR
                     if connection.get("stability") == "unstable"
                     else constants.CONNECTION_COLOR)
        if selected:
            color = constants.PLAYER_CONNECTION_COLOR
        width = (constants.STRONG_CONNECTION_WIDTH
                 if connection.get("bandwidth") == "strong"
                 else constants.WEAK_CONNECTION_WIDTH)
        width = max(1, round(width * self.zoom))
        if connection.get("stability") == "unstable":
            draw_dashed_line(surface, color, start, end, width)
        else:
            draw_transparent_line(surface, color, start, end, width)
        if (not connection.get("monitored", False)
                and connection.get("stability") != "unstable"
                and connection.get("bandwidth") == "strong"):
            draw_transparent_line(
                surface,
                constants.PLAYER_CONNECTION_CORE_COLOR,
                start,
                end,
                max(1, round(2 * self.zoom)),
            )
        if connection.get("security") == "encrypted":
            draw_lock(surface, (start + end) / 2, self.zoom)

    def draw_node(self, surface, node):
        position = self.world_to_screen(node["position"])
        radius = max(7, round(constants.node_radius(node["size"]) * self.zoom))
        node_id = node["id"]
        is_primary = node_id == self.primary_node
        is_secondary = node_id in self.secondary_nodes
        is_monitored = node_id in self.monitored_nodes
        selected = self.selected == ("node", node["id"])
        if is_primary or is_secondary:
            if is_primary:
                node_glow = constants.ACTIVE_NODE_GLOW
                node_stroke = constants.ACTIVE_NODE_STROKE
                node_core = constants.ACTIVE_NODE_CORE
                node_inner = constants.ACTIVE_NODE_INNER
                node_center = constants.ACTIVE_NODE_CENTER
            else:
                node_glow = constants.SECONDARY_NODE_GLOW
                node_stroke = constants.SECONDARY_NODE_STROKE
                node_core = constants.SECONDARY_NODE_CORE
                node_inner = constants.SECONDARY_NODE_INNER
                node_center = constants.SECONDARY_NODE_CENTER
            draw_transparent_circle(surface, node_glow, position, radius + round(24 * self.zoom))
            if is_primary:
                draw_transparent_circle(surface, constants.PRIMARY_NODE_RING, position, radius + round(9 * self.zoom), max(1, round(2 * self.zoom)))
            draw_transparent_circle(surface, node_stroke, position, radius, max(2, round(3 * self.zoom)))
            draw_transparent_circle(surface, node_core, position, max(2, radius - round(7 * self.zoom)))
            draw_transparent_circle(surface, node_inner, position, max(2, radius - round(17 * self.zoom)))
            draw_transparent_circle(surface, node_center, position, max(2, round(radius * 0.2)))
            if is_monitored:
                draw_transparent_circle(surface, constants.MONITORED_NODE_STROKE, position, radius + round(13 * self.zoom), max(2, round(2 * self.zoom)))
            if selected:
                draw_transparent_circle(surface, constants.SELECTED_NODE_COLOR, position, radius + 5, 2)
        else:
            fill = constants.MONITORED_NODE_FILL if is_monitored else constants.CACHED_NODE_FILL
            stroke = constants.MONITORED_NODE_STROKE if is_monitored else constants.CACHED_NODE_STROKE
            draw_transparent_circle(surface, fill, position, radius)
            draw_transparent_circle(surface, stroke, position, radius, max(1, round(2 * self.zoom)))
            if is_monitored:
                draw_transparent_circle(surface, constants.MONITOR_MARKER_COLOR, position, max(3, round(5 * self.zoom)))
            if selected:
                draw_transparent_circle(surface, constants.SELECTED_NODE_COLOR, position, radius + 5, 2)
        node_label = node.get("label")
        if node_label and node_label != "Unknown":
            label = self.small_font.render(node_label, True, constants.TEXT_COLOR)
            surface.blit(label, (position.x + radius + 8, position.y - label.get_height() / 2))

    def draw_help(self, surface):
        draw_help(surface, self.small_font)

    def draw_readout(self, surface):
        panel = pygame.Rect(18, 18, 260, 145)
        panel_surface = pygame.Surface(panel.size, pygame.SRCALPHA)
        panel_surface.fill(constants.PANEL_COLOR)
        surface.blit(panel_surface, panel.topleft)
        pygame.draw.rect(surface, constants.CURRENT_COLOR, panel, 1, border_radius=8)
        kind, value = self.selected
        if kind == "node":
            node = self.nodes[value]
            lines = [node.get("label", value), f"ID: {value}",
                     f"State: {node.get('state', 'unknown')}",
                     f"Size: {node.get('size', 'unknown')}"]
        else:
            connection = self.connections[value]
            lines = ["Connection", f"{connection['from']} -> {connection['to']}",
                     f"Bandwidth: {connection.get('bandwidth', 'unknown')}",
                     f"Stability: {connection.get('stability', 'unknown')}",
                     f"Security: {connection.get('security', 'unknown')}"]
        for line_index, line in enumerate(lines):
            font = self.font if line_index == 0 else self.small_font
            label = font.render(line, True, constants.TEXT_COLOR)
            surface.blit(label, (30, 30 + line_index * 23))
