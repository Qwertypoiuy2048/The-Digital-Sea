import copy
import os
import unittest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
import pygame

import constants
from code_layout import DESIGN_SIZE, scale_rect, screen_rects, telemetry_rects
from code_screen import CodeScreen
from data_loader import load_json
from network_layout import compute_node_positions
from network_screen import NetworkScreen, distance_to_segment
from screen_manager import ScreenManager


class LayoutTests(unittest.TestCase):
    def test_scale_rect_preserves_design_size(self):
        self.assertEqual(scale_rect((1, 2, 3, 4), DESIGN_SIZE), pygame.Rect(1, 2, 3, 4))

    def test_scale_rect_scales_all_edges(self):
        self.assertEqual(scale_rect((10, 20, 100, 50), (720, 405)), pygame.Rect(5, 10, 50, 25))

    def test_code_layout_regions_are_inside_surface_at_design_size(self):
        surface = pygame.Rect((0, 0), DESIGN_SIZE)
        for rect in screen_rects(DESIGN_SIZE).values():
            self.assertTrue(surface.contains(rect), rect)
        self.assertEqual(len(telemetry_rects(DESIGN_SIZE)), 4)

    def test_network_positions_are_deterministic_and_cover_all_nodes(self):
        nodes = [{"id": str(i), "size": "small"} for i in range(4)]
        connections = [{"from": "0", "to": "1"}, {"from": "1", "to": "2"}]
        first = compute_node_positions(nodes, connections, "0")
        second = compute_node_positions(nodes, connections, "0")
        self.assertEqual(first, second)
        self.assertEqual(set(first), {"0", "1", "2", "3"})
        self.assertEqual(first["0"], pygame.Vector2(constants.NETWORK_CENTER))

    def test_network_positions_fallback_to_first_node_and_disconnected_ring(self):
        nodes = [{"id": "a"}, {"id": "b"}]
        positions = compute_node_positions(nodes, [], "missing")
        self.assertEqual(set(positions), {"a", "b"})
        self.assertNotEqual(positions["a"], positions["b"])

    def test_distance_to_segment_handles_projection_and_zero_length(self):
        self.assertAlmostEqual(distance_to_segment((5, 2), (0, 0), (10, 0)), 2)
        self.assertAlmostEqual(distance_to_segment((20, 0), (0, 0), (10, 0)), 10)
        self.assertAlmostEqual(distance_to_segment((3, 4), (0, 0), (0, 0)), 5)


class PygameScreenTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        cls.state_fixture = {
            "player": load_json("player.json"),
            "module_catalog": load_json("modules.json"),
            "cached_modules": load_json("cached_modules.json"),
            "network_cache": load_json("network_cache.json"),
        }

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def state(self):
        return copy.deepcopy(self.state_fixture)

    def test_code_screen_draws_at_default_and_resized_surfaces(self):
        code = CodeScreen(self.state())
        for size in ((1000, 800), (1440, 810), (640, 480)):
            surface = pygame.Surface(size, pygame.SRCALPHA)
            code.draw(surface)
            self.assertEqual(surface.get_size(), size)

    def test_network_screen_draws_and_assigns_positions_without_mutating_cache_shape(self):
        state = self.state()
        network = NetworkScreen(state)
        surface = pygame.Surface((1000, 800), pygame.SRCALPHA)
        network.draw(surface)
        self.assertEqual(set(network.nodes), {node["id"] for node in state["network_cache"]["nodes"]})
        self.assertTrue(all("position" in node for node in network.nodes.values()))

    def test_network_coordinate_conversion_round_trips(self):
        network = NetworkScreen(self.state())
        point = pygame.Vector2(123.5, -42.25)
        self.assertTrue(network.screen_to_world(network.world_to_screen(point)).distance_to(point) < 0.001)

    def test_network_mouse_selection_drag_and_zoom_are_bounded(self):
        network = NetworkScreen(self.state())
        node_position = network.world_to_screen(network.nodes["001"]["position"])
        network.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": node_position}))
        self.assertEqual(network.selected, ("node", "001"))
        network.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 3, "pos": (10, 10)}))
        network.handle_event(pygame.event.Event(pygame.MOUSEMOTION, {"pos": (20, 25)}))
        network.handle_event(pygame.event.Event(pygame.MOUSEBUTTONUP, {"button": 3, "pos": (20, 25)}))
        self.assertFalse(network.dragging)
        for _ in range(100):
            network.handle_event(pygame.event.Event(pygame.MOUSEWHEEL, {"y": 1}))
        self.assertEqual(network.zoom, constants.MAX_ZOOM)
        for _ in range(100):
            network.handle_event(pygame.event.Event(pygame.MOUSEWHEEL, {"y": -1}))
        self.assertEqual(network.zoom, constants.MIN_ZOOM)

    def test_code_click_selects_module_and_scroll_clamps(self):
        code = CodeScreen(self.state())
        surface = pygame.Surface((1000, 800), pygame.SRCALPHA)
        code.draw(surface)
        module_id, hitbox = next(iter(code.module_hitboxes.items()))
        code.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": hitbox.center}))
        self.assertEqual(code.selected_module_id, module_id)
        code.handle_event(pygame.event.Event(pygame.MOUSEWHEEL, {"y": -100, "pos": (500, 400)}))
        self.assertGreaterEqual(code.scroll_offsets["workspace"], 0)
        workspace = screen_rects(surface.get_size())["workspace"]
        self.assertLessEqual(code.scroll_offsets["workspace"], max(0, code.content_heights["workspace"] - workspace.height))

    def test_screen_manager_routes_events_and_draws_active_screen(self):
        code = CodeScreen(self.state())
        network = NetworkScreen(self.state())
        manager = ScreenManager({"code": code, "network": network}, "code")
        surface = pygame.Surface((1000, 800), pygame.SRCALPHA)
        manager.draw(surface)
        manager.set_screen("network")
        manager.draw(surface)
        self.assertIs(manager.active_screen, network)
        with self.assertRaises(KeyError):
            manager.set_screen("missing")


if __name__ == "__main__":
    unittest.main()
