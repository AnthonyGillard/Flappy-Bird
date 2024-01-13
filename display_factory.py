import pygame


class DisplayFactory:
    BACKGROUND_FILE_PATH = "C:\\Users\\erind\\PycharmProjects\\flappyBird\\images\\background.png"
    LOGO_FILE_PATH = "C:\\Users\\erind\\PycharmProjects\\flappyBird\\images\\Logo.jpg"
    FONT = 'timesnewroman'
    FONT_SIZE = 28
    SURFACE_WIDTH = 400
    SURFACE_HEIGHT = 600

    def __init__(self):
        self.background = pygame.image.load(self.BACKGROUND_FILE_PATH)
        self.background = pygame.transform.scale(self.background, (self.SURFACE_WIDTH, self.SURFACE_HEIGHT))

        self._create_application_surface()

    def _create_application_surface(self):
        self.surface = pygame.display.set_mode((self.SURFACE_WIDTH, self.SURFACE_HEIGHT))

        pygame.display.set_caption('Flappy Bird')
        pygame.display.set_icon(pygame.image.load(self.LOGO_FILE_PATH))

    def create_start_menu(self, grounds, start_graphic):
        self.surface.blit(self.background, (0, 0))

        for ground in grounds:
            ground.draw(self.surface)

        start_graphic.draw(self.surface)

