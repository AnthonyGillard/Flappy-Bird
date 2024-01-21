import pygame


class ImageProcessing:
    @staticmethod
    def load_and_scale_image(file_path, width, height):
        return pygame.transform.scale(pygame.image.load(file_path), (width, height))
