import pygame
from equations import calculate_derivative_multi_by_time


class Ground:
    FILE_PATH = "C:\\Users\\erind\\PycharmProjects\\flappyBird\\images\\ground.png"
    U = 70

    def __init__(self, window_width, window_height, ground_height, start_out_of_window):
        self.width = window_width * 1.05
        self.height = ground_height

        self.image = self._get_ground_image()

        self.hit_box = self.image.get_rect()
        self.hit_box.y = window_height - self.height
        self._move_to_lateral_start_position(start_out_of_window=start_out_of_window)

    def _get_ground_image(self):
        ground = pygame.image.load(self.FILE_PATH)
        return pygame.transform.scale(ground, (self.width, self.height))

    def _move_to_lateral_start_position(self, start_out_of_window=1):
        self.hit_box.x = self.width * start_out_of_window

    def move(self, time_ms):
        self.hit_box.x -= calculate_derivative_multi_by_time(self.U, (time_ms / 1000))
        if self.hit_box.x <= -self.width:
            self._move_to_lateral_start_position()

    def draw(self, surface):
        surface.blit(self.image, self.hit_box)
