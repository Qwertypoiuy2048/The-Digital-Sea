"""Shared contract for all game screens."""


class Screen:
    """Minimal interface used by the application screen manager."""

    def handle_event(self, event):
        raise NotImplementedError

    def draw(self, surface):
        raise NotImplementedError
