"""Application-level routing between game screens."""


class ScreenManager:
    def __init__(self, screens: dict, starting_screen: str):
        self.screens = screens
        self.active_screen_name = None
        self.set_screen(starting_screen)

    @property
    def active_screen(self):
        return self.screens[self.active_screen_name]

    def set_screen(self, screen_name: str):
        if screen_name not in self.screens:
            raise KeyError(f"Unknown screen: {screen_name}")
        self.active_screen_name = screen_name
        refresh = getattr(self.active_screen, "refresh", None)
        if callable(refresh):
            refresh()

    def handle_event(self, event):
        requested_screen = self.active_screen.handle_event(event)
        if requested_screen is not None:
            self.set_screen(requested_screen)

    def draw(self, surface):
        self.active_screen.draw(surface)
