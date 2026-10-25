"""Application entry point for The Digital Sea."""

import pygame

import constants
from data_loader import load_json
from network_screen import NetworkScreen
from screen_manager import ScreenManager


def main():
    pygame.init()
    pygame.display.set_caption(constants.WINDOW_TITLE)
    screen = pygame.display.set_mode(constants.WINDOW_SIZE, pygame.RESIZABLE)
    clock = pygame.time.Clock()
    state = {
        "player": load_json("player.json"),
        "network_cache": load_json("network_cache.json"),
    }
    screens = {
        "network": NetworkScreen(state),
    }
    screen_manager = ScreenManager(screens, "network")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                screen_manager.handle_event(event)
        screen_manager.draw(screen)
        pygame.display.flip()
        clock.tick(constants.FRAME_RATE)

    pygame.quit()


if __name__ == "__main__":
    main()
