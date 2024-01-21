import unittest
from unittest.mock import Mock, patch, call
from image_processing import ImageProcessing


class TestImageProcessing(unittest.TestCase):
    @patch('pygame.image.load', return_value='image')
    @patch('pygame.transform.scale')
    def test_load_and_scale_image_loads_image_via_pygame(self, mocked_scale, mocked_load):
        image_processing = ImageProcessing()

        image_processing.load_and_scale_image('file_path', 'width', 'height')

        mocked_load.assert_called_once_with('file_path')

    @patch('pygame.image.load', return_value='image')
    @patch('pygame.transform.scale')
    def test_load_and_scale_images_scales_image_via_pygame(self, mocked_scale, mocked_load):
        image_processing = ImageProcessing()

        image_processing.load_and_scale_image('file_path', 'width', 'height')

        mocked_scale.assert_called_once_with('image', ('width', 'height'))
