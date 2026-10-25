"""Layout logic for placing network nodes in world space."""

from __future__ import annotations

import math

import pygame

import constants


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
