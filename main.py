import os
import pygame
from game_manager import GameManager

FPS = 30

pygame.init()

game_manager = GameManager(os.getcwd())

clock = pygame.time.Clock()

running = True
while running:
    clock.tick(FPS)

    running = game_manager.manage_events(pygame.event.get())
    game_manager.increment_game_through_time(clock.get_time())

    pygame.display.update()
