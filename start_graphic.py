from image_processing import ImageProcessing


class StartGraphic:
    FILE_PATH = "\\images\\start.png"
    WIDTH = 176
    HEIGHT = 77

    image_processor = ImageProcessing()

    def __init__(self, cwd, surface_width, y_position):
        self.image = self.image_processor.load_and_scale_image(cwd + self.FILE_PATH, self.WIDTH, self.HEIGHT)

        x_position = (surface_width / 2) - (self.WIDTH / 2)
        self.position = (x_position, y_position)

    def draw(self, surface):
        surface.blit(self.image, self.position)
