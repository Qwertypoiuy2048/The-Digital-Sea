"""Application-level routing between game screens."""


class ScreenManager:
    def __init__(self, screens: dict, starting_screen: str):
        self.screens = screens
        self.active_screen_name = starting_screen

    @property
    def active_screen(self):
        return self.screens[self.active_screen_name]

    def set_screen(self, screen_name: str):
        if screen_name not in self.screens:
            raise KeyError(f"Unknown screen: {screen_name}")
        self.active_screen_name = screen_name

    def handle_event(self, event):
        self.active_screen.handle_event(event)

    def draw(self, surface):
        self.active_screen.draw(surface)
