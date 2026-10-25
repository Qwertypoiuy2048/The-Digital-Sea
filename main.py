"""The Digital Sea - first interactive network screen prototype."""

from __future__ import annotations

import json
import math
from pathlib import Path

import pygame

import constants


ROOT = Path(__file__).parent
DATA_DIR = ROOT / "data"


def load_json(filename: str) -> dict:
    with (DATA_DIR / filename).open(encoding="utf-8") as file:
        return json.load(file)


def node_radius(size: str) -> float:
    return constants.node_radius(size)


def draw_transparent_line(surface, color, start, end, width=2):
    layer = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    pygame.draw.line(layer, color, start, end, width)
    surface.blit(layer, (0, 0))


def draw_dashed_line(surface, color, start, end, width=2, dash_length=10):
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


def distance_to_segment(point, start, end) -> float:
    point = pygame.Vector2(point)
    start = pygame.Vector2(start)
    segment = pygame.Vector2(end) - start
    if segment.length_squared() == 0:
        return point.distance_to(start)
    projection = max(0, min(1, (point - start).dot(segment) / segment.length_squared()))
    return point.distance_to(start + segment * projection)


def draw_transparent_circle(surface, color, center, radius, width=0):
    """Draw an RGBA circle by compositing it onto the destination surface."""
    radius = max(1, round(radius))
    layer = pygame.Surface((radius * 2 + 2, radius * 2 + 2), pygame.SRCALPHA)
    pygame.draw.circle(layer, color, (radius + 1, radius + 1), radius, width)
    surface.blit(layer, (center[0] - radius - 1, center[1] - radius - 1))


def compute_node_positions(nodes, connections, primary_id):
    """Place nodes in deterministic rings based on graph distance from primary."""
    node_ids = [node["id"] for node in nodes]
    adjacency = {node_id: [] for node_id in node_ids}
    for connection in connections:
        start = connection["from"]
        end = connection["to"]
        if start in adjacency and end in adjacency:
            adjacency[start].append(end)
            adjacency[end].append(start)

    root = primary_id if primary_id in adjacency else (node_ids[0] if node_ids else None)
    distances = {root: 0} if root else {}
    pending = [root] if root else []
    while pending:
        current = pending.pop(0)
        for neighbor in adjacency[current]:
            if neighbor not in distances:
                distances[neighbor] = distances[current] + 1
                pending.append(neighbor)

    # Disconnected nodes are placed after the connected graph.
    next_distance = max(distances.values(), default=0) + 1
    for node_id in node_ids:
        if node_id not in distances:
            distances[node_id] = next_distance

    layers = {}
    for node_id, distance in distances.items():
        layers.setdefault(distance, []).append(node_id)

    positions = {}
    center = pygame.Vector2(constants.NETWORK_CENTER)
    for distance, layer_nodes in layers.items():
        if distance == 0:
            positions[layer_nodes[0]] = center
            continue
        radius = constants.NETWORK_LAYER_SPACING * distance
        for index, node_id in enumerate(layer_nodes):
            angle = -math.pi / 2 + (2 * math.pi * index / len(layer_nodes))
            positions[node_id] = center + pygame.Vector2(math.cos(angle), math.sin(angle)) * radius
    return positions


class NetworkScreen:
    def __init__(self, player: dict, cache: dict):
        self.player = player
        self.nodes = {node["id"]: node for node in cache["nodes"]}
        self.connections = cache["connections"]
        active_nodes = player.get("activeNodes", {})
        self.primary_node = active_nodes.get("primary")
        self.secondary_nodes = set(active_nodes.get("secondary", []))
        # Temporary compatibility with the earlier player-file key.
        if not self.primary_node and player.get("activeDevices"):
            self.primary_node = player["activeDevices"][0]
            self.secondary_nodes = set(player["activeDevices"][1:])
        positions = compute_node_positions(cache["nodes"], self.connections, self.primary_node)
        for node_id, node in self.nodes.items():
            node["position"] = positions[node_id]
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
            if world_position.distance_to(node["position"]) <= node_radius(node["size"]):
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
        surface.fill(constants.BACKGROUND_COLOR)

    def draw_connection(self, surface, connection, index):
        start = self.world_to_screen(self.nodes[connection["from"]]["position"])
        end = self.world_to_screen(self.nodes[connection["to"]]["position"])
        selected = self.selected == ("connection", index)
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
        if connection.get("stability") != "unstable" and connection.get("bandwidth") == "strong":
            draw_transparent_line(
                surface,
                constants.PLAYER_CONNECTION_CORE_COLOR,
                start,
                end,
                max(1, round(2 * self.zoom)),
            )

    def draw_node(self, surface, node):
        position = self.world_to_screen(node["position"])
        radius = max(7, round(node_radius(node["size"]) * self.zoom))
        node_id = node["id"]
        is_primary = node_id == self.primary_node
        is_secondary = node_id in self.secondary_nodes
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

            # Active nodes use the layered cyan treatment from the SVG mockup.
            draw_transparent_circle(surface, node_glow, position, radius + round(24 * self.zoom))
            if is_primary:
                draw_transparent_circle(surface, constants.PRIMARY_NODE_RING, position, radius + round(9 * self.zoom), max(1, round(2 * self.zoom)))
            draw_transparent_circle(surface, node_stroke, position, radius, max(2, round(3 * self.zoom)))
            draw_transparent_circle(surface, node_core, position, max(2, radius - round(7 * self.zoom)))
            draw_transparent_circle(surface, node_inner, position, max(2, radius - round(17 * self.zoom)))
            draw_transparent_circle(surface, node_center, position, max(2, round(radius * 0.2)))
            if selected:
                draw_transparent_circle(surface, constants.SELECTED_NODE_COLOR, position, radius + 5, 2)
        else:
            # Cached devices are deliberately quieter and more transparent.
            draw_transparent_circle(surface, constants.CACHED_NODE_FILL, position, radius)
            draw_transparent_circle(surface, constants.CACHED_NODE_STROKE, position, radius, max(1, round(2 * self.zoom)))
            if selected:
                draw_transparent_circle(surface, constants.SELECTED_NODE_COLOR, position, radius + 5, 2)
        node_label = node.get("label")
        if node_label and node_label != "Unknown":
            label = self.small_font.render(node_label, True, constants.TEXT_COLOR)
            surface.blit(label, (position.x + radius + 8, position.y - label.get_height() / 2))

    def draw_help(self, surface):
        text = "LEFT: inspect   WHEEL: zoom   MIDDLE/RIGHT DRAG: pan"
        label = self.small_font.render(text, True, constants.MUTED_TEXT_COLOR)
        surface.blit(label, (18, surface.get_height() - label.get_height() - 18))

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


def main():
    pygame.init()
    pygame.display.set_caption(constants.WINDOW_TITLE)
    screen = pygame.display.set_mode(constants.WINDOW_SIZE, pygame.RESIZABLE)
    clock = pygame.time.Clock()
    network = NetworkScreen(load_json("player.json"), load_json("network_cache.json"))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                network.handle_event(event)
        network.draw(screen)
        pygame.display.flip()
        clock.tick(constants.FRAME_RATE)

    pygame.quit()


if __name__ == "__main__":
    main()
