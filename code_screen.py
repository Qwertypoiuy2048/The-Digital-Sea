"""Read-only Code screen driven by the loaded player and module data."""

from __future__ import annotations

import pygame

import constants
from code_layout import screen_rects, telemetry_rects, scale_rect
from data_loader import update_player_data
from drawing import draw_background
from program_runtime import (
    add_module_instance,
    adjust_module_compute,
    build_program_runtime,
    add_extension_to_instance,
    extension_add_error,
    module_compute_error,
    module_add_error,
    remove_extension_from_instance,
    remove_module_instance,
)
from screen import Screen


class CodeScreen(Screen):
    """Display the active program and derived runtime state without editing it."""

    def __init__(self, state: dict):
        self.player = state["player"]
        self.module_catalog = state.get("module_catalog", {})
        self.cached_modules = state.get("cached_modules", {})
        self.runtime = build_program_runtime(self.player, self.module_catalog,
                                             cached_modules=self.cached_modules)
        self.font = pygame.font.Font(None, 25)
        self.small_font = pygame.font.Font(None, 18)
        self.tiny_font = pygame.font.Font(None, 15)
        self.scroll_offsets = {"library": 0, "workspace": 0, "state": 0}
        self.content_heights = {"library": 0, "workspace": 0, "state": 0}
        self.surface_size = constants.WINDOW_SIZE
        self.mouse_position = (0, 0)
        self.hovered_library_item = None
        self.module_hitboxes = {}
        self.selected_module_id = None
        self.module_menu_rect = None
        self.module_action_rects = {}
        self.extension_removal_rects = {}
        self.extension_removal_mode = False
        self.library_module_hitboxes = {}
        self.selected_library_module_id = None
        self.add_module_menu_rect = None
        self.add_module_button_rect = None
        self.library_extension_hitboxes = {}
        self.selected_sidebar_extension_id = None
        self.sidebar_extension_menu_rect = None
        self.extension_add_rects = {}
        self.extension_add_mode = False
        self.extension_target_rects = {}

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.mouse_position = event.pos
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.add_module_button_rect is not None and self.add_module_button_rect.collidepoint(event.pos):
                self.add_selected_library_module()
            elif self.add_module_menu_rect is not None and self.add_module_menu_rect.collidepoint(event.pos):
                pass
            elif self.sidebar_extension_menu_rect is not None and self.sidebar_extension_menu_rect.collidepoint(event.pos):
                extension_id = next(
                    (value for value, rect in self.extension_target_rects.items()
                     if rect.collidepoint(event.pos)), None
                )
                if extension_id:
                    self.add_sidebar_extension_to_module(extension_id)
            elif self.module_menu_rect is not None and self.module_menu_rect.collidepoint(event.pos):
                if self.module_action_rects.get("REMOVE MODULE", pygame.Rect(0, 0, 0, 0)).collidepoint(event.pos):
                    self.remove_selected_module()
                elif self.module_action_rects.get("INCREASE COMPUTE", pygame.Rect(0, 0, 0, 0)).collidepoint(event.pos):
                    self.adjust_selected_compute(1)
                elif self.module_action_rects.get("DECREASE COMPUTE", pygame.Rect(0, 0, 0, 0)).collidepoint(event.pos):
                    self.adjust_selected_compute(-1)
                elif self.module_action_rects.get("REMOVE EXTENSION", pygame.Rect(0, 0, 0, 0)).collidepoint(event.pos):
                    self.extension_removal_mode = True
                    self.extension_add_mode = False
                elif self.module_action_rects.get("ADD EXTENSION", pygame.Rect(0, 0, 0, 0)).collidepoint(event.pos):
                    self.extension_add_mode = True
                    self.extension_removal_mode = False
                elif self.extension_add_mode:
                    extension_id = next(
                        (value for value, rect in self.extension_add_rects.items()
                         if rect.collidepoint(event.pos)), None
                    )
                    if extension_id:
                        self.add_selected_extension(extension_id)
                elif self.extension_removal_mode:
                    extension_id = next(
                        (value for value, rect in self.extension_removal_rects.items()
                         if rect.collidepoint(event.pos)),
                        None,
                    )
                    if extension_id:
                        self.remove_selected_extension(extension_id)
            else:
                clicked_module = next(
                    (instance_id for instance_id, rect in self.module_hitboxes.items()
                     if rect.collidepoint(event.pos)),
                    None,
                )
                if clicked_module:
                    self.selected_module_id = clicked_module
                    self.extension_removal_mode = False
                    self.extension_add_mode = False
                else:
                    clicked_library_module = next(
                        (definition_id for definition_id, rect in self.library_module_hitboxes.items()
                         if rect.collidepoint(event.pos)), None
                    )
                    if clicked_library_module is not None:
                        self.selected_library_module_id = clicked_library_module
                        self.selected_sidebar_extension_id = None
                        self.sidebar_extension_menu_rect = None
                    else:
                        clicked_library_extension = next(
                            (extension_id for extension_id, rect in self.library_extension_hitboxes.items()
                             if rect.collidepoint(event.pos)), None
                        )
                        if clicked_library_extension is not None:
                            self.selected_sidebar_extension_id = clicked_library_extension
                            self.selected_module_id = None
                            self.selected_library_module_id = None
                            self.add_module_menu_rect = None
                            self.extension_removal_mode = False
                            self.extension_add_mode = False
                        else:
                            self.selected_sidebar_extension_id = None
                            self.sidebar_extension_menu_rect = None
                            self.selected_module_id = None
                            self.extension_removal_mode = False
                            self.selected_library_module_id = None
        if event.type == pygame.MOUSEWHEEL:
            rects = screen_rects(self.surface_size)
            position = getattr(event, "pos", self.mouse_position)
            if position == (0, 0):
                position = pygame.mouse.get_pos()
            for region in ("library", "workspace", "state"):
                if rects[region].collidepoint(position):
                    self.scroll_offsets[region] -= event.y * 32
                    self.clamp_scroll(region, rects[region])
                    break
        return None

    def draw(self, surface):
        self.surface_size = surface.get_size()
        draw_background(surface)
        rects = screen_rects(surface.get_size())
        self.draw_telemetry(surface)
        self.draw_library(surface, rects["library"], self.scroll_offsets["library"])
        self.draw_workspace(surface, rects["workspace"], self.scroll_offsets["workspace"])
        self.draw_state(surface, rects["state"], self.scroll_offsets["state"])
        footer = self.render("READ-ONLY PREVIEW // PLAYER DATA", self.tiny_font,
                             constants.MUTED_TEXT_COLOR)
        surface.blit(footer, (18, surface.get_height() - footer.get_height() - 18))
        # Popups are rendered last so they sit above every panel and card.
        self.draw_library_status_bubble(surface)
        self.draw_module_menu(surface, rects["workspace"])
        self.draw_add_module_menu(surface, rects["library"])
        self.draw_sidebar_extension_menu(surface, rects["library"])

    def clamp_scroll(self, region, viewport):
        maximum = max(0, self.content_heights[region] - viewport.height)
        self.scroll_offsets[region] = max(0, min(self.scroll_offsets[region], maximum))

    def begin_panel_content(self, surface, viewport, top_padding=0, bottom_padding=0):
        """Draw a panel and clip scrolling content between fixed top/bottom areas."""
        old_clip = surface.get_clip()
        content_rect = pygame.Rect(
            viewport.x + 2,
            viewport.y + top_padding,
            viewport.width - 4,
            viewport.height - top_padding - bottom_padding,
        )
        surface.set_clip(content_rect)
        return old_clip

    def end_panel_content(self, surface, viewport, old_clip):
        surface.set_clip(old_clip)
        pygame.draw.rect(surface, constants.CODE_PANEL_BORDER, viewport,
                         width=1, border_radius=8)

    def render(self, text, font, color=constants.TEXT_COLOR):
        return font.render(str(text), True, color)

    def wrapped_lines(self, text, font, max_width, max_lines=None):
        words = str(text).split()
        lines = []
        current = ""
        for word in words:
            candidate = word if not current else f"{current} {word}"
            if font.size(candidate)[0] <= max_width:
                current = candidate
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        if max_lines is None or len(lines) <= max_lines:
            return lines
        lines = lines[:max_lines]
        last = lines[-1]
        while last and font.size(f"{last}...")[0] > max_width:
            last = last[:-1]
        lines[-1] = f"{last.rstrip()}..."
        return lines

    def draw_wrapped(self, surface, text, font, color, rect, max_lines=None):
        line_height = font.get_height()
        for index, line in enumerate(self.wrapped_lines(text, font, rect.width, max_lines)):
            surface.blit(self.render(line, font, color), (rect.x, rect.y + index * line_height))

    def panel(self, surface, rect, border=constants.CODE_PANEL_BORDER):
        pygame.draw.rect(surface, constants.CODE_PANEL_COLOR, rect, border_radius=8)
        pygame.draw.rect(surface, border, rect, width=1, border_radius=8)

    def draw_telemetry(self, surface):
        compute = self.runtime["compute"]
        memory = self.runtime["memory"]
        labels = [
            ("PLAYER", self.player.get("playerId", "unknown"), constants.CODE_TEAL, None),
            ("COMPUTE", f"{compute['used']} / {compute['capacity']} CU", constants.CODE_BLUE, compute),
            ("MEMORY", f"{memory['used']} / {memory['capacity']} MB", constants.CODE_PURPLE, memory),
            ("CORES", f"{self.runtime['cores']['used']} / {self.runtime['cores']['capacity']}", constants.CODE_AMBER, self.runtime["cores"]),
        ]
        for rect, (label, value, color, resource) in zip(telemetry_rects(surface.get_size()), labels):
            self.panel(surface, rect)
            over_capacity = resource is not None and resource["used"] > resource["capacity"]
            display_color = constants.CODE_ERROR if over_capacity else color
            surface.blit(self.render(label, self.tiny_font, constants.CODE_MUTED),
                         (rect.x + 16, rect.y + 18))
            surface.blit(self.render(value, self.font, constants.TEXT_COLOR),
                         (rect.x + 16, rect.y + 45))
            if resource is not None:
                if over_capacity:
                    surface.blit(self.render("ERROR: OVER CAPACITY", self.tiny_font, display_color),
                                 (rect.x + 16, rect.bottom - 35))
                bar = pygame.Rect(rect.x + 16, rect.bottom - 12, rect.width - 32, 5)
                ratio = min(1, resource["used"] / resource["capacity"]) if resource["capacity"] else 0
                pygame.draw.rect(surface, constants.CODE_ITEM_COLOR, bar, border_radius=2)
                pygame.draw.rect(surface, display_color,
                                 pygame.Rect(bar.x, bar.y, max(20, round(bar.width * ratio)), bar.height),
                                 border_radius=2)

    def draw_library(self, surface, rect, scroll=0):
        self.hovered_library_item = None
        self.library_module_hitboxes = {}
        self.library_extension_hitboxes = {}
        entries = self.library_entries()
        modules = [entry for entry in entries if entry["kind"] == "module"]
        extensions = [entry for entry in entries if entry["kind"] == "extension"]
        extension_types = sorted({entry["type"] for entry in extensions})
        required_height = 90
        if modules:
            required_height += 30 + len(modules) * 40
        if extensions:
            required_height += 48
            required_height += sum(
                30 + sum(entry["type"] == extension_type for entry in extensions) * 40
                for extension_type in extension_types
            )
        required_height += 65
        self.content_heights["library"] = required_height
        self.clamp_scroll("library", rect)
        self.panel(surface, rect)
        x = rect.x + 18
        surface.blit(self.render("CODE LIBRARY", self.font, constants.TEXT_COLOR), (x, rect.y + 25))
        surface.blit(self.render("current availability", self.tiny_font, constants.CODE_MUTED),
                     (x, rect.y + 53))
        old_clip = self.begin_panel_content(surface, rect, top_padding=78, bottom_padding=58)
        panel_rect = rect.move(0, -self.scroll_offsets["library"])
        panel_rect.height = required_height
        x = panel_rect.x + 18
        offset = 90
        if modules:
            self.library_section(surface, x, panel_rect.y + offset, "MODULES", constants.CODE_TEAL)
            offset += 30
            offset = self.draw_library_items(surface, panel_rect, offset, modules)
        if extensions:
            offset += 12
            self.library_section(surface, x, panel_rect.y + offset, "EXTENSIONS", constants.CODE_PURPLE)
            offset += 30
            for extension_type in extension_types:
                type_label = extension_type.replace("Type", " Type").upper()
                self.library_section(surface, x + 8, panel_rect.y + offset,
                                     type_label, constants.CODE_PURPLE)
                offset += 24
                typed_extensions = [entry for entry in extensions if entry["type"] == extension_type]
                offset = self.draw_library_items(surface, panel_rect, offset, typed_extensions)

        memory = self.runtime["memory"]
        self.end_panel_content(surface, rect, old_clip)
        self.draw_resource_bar(surface, pygame.Rect(rect.x + 18, rect.bottom - 48, rect.width - 36, 28),
                               "MEMORY", memory["used"], memory["capacity"], constants.CODE_PURPLE, "MB")

    def draw_library_items(self, surface, panel_rect, offset, entries):
        colors = {
            "IN USE": constants.CODE_TEAL,
            "READY": constants.CODE_BLUE,
            "NOT ENOUGH COMPUTE": constants.CODE_AMBER,
        }
        for entry in entries:
            item_rect = self.library_item(surface, panel_rect, offset, entry["name"], entry["cost"],
                                          colors[entry["status"]])
            if entry["kind"] == "module":
                self.library_module_hitboxes[entry["id"]] = item_rect.copy()
            else:
                self.library_extension_hitboxes[entry["id"]] = item_rect.copy()
            if item_rect.collidepoint(self.mouse_position):
                self.hovered_library_item = {**entry, "rect": item_rect.copy()}
            offset += 40
        return offset

    def library_entries(self):
        available_compute = self.runtime["compute"]["available"]
        active_modules = {module["definitionId"] for module in self.runtime["modules"]}
        active_extensions = set(self.runtime["extensions"])
        entries = []
        for module_id in self.cached_modules.get("modules", []):
            definition = self.module_catalog.get("modules", {}).get(module_id, {})
            cost = int(definition.get("mediumCompute", definition.get("lowCompute", 0)))
            status = "IN USE" if module_id in active_modules else (
                "READY" if cost <= available_compute else "NOT ENOUGH COMPUTE")
            entries.append({
                "id": module_id,
                "name": definition.get("name", module_id), "cost": f"{cost} CU",
                "status": status, "kind": "module", "type": "module",
            })
        for extension_id in self.cached_modules.get("extensions", []):
            definition = self.module_catalog.get("extensions", {}).get(extension_id, {})
            cost = int(definition.get("computeCost", 0))
            status = "IN USE" if extension_id in active_extensions else (
                "READY" if cost <= available_compute else "NOT ENOUGH COMPUTE")
            entries.append({
                "id": extension_id,
                "name": definition.get("name", extension_id), "cost": f"{cost} CU",
                "status": status, "kind": "extension", "type": definition.get("type", "unknown"),
            })
        return entries

    def library_section(self, surface, x, y, title, color):
        pygame.draw.circle(surface, color, (x + 5, y + 5), 5)
        surface.blit(self.render(title, self.tiny_font, color), (x + 18, y - 3))

    def library_item(self, surface, rect, offset, label, cost, color):
        item = pygame.Rect(rect.x + 18, rect.y + offset, rect.width - 36, 33)
        pygame.draw.rect(surface, constants.CODE_ITEM_COLOR, item, border_radius=5)
        pygame.draw.rect(surface, color, item, width=1, border_radius=5)
        self.draw_wrapped(surface, label.upper(), self.tiny_font, constants.TEXT_COLOR,
                          pygame.Rect(item.x + 10, item.y + 5, item.width - 75, item.height - 8))
        value = self.render(cost, self.tiny_font, color)
        surface.blit(value, (item.right - value.get_width() - 10, item.y + 10))
        return item

    def draw_library_status_bubble(self, surface):
        if not self.hovered_library_item:
            return
        item = self.hovered_library_item
        bubble = pygame.Rect(item["rect"].right + 10, item["rect"].y, 210, 62)
        if bubble.right > surface.get_width() - 8:
            bubble.x = item["rect"].left - bubble.width - 10
        if bubble.bottom > surface.get_height() - 8:
            bubble.bottom = surface.get_height() - 8
        layer = pygame.Surface(bubble.size, pygame.SRCALPHA)
        layer.fill((9, 24, 35, 245))
        surface.blit(layer, bubble.topleft)
        color = {
            "IN USE": constants.CODE_TEAL,
            "READY": constants.CODE_BLUE,
            "NOT ENOUGH COMPUTE": constants.CODE_AMBER,
        }[item["status"]]
        pygame.draw.rect(surface, color, bubble, width=2, border_radius=6)
        surface.blit(self.render(item["status"], self.tiny_font, color),
                     (bubble.x + 10, bubble.y + 9))
        surface.blit(self.render(item["name"], self.tiny_font, constants.TEXT_COLOR),
                     (bubble.x + 10, bubble.y + 28))
        surface.blit(self.render(f"COMPUTE  {item['cost']}", self.tiny_font, constants.CODE_MUTED),
                     (bubble.x + 10, bubble.y + 45))

    def draw_add_module_menu(self, surface, library_rect):
        if not self.selected_library_module_id:
            self.add_module_menu_rect = None
            self.add_module_button_rect = None
            return
        definition = self.module_catalog.get("modules", {}).get(self.selected_library_module_id, {})
        item_rect = self.library_module_hitboxes.get(self.selected_library_module_id)
        if item_rect is None:
            item_rect = pygame.Rect(library_rect.right + 10, library_rect.y + 90, 1, 1)
        error = module_add_error(self.player, self.module_catalog, self.cached_modules,
                                 self.selected_library_module_id)
        menu_height = 154 if error is None else 190
        menu = pygame.Rect(item_rect.right + 10, item_rect.y, 250, menu_height)
        if menu.right > surface.get_width() - 8:
            menu.x = item_rect.left - menu.width - 10
        menu.y = max(8, min(menu.y, surface.get_height() - menu.height - 8))
        self.add_module_menu_rect = menu
        layer = pygame.Surface(menu.size, pygame.SRCALPHA)
        layer.fill((8, 22, 32, 250))
        surface.blit(layer, menu.topleft)
        border = constants.CODE_ERROR if error else constants.CODE_TEAL
        pygame.draw.rect(surface, border, menu, width=2, border_radius=8)
        surface.blit(self.render("ADD MODULE", self.small_font, constants.TEXT_COLOR),
                     (menu.x + 16, menu.y + 14))
        self.draw_wrapped(surface, definition.get("name", self.selected_library_module_id),
                          self.tiny_font, constants.CODE_MUTED,
                          pygame.Rect(menu.x + 16, menu.y + 38, menu.width - 32, 24), max_lines=1)
        button = pygame.Rect(menu.x + 16, menu.y + 70, menu.width - 32, 30)
        self.add_module_button_rect = button
        pygame.draw.rect(surface, constants.CODE_ITEM_COLOR, button, border_radius=5)
        pygame.draw.rect(surface, border, button, width=2, border_radius=5)
        surface.blit(self.render("ADD MODULE", self.tiny_font, border),
                     (button.x + 10, button.y + 8))
        if error:
            surface.blit(self.render("ERROR", self.tiny_font, constants.CODE_ERROR),
                         (menu.x + 16, menu.y + 108))
            self.draw_wrapped(surface, error, self.tiny_font, constants.CODE_ERROR,
                              pygame.Rect(menu.x + 16, menu.y + 125, menu.width - 32, 48))
        else:
            surface.blit(self.render("medium tier", self.tiny_font, constants.CODE_BLUE),
                         (menu.x + 16, menu.y + 112))

    def compatible_extension_ids(self, module):
        definition = self.module_catalog.get("modules", {}).get(module["definitionId"], {})
        compatible_types = set(definition.get("necessaryExtensions", []) +
                               definition.get("optionalExtensions", []))
        attached = set(module.get("extensions", []))
        return [
            extension_id for extension_id in self.cached_modules.get("extensions", [])
            if extension_id not in attached and
            self.module_catalog.get("extensions", {}).get(extension_id, {}).get("type") in compatible_types
        ]

    def draw_sidebar_extension_menu(self, surface, library_rect):
        if not self.selected_sidebar_extension_id:
            self.sidebar_extension_menu_rect = None
            self.extension_target_rects = {}
            return
        definition = self.module_catalog.get("extensions", {}).get(self.selected_sidebar_extension_id, {})
        targets = [
            module for module in self.runtime["modules"]
            if self.selected_sidebar_extension_id in self.compatible_extension_ids(module)
        ]
        item_rect = self.library_extension_hitboxes.get(self.selected_sidebar_extension_id)
        if item_rect is None:
            item_rect = pygame.Rect(library_rect.right + 10, library_rect.y + 90, 1, 1)
        menu = pygame.Rect(item_rect.right + 10, item_rect.y, 270, 112 + len(targets) * 29)
        if menu.right > surface.get_width() - 8:
            menu.x = item_rect.left - menu.width - 10
        menu.y = max(8, min(menu.y, surface.get_height() - menu.height - 8))
        self.sidebar_extension_menu_rect = menu
        self.extension_target_rects = {}
        layer = pygame.Surface(menu.size, pygame.SRCALPHA)
        layer.fill((8, 22, 32, 250))
        surface.blit(layer, menu.topleft)
        pygame.draw.rect(surface, constants.CODE_PURPLE, menu, width=2, border_radius=8)
        surface.blit(self.render("ADD EXTENSION", self.small_font, constants.TEXT_COLOR),
                     (menu.x + 16, menu.y + 14))
        self.draw_wrapped(surface, definition.get("name", self.selected_sidebar_extension_id),
                          self.tiny_font, constants.CODE_PURPLE,
                          pygame.Rect(menu.x + 16, menu.y + 38, menu.width - 32, 22), max_lines=1)
        surface.blit(self.render("SELECT MODULE INSTANCE", self.tiny_font, constants.CODE_AMBER),
                     (menu.x + 16, menu.y + 66))
        if not targets:
            surface.blit(self.render("NO COMPATIBLE MODULES", self.tiny_font, constants.CODE_ERROR),
                         (menu.x + 16, menu.y + 88))
        for index, module in enumerate(targets):
            row = pygame.Rect(menu.x + 16, menu.y + 88 + index * 29, menu.width - 32, 23)
            self.extension_target_rects[module["instanceId"]] = row
            error = extension_add_error(self.player, self.module_catalog,
                                        self.cached_modules, module["instanceId"],
                                        self.selected_sidebar_extension_id)
            row_color = constants.CODE_ERROR if error else constants.CODE_TEAL
            pygame.draw.rect(surface, constants.CODE_ITEM_COLOR, row, border_radius=4)
            pygame.draw.rect(surface, row_color, row, width=1, border_radius=4)
            surface.blit(self.render(module["instanceId"], self.tiny_font, row_color),
                         (row.x + 9, row.y + 5))

    def add_selected_extension(self, extension_id):
        if not self.selected_module_id:
            return
        if add_extension_to_instance(self.player, self.module_catalog, self.cached_modules,
                                     self.selected_module_id, extension_id):
            update_player_data(self.player)
            self.runtime = build_program_runtime(
                self.player, self.module_catalog, cached_modules=self.cached_modules
            )
            self.extension_add_mode = False
            self.module_menu_rect = None
            self.module_action_rects = {}
            self.extension_add_rects = {}

    def add_sidebar_extension_to_module(self, instance_id):
        if not self.selected_sidebar_extension_id:
            return
        if add_extension_to_instance(
                self.player, self.module_catalog, self.cached_modules,
                instance_id, self.selected_sidebar_extension_id):
            update_player_data(self.player)
            self.runtime = build_program_runtime(
                self.player, self.module_catalog, cached_modules=self.cached_modules
            )
            self.selected_sidebar_extension_id = None
            self.sidebar_extension_menu_rect = None
            self.extension_target_rects = {}

    def add_selected_library_module(self):
        if not self.selected_library_module_id:
            return
        error = module_add_error(self.player, self.module_catalog, self.cached_modules,
                                 self.selected_library_module_id)
        if error:
            return
        instance_id = add_module_instance(
            self.player, self.module_catalog, self.cached_modules,
            self.selected_library_module_id,
        )
        if instance_id:
            update_player_data(self.player)
            self.runtime = build_program_runtime(
                self.player,
                self.module_catalog,
                cached_modules=self.cached_modules,
            )
            self.selected_library_module_id = None
            self.add_module_menu_rect = None
            self.add_module_button_rect = None

    def draw_workspace(self, surface, workspace, scroll=0):
        self.module_hitboxes = {}
        self.panel(surface, workspace)
        surface.blit(self.render("MAIN PROGRAM", self.font, constants.TEXT_COLOR),
                     (workspace.x + 20, workspace.y + 25))
        surface.blit(self.render("read-only configuration preview", self.tiny_font, constants.CODE_MUTED),
                     (workspace.x + 20, workspace.y + 54))
        old_clip = self.begin_panel_content(surface, workspace, top_padding=78, bottom_padding=12)
        content_offset = self.scroll_offsets["workspace"]
        header = scale_rect((350, 236, 750, 48), surface.get_size()).move(0, -content_offset)
        pygame.draw.rect(surface, constants.CODE_HEADER, header, border_radius=8)
        pygame.draw.rect(surface, constants.CODE_TEAL, header, width=1, border_radius=8)
        player_id = self.player.get("playerId", "unknown")
        surface.blit(self.render(f"PROGRAM INSTANCE // {player_id}", self.small_font),
                     (header.x + 22, header.y + 15))

        y = 305
        for module in self.runtime["modules"]:
            definition = self.module_catalog.get("modules", {}).get(module["definitionId"], {})
            description_lines = self.wrapped_lines(
                definition.get("description", "No description available"),
                self.tiny_font, 324
            )
            module_height = max(92, 75 + len(description_lines) * self.tiny_font.get_height())
            module_rect = scale_rect((350, y, 360, module_height), surface.get_size()).move(0, -content_offset)
            self.module_hitboxes[module["instanceId"]] = module_rect.copy()
            self.module_card(surface, module_rect, module)
            extension_x = 735
            extension_height = 56
            extension_lines = []
            for extension_id in module["extensions"]:
                extension_name = self.module_catalog.get("extensions", {}).get(extension_id, {}).get(
                    "name", extension_id)
                extension_lines.append((
                    extension_id,
                    self.wrapped_lines(extension_name.upper(), self.tiny_font, 225),
                    module.get("extensionCosts", {}).get(
                        extension_id, self.module_catalog.get("extensions", {}).get(extension_id, {}).get("computeCost", 0)
                    ),
                ))
            if extension_lines:
                extension_height = max(56, 24 + sum(max(1, len(lines)) for _, lines, _ in extension_lines)
                                       * self.tiny_font.get_height() + 18)
                extension_rect = scale_rect((extension_x, y + 18, 255, extension_height), surface.get_size()).move(0, -content_offset)
                pygame.draw.line(surface, constants.CODE_PURPLE,
                                 (module_rect.right, extension_rect.centery),
                                 (extension_rect.left, extension_rect.centery), 2)
                self.extension_box(surface, extension_rect, extension_lines)
            if module["missingExtensions"]:
                required_height = max(56, 38 + len(module["missingExtensions"]) * 22)
                required_y = y + 18 + (extension_height + 8 if extension_lines else 0)
                required_rect = scale_rect((extension_x, required_y, 255, required_height), surface.get_size()).move(0, -content_offset)
                pygame.draw.line(surface, constants.CODE_ERROR,
                                 (module_rect.right, required_rect.centery),
                                 (required_rect.left, required_rect.centery), 2)
                self.required_extension_box(surface, required_rect, module["missingExtensions"])
                extension_height += required_height + (8 if extension_lines else 0)
            has_extension_area = bool(module["extensions"] or module["missingExtensions"])
            y += max(module_height, extension_height if has_extension_area else 0) + 25

        drop_top = max(590, y + 25)
        drop_unscrolled = scale_rect((350, drop_top, 640, 40), surface.get_size())
        content_bottom = drop_unscrolled.bottom + 70
        self.content_heights["workspace"] = max(workspace.height, content_bottom - workspace.y)
        self.clamp_scroll("workspace", workspace)
        drop = drop_unscrolled.move(0, -content_offset)
        pygame.draw.rect(surface, constants.CODE_ITEM_COLOR, drop, border_radius=7)
        pygame.draw.rect(surface, constants.CODE_MUTED, drop, width=1, border_radius=7)
        surface.blit(self.render("INTERACTIVE EDITING: NOT ENABLED", self.small_font, constants.CODE_MUTED),
                     (drop.x + 20, drop.y + 12))
        self.end_panel_content(surface, workspace, old_clip)

    def draw_module_menu(self, surface, workspace):
        if not self.selected_module_id:
            self.module_menu_rect = None
            self.module_action_rects = {}
            self.extension_removal_rects = {}
            return
        module = next((item for item in self.runtime["modules"]
                       if item["instanceId"] == self.selected_module_id), None)
        if module is None:
            self.selected_module_id = None
            self.module_menu_rect = None
            self.module_action_rects = {}
            self.extension_removal_rects = {}
            return

        attached_extensions = module["extensions"]
        compatible_extensions = self.compatible_extension_ids(module)
        menu_height = 252
        if self.extension_removal_mode:
            menu_height += len(attached_extensions) * 29
        if self.extension_add_mode:
            menu_height += len(compatible_extensions) * 29
        menu = pygame.Rect(workspace.right - 272, workspace.y + 92, 252, menu_height)
        self.module_menu_rect = menu
        layer = pygame.Surface(menu.size, pygame.SRCALPHA)
        layer.fill((8, 22, 32, 250))
        surface.blit(layer, menu.topleft)
        border = constants.CODE_ERROR if module["state"] == "blocked" else constants.CODE_TEAL
        pygame.draw.rect(surface, border, menu, width=2, border_radius=8)
        surface.blit(self.render("MODULE CONTROLS", self.small_font, constants.TEXT_COLOR),
                     (menu.x + 16, menu.y + 14))
        self.draw_wrapped(surface, f"{module['name']} // {module['instanceId']}",
                          self.tiny_font, constants.CODE_MUTED,
                          pygame.Rect(menu.x + 16, menu.y + 38, menu.width - 32, 26))
        surface.blit(self.render("VISUAL PREVIEW", self.tiny_font, constants.CODE_AMBER),
                     (menu.x + 16, menu.y + 66))
        surface.blit(self.render(f"COMPUTE: {module['allocation']} CU", self.tiny_font, constants.CODE_BLUE),
                     (menu.x + 128, menu.y + 66))

        actions = [
            "REMOVE MODULE",
            "ADD EXTENSION",
            "REMOVE EXTENSION",
            "INCREASE COMPUTE",
            "DECREASE COMPUTE",
        ]
        self.module_action_rects = {}
        self.extension_removal_rects = {}
        self.extension_add_rects = {}
        for index, action in enumerate(actions):
            row = pygame.Rect(menu.x + 16, menu.y + 88 + index * 29, menu.width - 32, 23)
            self.module_action_rects[action] = row
            action_color = constants.CODE_MUTED
            if action == "INCREASE COMPUTE" and module_compute_error(
                    self.player, self.module_catalog, module["instanceId"], 1):
                action_color = constants.CODE_ERROR
            pygame.draw.rect(surface, constants.CODE_ITEM_COLOR, row, border_radius=4)
            pygame.draw.rect(surface, action_color, row, width=1, border_radius=4)
            surface.blit(self.render(action, self.tiny_font, action_color),
                         (row.x + 9, row.y + 5))

        if self.extension_removal_mode:
            heading_y = menu.y + 237
            surface.blit(self.render("SELECT EXTENSION TO REMOVE", self.tiny_font, constants.CODE_AMBER),
                         (menu.x + 16, heading_y))
            if not attached_extensions:
                surface.blit(self.render("NO ATTACHED EXTENSIONS", self.tiny_font, constants.CODE_MUTED),
                             (menu.x + 16, heading_y + 22))
            for index, extension_id in enumerate(attached_extensions):
                definition = self.module_catalog.get("extensions", {}).get(extension_id, {})
                row = pygame.Rect(menu.x + 16, heading_y + 22 + index * 29,
                                  menu.width - 32, 23)
                self.extension_removal_rects[extension_id] = row
                pygame.draw.rect(surface, constants.CODE_ITEM_COLOR, row, border_radius=4)
                pygame.draw.rect(surface, constants.CODE_PURPLE, row, width=1, border_radius=4)
                surface.blit(self.render(definition.get("name", extension_id), self.tiny_font,
                                         constants.CODE_PURPLE), (row.x + 9, row.y + 5))
        if self.extension_add_mode:
            heading_y = menu.y + 237
            surface.blit(self.render("SELECT EXTENSION TO ADD", self.tiny_font, constants.CODE_AMBER),
                         (menu.x + 16, heading_y))
            if not compatible_extensions:
                surface.blit(self.render("NO COMPATIBLE EXTENSIONS", self.tiny_font, constants.CODE_MUTED),
                             (menu.x + 16, heading_y + 22))
            for index, extension_id in enumerate(compatible_extensions):
                definition = self.module_catalog.get("extensions", {}).get(extension_id, {})
                row = pygame.Rect(menu.x + 16, heading_y + 22 + index * 29,
                                  menu.width - 32, 23)
                self.extension_add_rects[extension_id] = row
                error = extension_add_error(self.player, self.module_catalog,
                                            self.cached_modules, module["instanceId"], extension_id)
                row_color = constants.CODE_ERROR if error else constants.CODE_PURPLE
                pygame.draw.rect(surface, constants.CODE_ITEM_COLOR, row, border_radius=4)
                pygame.draw.rect(surface, row_color, row, width=1, border_radius=4)
                surface.blit(self.render(definition.get("name", extension_id), self.tiny_font,
                                         row_color), (row.x + 9, row.y + 5))

    def remove_selected_module(self):
        """Remove the selected module, then refresh derived display state."""
        if not self.selected_module_id:
            return
        if remove_module_instance(self.player, self.selected_module_id):
            update_player_data(self.player)
            self.runtime = build_program_runtime(
                self.player,
                self.module_catalog,
                cached_modules=self.cached_modules,
            )
            self.selected_module_id = None
            self.extension_removal_mode = False
            self.module_menu_rect = None
            self.module_action_rects = {}

    def remove_selected_extension(self, extension_id):
        """Remove one selected module extension, then refresh derived state."""
        if not self.selected_module_id:
            return
        if remove_extension_from_instance(self.player, self.selected_module_id, extension_id):
            update_player_data(self.player)
            self.runtime = build_program_runtime(
                self.player,
                self.module_catalog,
                cached_modules=self.cached_modules,
            )
            self.extension_removal_mode = False
            self.module_menu_rect = None
            self.module_action_rects = {}
            self.extension_removal_rects = {}

    def adjust_selected_compute(self, direction):
        """Change the selected module to its next compute tier."""
        if not self.selected_module_id:
            return
        if adjust_module_compute(self.player, self.module_catalog,
                                 self.selected_module_id, direction):
            update_player_data(self.player)
            self.runtime = build_program_runtime(
                self.player,
                self.module_catalog,
                cached_modules=self.cached_modules,
            )

    def module_card(self, surface, rect, module):
        pygame.draw.rect(surface, constants.CODE_ITEM_COLOR, rect, border_radius=8)
        inactive = module["state"] == "blocked"
        color = constants.CODE_ERROR if inactive else constants.CODE_TEAL
        pygame.draw.rect(surface, color, rect, width=2, border_radius=8)
        pygame.draw.rect(surface, constants.CODE_HEADER, (rect.x, rect.y, rect.width, 28), border_radius=8)
        surface.blit(self.render(module["name"].upper(), self.tiny_font, constants.TEXT_COLOR),
                     (rect.x + 18, rect.y + 8))
        state = self.render("INACTIVE" if inactive else module["state"].upper(), self.tiny_font, color)
        surface.blit(state, (rect.right - state.get_width() - 14, rect.y + 8))
        description = self.module_catalog.get("modules", {}).get(module["definitionId"], {}).get(
            "description", "No description available")
        description = f"{module['instanceId']}: {description}"
        description_rect = pygame.Rect(rect.x + 18, rect.y + 43, rect.width - 36, rect.height - 70)
        self.draw_wrapped(surface, description, self.tiny_font, constants.CODE_MUTED, description_rect)
        detail = f"{module['frequency']}  {module['computeCost']} CU  {module['memoryCost']} MB"
        surface.blit(self.render(detail, self.tiny_font, constants.CODE_BLUE),
                     (rect.x + 18, rect.bottom - 18))

    def extension_box(self, surface, rect, extension_lines):
        pygame.draw.rect(surface, constants.CODE_ITEM_COLOR, rect, border_radius=8)
        pygame.draw.rect(surface, constants.CODE_PURPLE, rect, width=2, border_radius=8)
        pygame.draw.circle(surface, constants.CODE_PURPLE, (rect.left, rect.centery), 7)
        y = rect.y + 8
        for extension_id, lines, extension_cost in extension_lines:
            definition = self.module_catalog.get("extensions", {}).get(extension_id, {})
            self.draw_wrapped(surface, "  " + " ".join(lines), self.tiny_font,
                              constants.CODE_PURPLE,
                              pygame.Rect(rect.x + 15, y, rect.width - 30, rect.height - 18),
                              max_lines=len(lines))
            cost = self.render(f"COMPUTE  {extension_cost} CU",
                               self.tiny_font, constants.CODE_MUTED)
            surface.blit(cost, (rect.right - cost.get_width() - 14, y))
            y += max(1, len(lines)) * self.tiny_font.get_height() + 4

    def required_extension_box(self, surface, rect, missing_types):
        pygame.draw.rect(surface, constants.CODE_ITEM_COLOR, rect, border_radius=8)
        pygame.draw.rect(surface, constants.CODE_ERROR, rect, width=2, border_radius=8)
        pygame.draw.circle(surface, constants.CODE_ERROR, (rect.left, rect.centery), 7)
        surface.blit(self.render("REQUIRED", self.tiny_font, constants.CODE_ERROR),
                     (rect.x + 15, rect.y + 7))
        y = rect.y + 25
        for missing_type in missing_types:
            label = missing_type.replace("Type", " Type").replace("type", " type").upper()
            self.draw_wrapped(surface, label, self.tiny_font, constants.CODE_ERROR,
                              pygame.Rect(rect.x + 15, y, rect.width - 30, 18), max_lines=1)
            y += 20

    def draw_state(self, surface, rect, scroll=0):
        self.panel(surface, rect)
        x = rect.x + 20
        surface.blit(self.render("ACTIVE ABILITIES", self.font, constants.TEXT_COLOR),
                     (x, rect.y + 25))
        surface.blit(self.render("derived runtime usage", self.tiny_font, constants.CODE_MUTED),
                     (x, rect.y + 53))
        old_clip = self.begin_panel_content(surface, rect, top_padding=78, bottom_padding=112)
        content_offset = self.scroll_offsets["state"]
        y = rect.y + 100 - content_offset
        for module in self.runtime["modules"]:
            inactive = module["state"] == "blocked"
            self.state_row(surface, x, y, module["name"],
                           "INACTIVE" if inactive else f"{module['computeCost']} CU",
                           constants.CODE_ERROR if inactive else constants.CODE_TEAL,
                           rect.right - 20)
            y += 28
            self.state_row(surface, x + 16, y, "BASE MODULE",
                           f"{module['allocation']} CU", constants.CODE_BLUE, rect.right - 20)
            y += 25
            for extension_id in module["extensions"]:
                definition = self.module_catalog.get("extensions", {}).get(extension_id, {})
                self.extension_state_row(surface, x + 16, y, definition.get("name", extension_id),
                                         f"{module.get('extensionCosts', {}).get(extension_id, definition.get('computeCost', 0))} CU",
                                         rect.right - 20)
                y += 25
            y += 8
        content_bottom = y + content_offset + 10
        self.content_heights["state"] = max(rect.height, content_bottom + 100 - rect.y)
        self.clamp_scroll("state", rect)
        self.end_panel_content(surface, rect, old_clip)

        summary_y = rect.bottom - 102
        surface.blit(self.render("PROCESSING SUMMARY", self.small_font, constants.CODE_TEAL), (x, summary_y))
        compute = self.runtime["compute"]
        self.draw_resource_bar(surface, pygame.Rect(x, summary_y + 22, rect.width - 40, 30),
                               "COMPUTE", compute["used"], compute["capacity"], constants.CODE_BLUE, "CU")
        self.state_row(surface, x, rect.bottom - 38, "AVAILABLE", f"{compute['available']} CU",
                       constants.CODE_TEAL if compute["available"] >= 0 else constants.CODE_AMBER,
                       rect.right - 20)

    def draw_resource_bar(self, surface, rect, label, used, capacity, color, unit):
        over_capacity = used > capacity
        display_color = constants.CODE_ERROR if over_capacity else color
        pygame.draw.rect(surface, constants.CODE_ITEM_COLOR, rect, border_radius=5)
        ratio = min(1, max(0, used / capacity)) if capacity else 0
        fill = pygame.Rect(rect.x, rect.y, round(rect.width * ratio), rect.height)
        if fill.width > 0:
            pygame.draw.rect(surface, display_color, fill, border_radius=5)
        pygame.draw.rect(surface, display_color, rect, width=1, border_radius=5)
        text_label = f"{label} ERROR  {used} / {capacity} {unit}" if over_capacity else \
            f"{label} USED  {used} / {capacity} {unit}"
        text = self.render(text_label, self.tiny_font,
                           constants.TEXT_COLOR)
        surface.blit(text, (rect.x + 10, rect.y + (rect.height - text.get_height()) // 2))

    def extension_state_row(self, surface, x, y, label, value, right=None):
        pygame.draw.line(surface, constants.CODE_PURPLE, (x, y + 7), (x, y + 16), 2)
        pygame.draw.line(surface, constants.CODE_PURPLE, (x, y + 16), (x + 10, y + 16), 2)
        self.state_row(surface, x + 16, y, label, value, constants.CODE_PURPLE, right)

    def state_row(self, surface, x, y, label, value, color, right=None):
        value_surface = self.render(value, self.tiny_font, color)
        value_right = right if right is not None else x + 218
        value_x = value_right - value_surface.get_width()
        surface.blit(value_surface, (value_x, y))
        self.draw_wrapped(surface, label, self.tiny_font, constants.CODE_MUTED,
                          pygame.Rect(x, y, max(1, value_x - x - 8), self.tiny_font.get_height()),
                          max_lines=1)
