"""Read-only Code screen driven by the loaded player and module data."""

from __future__ import annotations

import pygame

import constants
from code_layout import screen_rects, telemetry_rects, scale_rect
from drawing import draw_background
from program_runtime import build_program_runtime
from screen import Screen


class CodeScreen(Screen):
    """Display the active program and derived runtime state without editing it."""

    def __init__(self, state: dict):
        self.player = state["player"]
        self.module_catalog = state.get("module_catalog", {})
        self.cached_modules = state.get("cached_modules", {})
        self.runtime = build_program_runtime(self.player, self.module_catalog)
        self.font = pygame.font.Font(None, 25)
        self.small_font = pygame.font.Font(None, 18)
        self.tiny_font = pygame.font.Font(None, 15)

    def handle_event(self, event):
        return None

    def draw(self, surface):
        draw_background(surface)
        rects = screen_rects(surface.get_size())
        self.draw_telemetry(surface)
        self.draw_library(surface, rects["library"])
        self.draw_workspace(surface, rects["workspace"])
        self.draw_state(surface, rects["state"])
        footer = self.render("READ-ONLY PREVIEW // PLAYER DATA", self.tiny_font,
                             constants.MUTED_TEXT_COLOR)
        surface.blit(footer, (18, surface.get_height() - footer.get_height() - 18))

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
            ("PLAYER", self.player.get("playerId", "unknown"), constants.CODE_TEAL),
            ("COMPUTE", f"{compute['used']} / {compute['capacity']} CU", constants.CODE_BLUE),
            ("MEMORY", f"{memory['used']} / {memory['capacity']} MB", constants.CODE_PURPLE),
        ]
        for rect, (label, value, color) in zip(telemetry_rects(surface.get_size()), labels):
            self.panel(surface, rect)
            surface.blit(self.render(label, self.tiny_font, constants.CODE_MUTED),
                         (rect.x + 16, rect.y + 18))
            surface.blit(self.render(value, self.font, constants.TEXT_COLOR),
                         (rect.x + 16, rect.y + 45))
            capacity = compute["capacity"] if label == "COMPUTE" else memory["capacity"]
            used = compute["used"] if label == "COMPUTE" else memory["used"]
            ratio = min(1, used / capacity) if capacity else 0
            bar = pygame.Rect(rect.x + 16, rect.bottom - 17, rect.width - 32, 5)
            pygame.draw.rect(surface, constants.CODE_ITEM_COLOR, bar, border_radius=2)
            pygame.draw.rect(surface, color,
                             pygame.Rect(bar.x, bar.y, max(20, round(bar.width * ratio)), bar.height),
                             border_radius=2)

    def draw_library(self, surface, rect):
        entries = self.library_entries()
        group_counts = [sum(entry["status"] == status for entry in entries)
                        for status in ("IN USE", "READY", "NOT ENOUGH COMPUTE")]
        required_height = 90 + sum(36 + count * 40 for count in group_counts) + 65
        panel_rect = rect.copy()
        panel_rect.height = max(rect.height, required_height)
        self.panel(surface, panel_rect)
        x = panel_rect.x + 18
        surface.blit(self.render("CODE LIBRARY", self.font, constants.TEXT_COLOR), (x, panel_rect.y + 25))
        surface.blit(self.render("current availability", self.tiny_font, constants.CODE_MUTED),
                     (x, panel_rect.y + 53))
        groups = [
            ("IN USE", constants.CODE_TEAL),
            ("READY", constants.CODE_BLUE),
            ("NOT ENOUGH COMPUTE", constants.CODE_AMBER),
        ]
        offset = 90
        for title, color in groups:
            group = [entry for entry in entries if entry["status"] == title]
            self.library_section(surface, x, panel_rect.y + offset, title, color)
            offset += 24
            for entry in group:
                self.library_item(surface, panel_rect, offset, entry["name"], entry["cost"], color)
                offset += 40
            offset += 12

        memory = self.runtime["memory"]
        self.draw_resource_bar(surface, pygame.Rect(panel_rect.x + 18, panel_rect.bottom - 53, panel_rect.width - 36, 28),
                               "MEMORY", memory["used"], memory["capacity"], constants.CODE_PURPLE, "MB")

    def library_entries(self):
        available_compute = self.runtime["compute"]["available"]
        active_modules = {module["id"] for module in self.runtime["modules"]}
        active_extensions = set(self.runtime["extensions"])
        entries = []
        for module_id in self.cached_modules.get("modules", []):
            definition = self.module_catalog.get("modules", {}).get(module_id, {})
            cost = int(definition.get("mediumCompute", definition.get("lowCompute", 0)))
            status = "IN USE" if module_id in active_modules else (
                "READY" if cost <= available_compute else "NOT ENOUGH COMPUTE")
            entries.append({"name": definition.get("name", module_id), "cost": f"{cost} CU", "status": status})
        for extension_id in self.cached_modules.get("extensions", []):
            definition = self.module_catalog.get("extensions", {}).get(extension_id, {})
            cost = int(definition.get("computeCost", 0))
            status = "IN USE" if extension_id in active_extensions else (
                "READY" if cost <= available_compute else "NOT ENOUGH COMPUTE")
            entries.append({"name": definition.get("name", extension_id), "cost": f"{cost} CU", "status": status})
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

    def draw_workspace(self, surface, workspace):
        self.panel(surface, workspace)
        surface.blit(self.render("MAIN PROGRAM", self.font, constants.TEXT_COLOR),
                     (workspace.x + 20, workspace.y + 25))
        surface.blit(self.render("read-only configuration preview", self.tiny_font, constants.CODE_MUTED),
                     (workspace.x + 20, workspace.y + 54))
        header = scale_rect((350, 236, 750, 48), surface.get_size())
        pygame.draw.rect(surface, constants.CODE_HEADER, header, border_radius=8)
        pygame.draw.rect(surface, constants.CODE_TEAL, header, width=1, border_radius=8)
        player_id = self.player.get("playerId", "unknown")
        surface.blit(self.render(f"PROGRAM INSTANCE // {player_id}", self.small_font),
                     (header.x + 22, header.y + 15))

        y = 305
        for module in self.runtime["modules"]:
            definition = self.module_catalog.get("modules", {}).get(module["id"], {})
            description_lines = self.wrapped_lines(
                definition.get("description", "No description available"),
                self.tiny_font, 324
            )
            module_height = max(92, 75 + len(description_lines) * self.tiny_font.get_height())
            module_rect = scale_rect((350, y, 360, module_height), surface.get_size())
            self.module_card(surface, module_rect, module)
            extension_x = 735
            for extension_id in module["extensions"]:
                extension_name = self.module_catalog.get("extensions", {}).get(extension_id, {}).get(
                    "name", extension_id)
                extension_lines = self.wrapped_lines(extension_name.upper(), self.tiny_font, 225)
                extension_height = max(56, 24 + len(extension_lines) * self.tiny_font.get_height() + 18)
                extension_rect = scale_rect((extension_x, y + 18, 255, extension_height), surface.get_size())
                pygame.draw.line(surface, constants.CODE_PURPLE,
                                 (module_rect.right, extension_rect.centery),
                                 (extension_rect.left, extension_rect.centery), 2)
                self.extension_piece(surface, extension_rect, extension_id)
                extension_x += 270
            y += max(module_height, extension_height if module["extensions"] else 0) + 25

        drop = scale_rect((350, 590, 640, 40), surface.get_size())
        pygame.draw.rect(surface, constants.CODE_ITEM_COLOR, drop, border_radius=7)
        pygame.draw.rect(surface, constants.CODE_MUTED, drop, width=1, border_radius=7)
        surface.blit(self.render("INTERACTIVE EDITING: NOT ENABLED", self.small_font, constants.CODE_MUTED),
                     (drop.x + 20, drop.y + 12))

    def module_card(self, surface, rect, module):
        pygame.draw.rect(surface, constants.CODE_ITEM_COLOR, rect, border_radius=8)
        color = constants.CODE_AMBER if module["state"] == "blocked" else constants.CODE_TEAL
        pygame.draw.rect(surface, color, rect, width=2, border_radius=8)
        pygame.draw.rect(surface, constants.CODE_HEADER, (rect.x, rect.y, rect.width, 28), border_radius=8)
        surface.blit(self.render(module["name"].upper(), self.tiny_font, constants.TEXT_COLOR),
                     (rect.x + 18, rect.y + 8))
        state = self.render(module["state"].upper(), self.tiny_font, color)
        surface.blit(state, (rect.right - state.get_width() - 14, rect.y + 8))
        description = self.module_catalog.get("modules", {}).get(module["id"], {}).get(
            "description", "No description available")
        description_rect = pygame.Rect(rect.x + 18, rect.y + 43, rect.width - 36, rect.height - 70)
        self.draw_wrapped(surface, description, self.tiny_font, constants.CODE_MUTED, description_rect)
        detail = f"{module['frequency']}  {module['computeCost']} CU  {module['memoryCost']} MB"
        surface.blit(self.render(detail, self.tiny_font, constants.CODE_BLUE),
                     (rect.x + 18, rect.bottom - 18))

    def extension_piece(self, surface, rect, extension_id):
        definition = self.module_catalog.get("extensions", {}).get(extension_id, {})
        pygame.draw.rect(surface, constants.CODE_ITEM_COLOR, rect, border_radius=8)
        pygame.draw.rect(surface, constants.CODE_PURPLE, rect, width=2, border_radius=8)
        pygame.draw.circle(surface, constants.CODE_PURPLE, (rect.left, rect.centery), 7)
        self.draw_wrapped(surface, definition.get("name", extension_id).upper(), self.tiny_font,
                          constants.CODE_PURPLE,
                          pygame.Rect(rect.x + 15, rect.y + 7, rect.width - 30, rect.height - 25))
        surface.blit(self.render(f"COMPUTE  {definition.get('computeCost', 0)} CU",
                                 self.tiny_font, constants.CODE_MUTED), (rect.x + 15, rect.bottom - 18))

    def draw_state(self, surface, rect):
        self.panel(surface, rect)
        x = rect.x + 20
        surface.blit(self.render("ACTIVE ABILITIES", self.font, constants.TEXT_COLOR), (x, rect.y + 25))
        surface.blit(self.render("derived runtime usage", self.tiny_font, constants.CODE_MUTED),
                     (x, rect.y + 53))
        y = rect.y + 100
        for module in self.runtime["modules"]:
            self.state_row(surface, x, y, module["name"], f"{module['computeCost']} CU", constants.CODE_TEAL)
            y += 28
            for extension_id in module["extensions"]:
                definition = self.module_catalog.get("extensions", {}).get(extension_id, {})
                self.extension_state_row(surface, x + 16, y, definition.get("name", extension_id),
                                         f"{definition.get('computeCost', 0)} CU")
                y += 25
            y += 8
        summary_y = rect.bottom - 112
        surface.blit(self.render("PROCESSING SUMMARY", self.small_font, constants.CODE_TEAL), (x, summary_y))
        compute = self.runtime["compute"]
        self.draw_resource_bar(surface, pygame.Rect(x, rect.bottom - 78, rect.width - 40, 30),
                               "COMPUTE", compute["used"], compute["capacity"], constants.CODE_BLUE, "CU")
        self.state_row(surface, x, rect.bottom - 40, "AVAILABLE", f"{compute['available']} CU",
                       constants.CODE_TEAL if compute["available"] >= 0 else constants.CODE_AMBER)

    def draw_resource_bar(self, surface, rect, label, used, capacity, color, unit):
        pygame.draw.rect(surface, constants.CODE_ITEM_COLOR, rect, border_radius=5)
        ratio = min(1, max(0, used / capacity)) if capacity else 0
        fill = pygame.Rect(rect.x, rect.y, round(rect.width * ratio), rect.height)
        if fill.width > 0:
            pygame.draw.rect(surface, color, fill, border_radius=5)
        pygame.draw.rect(surface, color, rect, width=1, border_radius=5)
        text = self.render(f"{label} USED  {used} / {capacity} {unit}", self.tiny_font,
                           constants.TEXT_COLOR)
        surface.blit(text, (rect.x + 10, rect.y + (rect.height - text.get_height()) // 2))

    def extension_state_row(self, surface, x, y, label, value):
        pygame.draw.line(surface, constants.CODE_PURPLE, (x, y + 7), (x, y + 16), 2)
        pygame.draw.line(surface, constants.CODE_PURPLE, (x, y + 16), (x + 10, y + 16), 2)
        self.state_row(surface, x + 16, y, label, value, constants.CODE_PURPLE)

    def state_row(self, surface, x, y, label, value, color):
        surface.blit(self.render(label, self.tiny_font, constants.CODE_MUTED), (x, y))
        value_surface = self.render(value, self.tiny_font, color)
        surface.blit(value_surface, (x + 218 - value_surface.get_width(), y))
