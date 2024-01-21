import unittest
from unittest.mock import Mock, patch
from start_graphic import StartGraphic


class TestStartGraphic(unittest.TestCase):
    @patch('pipes.ImageProcessing.load_and_scale_image', return_value='image')
    def get_start_graphic_and_building_mocks(self, x_position, y_position, mocked_ip):
        return StartGraphic('file_path', x_position, y_position), mocked_ip

    def test_init_loads_image(self):
        start_graphic, mocked_ip = self.get_start_graphic_and_building_mocks(10, 20)

        mocked_ip.assert_called_once_with(
            'file_path' + start_graphic.FILE_PATH, start_graphic.WIDTH, start_graphic.HEIGHT)

    def test_init_populates_position_as_expected(self):
        width = 400
        height = 20

        start_graphic, _ = self.get_start_graphic_and_building_mocks(width, height)

        self.assertTupleEqual((112, height), start_graphic.position)

    def test_draw_calls_blit_function_as_expected(self):
        width = 10
        height = 20
        surface = Mock()
        surface.blit = Mock()
        start_graphic, _ = self.get_start_graphic_and_building_mocks(width, height)
        start_graphic.image = 'image'

        start_graphic.draw(surface)

        surface.blit.assert_called_once_with('image', start_graphic.position)

