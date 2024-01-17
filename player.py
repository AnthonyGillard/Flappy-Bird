import pygame
from equations import calculate_derivative_multi_by_time


class Player:
    FILE_PATH_IMAGE_UP = "C:\\Users\\erind\\PycharmProjects\\flappyBird\\Images\\bird_up.png"
    FILE_PATH_IMAGE_MID = "C:\\Users\\erind\\PycharmProjects\\flappyBird\\Images\\bird_mid.png"
    FILE_PATH_IMAGE_DOWN = "C:\\Users\\erind\\PycharmProjects\\flappyBird\\Images\\bird_down.png"

    WIDTH, HEIGHT = 20, 20
    ACCELERATION = 500

    def __init__(self, window_width):
        self.window_width = window_width

        self._load_up_image()
        self._load_mid_image()
        self._load_down_image()

        self.hit_box = self.bird_mid_image.get_rect()
        self.v = 0

        self._reset_player_position_and_velocity()

    def _load_up_image(self):
        self.bird_up_image = pygame.image.load(self.FILE_PATH_IMAGE_UP)
        self.bird_up_image = pygame.transform.scale(self.bird_up_image, (self.WIDTH, self.HEIGHT))

    def _load_mid_image(self):
        self.bird_mid_image = pygame.image.load(self.FILE_PATH_IMAGE_MID)
        self.bird_mid_image = pygame.transform.scale(self.bird_mid_image, (self.WIDTH, self.HEIGHT))

    def _load_down_image(self):
        self.bird_down_image = pygame.image.load(self.FILE_PATH_IMAGE_DOWN)
        self.bird_down_image = pygame.transform.scale(self.bird_down_image, (self.WIDTH, self.HEIGHT))

    def jump(self):
        self.v = -300

    def move(self, time_ms):
        self.v += calculate_derivative_multi_by_time(self.ACCELERATION, (time_ms / 1000))
        self.hit_box.y += calculate_derivative_multi_by_time(self.v, (time_ms / 1000))

    def draw(self, surface):
        if self.v > 0:
            surface.blit(self.bird_up_image, self.hit_box)
        elif self.v == 0:
            surface.blit(self.bird_mid_image, self.hit_box)
        elif self.v < 0:
            surface.blit(self.bird_down_image, self.hit_box)

    def reset(self):
        self._reset_player_position_and_velocity()

    def _reset_player_position_and_velocity(self):
        self.hit_box.x = (self.window_width / 2) - (self.WIDTH / 2)
        self.hit_box.y = 0
        self.v = 0
