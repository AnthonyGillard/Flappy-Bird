import pygame
import math
import random
from equations import calculate_derivative_multi_by_time
from image_processing import ImageProcessing

random.seed(1)


class Pipes:
    FILE_PATH_UPPER_PIPE = "\\Images\\pipe_top.png"
    FILE_PATH_LOWER_PIPE = "\\Images\\pipe_bottom.png"
    image_processor = ImageProcessing()

    WIDTH = 52
    HEIGHT = 800
    U = 70

    GAP_BETWEEN_PIPES = 100

    def __init__(self, cwd, height_available_for_pipes, surface_width, factor_outside_window):
        self.surface_width = surface_width
        self.height_available_for_pipes = height_available_for_pipes

        self._calculate_pipe_limitations()
        self._load_pipe_images(cwd)
        self._create_pipe_hit_boxes()
        self.reset(factor_outside_window, 0)

        self.previous_x = self.hit_boxes[0].x

    def _load_pipe_images(self, cwd):
        self.pipes = list()
        self.pipes.append(self.image_processor.load_and_scale_image(cwd + self.FILE_PATH_UPPER_PIPE,
                                                                    self.WIDTH, self.HEIGHT))
        self.pipes.append(self.image_processor.load_and_scale_image(cwd + self.FILE_PATH_LOWER_PIPE,
                                                                    self.WIDTH, self.HEIGHT))

    def _calculate_pipe_limitations(self):
        self.min_pipe_displacement = math.floor(0.2 * self.height_available_for_pipes)
        self.available_range_for_centre = self.height_available_for_pipes - self.GAP_BETWEEN_PIPES - (
                2 * self.min_pipe_displacement)

    def _create_pipe_hit_boxes(self):
        self.hit_boxes = list()
        for pipe in self.pipes:
            self.hit_boxes.append(pipe.get_rect())

    def move(self, time_ms):
        self.previous_x = self.hit_boxes[0].x
        for hit_box in self.hit_boxes:
            hit_box.x -= calculate_derivative_multi_by_time(self.U, (time_ms / 1000))
            if hit_box.x <= -self.WIDTH:
                self.reset()

    def draw(self, surface):
        for index, pipe in enumerate(self.pipes):
            surface.blit(pipe, self.hit_boxes[index])

    def passed_over_player(self):
        surface_mid_point = (self.surface_width / 2)
        if self.previous_x + self.WIDTH > surface_mid_point >= self.hit_boxes[0].x + self.WIDTH:
            return True
        else:
            return False

    def reset(self, factor_outside_window=1.5, add_width=1):
        pipe_centre = self._get_random_pipe_centre()

        self.hit_boxes[0].y = -self.HEIGHT + (pipe_centre - (self.GAP_BETWEEN_PIPES / 2))
        self.hit_boxes[1].y = pipe_centre + (self.GAP_BETWEEN_PIPES / 2)

        self.hit_boxes[0].x = (self.surface_width * factor_outside_window) - (self.WIDTH * add_width)
        self.hit_boxes[1].x = (self.surface_width * factor_outside_window) - (self.WIDTH * add_width)

    def _get_random_pipe_centre(self):
        return self.min_pipe_displacement + (self.GAP_BETWEEN_PIPES / 2) + \
            math.floor(self.available_range_for_centre * random.random())
