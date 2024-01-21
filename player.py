from equations import calculate_derivative_multi_by_time
from image_processing import ImageProcessing


class Player:
    FILE_PATH_IMAGE_UP = "\\Images\\bird_up.png"
    FILE_PATH_IMAGE_MID = "\\Images\\bird_mid.png"
    FILE_PATH_IMAGE_DOWN = "\\Images\\bird_down.png"

    WIDTH, HEIGHT = 20, 20
    ACCELERATION = 500
    v = 0

    image_processing = ImageProcessing()

    def __init__(self, cwd, window_width):
        self.window_width = window_width

        self._load_bird_images(cwd)
        self.hit_box = self.bird_mid_image.get_rect()

        self.reset()

    def _load_bird_images(self, cwd):
        self.bird_up_image = self.image_processing.load_and_scale_image(
            cwd + self.FILE_PATH_IMAGE_UP, self.WIDTH, self.HEIGHT)
        self.bird_mid_image = self.image_processing.load_and_scale_image(
            cwd + self.FILE_PATH_IMAGE_MID, self.WIDTH, self.HEIGHT)
        self.bird_down_image = self.image_processing.load_and_scale_image(
            cwd + self.FILE_PATH_IMAGE_DOWN, self.WIDTH, self.HEIGHT)

    def jump(self):
        self.v = -200

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
        self.hit_box.x = (self.window_width / 2) - (self.WIDTH / 2)
        self.hit_box.y = 0
        self.v = 0
