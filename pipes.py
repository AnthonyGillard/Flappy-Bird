import pygame
import math
import random
from equations import calculate_derivative_multi_by_time

random.seed(1)


class Pipes:
    FILE_PATH_UPPER_PIPE = "C:\\Users\\erind\\PycharmProjects\\flappyBird\\Images\\pipe_top.png"
    FILE_PATH_LOWER_PIPE = "C:\\Users\\erind\\PycharmProjects\\flappyBird\\Images\\pipe_bottom.png"

    WIDTH = 52
    HEIGHT = 800
    U = 70

    GAP_BETWEEN_PIPES = 100

    def __init__(self, height_available_for_pipes, surface_width, factor_outside_window):
        self.surface_width = surface_width
        self.height_available_for_pipes = height_available_for_pipes

        self.min_pipe_displacement = math.floor(0.2 * self.height_available_for_pipes)
        self.available_range_for_centre = self.height_available_for_pipes - self.GAP_BETWEEN_PIPES - (
                    2 * self.min_pipe_displacement)

        self.pipes = list()
        self.pipes.append(self._load_and_scale_image(self.FILE_PATH_UPPER_PIPE))
        self.pipes.append(self._load_and_scale_image(self.FILE_PATH_LOWER_PIPE))

        self.hit_boxes = list()
        for pipe in self.pipes:
            self.hit_boxes.append(pipe.get_rect())

        self.reset(factor_outside_window, 0)

    def _load_and_scale_image(self, file_path):
        image = pygame.image.load(file_path)
        return pygame.transform.scale(image, (self.WIDTH, self.HEIGHT))

    def move(self, time_ms):
        for hit_box in self.hit_boxes:
            hit_box.x -= calculate_derivative_multi_by_time(self.U, (time_ms / 1000))
            if hit_box.x <= -self.WIDTH:
                self.reset()

    def draw(self, surface):
        for index, pipe in enumerate(self.pipes):
            surface.blit(pipe, self.hit_boxes[index])

    def reset(self, factor_outside_window=1.5, add_width=1):
        pipe_centre = self._get_random_pipe_centre()

        self.hit_boxes[0].y = -self.HEIGHT + (pipe_centre - (self.GAP_BETWEEN_PIPES / 2))
        self.hit_boxes[1].y = pipe_centre + (self.GAP_BETWEEN_PIPES / 2)

        self.hit_boxes[0].x = (self.surface_width * factor_outside_window) - (self.WIDTH * add_width)
        self.hit_boxes[1].x = (self.surface_width * factor_outside_window) - (self.WIDTH * add_width)

    def _get_random_pipe_centre(self):
        return self.min_pipe_displacement + (self.GAP_BETWEEN_PIPES / 2) + \
            math.floor(self.available_range_for_centre * random.random())
