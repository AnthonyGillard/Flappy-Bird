import pygame
from image_processing import ImageProcessing


class DisplayFactory:
    BACKGROUND_FILE_PATH = "\\images\\background.png"
    LOGO_FILE_PATH = "\\images\\Logo.jpg"
    FONT = 'FlappyBirdy'
    FONT_SIZE = 28
    SURFACE_WIDTH = 400
    SURFACE_HEIGHT = 600

    image_processor = ImageProcessing()

    def __init__(self, cwd):
        self.background = self.image_processor.load_and_scale_image(
            cwd + self.BACKGROUND_FILE_PATH, self.SURFACE_WIDTH, self.SURFACE_HEIGHT)

        self.font = pygame.font.SysFont(self.FONT,  self.FONT_SIZE)

        self._create_application_surface(cwd)

    def _create_application_surface(self, cwd):
        self.surface = pygame.display.set_mode((self.SURFACE_WIDTH, self.SURFACE_HEIGHT))

        pygame.display.set_caption('Flappy Bird')
        pygame.display.set_icon(pygame.image.load(cwd + self.LOGO_FILE_PATH))

    def _draw_background(self):
        self.surface.blit(self.background, (0, 0))

    def _draw_grounds(self, grounds):
        for ground in grounds:
            ground.draw(self.surface)

    def _draw_text(self, text, y_position):
        score_text = self.font.render(text, 1, (255, 255, 255))
        score_rect = score_text.get_rect()
        score_rect.center = (self.SURFACE_WIDTH / 2, y_position)
        self.surface.blit(score_text, score_rect)

    def create_start_menu(self, grounds, start_graphic):
        self._draw_background()
        self._draw_grounds(grounds)
        start_graphic.draw(self.surface)

    def create_game_running_view(self, grounds, player, pipes, score):
        self._draw_background()

        for pipe in pipes:
            pipe.draw(self.surface)

        self._draw_grounds(grounds)
        player.draw(self.surface)
        self._draw_text(f'{score}', 100)

    def create_game_over(self, grounds, game_over_graphic, score):
        self._draw_background()
        self._draw_grounds(grounds)
        game_over_graphic.draw(self.surface)
        self._draw_text(f'Score: {score}', 250)

