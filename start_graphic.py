import pygame


class StartGraphic:
    FILE_PATH = "C:\\Users\\erind\\PycharmProjects\\flappyBird\\images\\start.png"
    WIDTH = 176
    HEIGHT = 77

    def __init__(self, surface_width, y_position):
        self.image = pygame.image.load(self.FILE_PATH)
        self.image = pygame.transform.scale(self.image, (self.WIDTH, self.HEIGHT))

        x_position = (surface_width / 2) - (self.WIDTH / 2)
        self.position = (x_position, y_position)

    def draw(self, surface):
        surface.blit(self.image, self.position)
