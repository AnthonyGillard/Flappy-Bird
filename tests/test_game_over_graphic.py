import unittest
from unittest.mock import Mock, patch
from game_over_graphic import GameOverGraphic


class TestGameOverGraphic(unittest.TestCase):
    @patch('pipes.ImageProcessing.load_and_scale_image', return_value='image')
    def get_start_graphic_and_building_mocks(self, surface_width, y_position, mocked_ip):
        return GameOverGraphic('file_path', surface_width, y_position), mocked_ip

    def test_init_loads_image(self):
        set_up = self.get_start_graphic_and_building_mocks(10, 20)

        set_up[1].assert_called_once_with(
            'file_path' + set_up[0].FILE_PATH, set_up[0].WIDTH, set_up[0].HEIGHT)

    def test_init_populates_position_as_expected(self):
        surface_width = 400
        y_position = 20

        set_up = self.get_start_graphic_and_building_mocks(surface_width, y_position)

        self.assertTupleEqual((104, y_position), set_up[0].position)

    def test_draw_calls_blit_function_as_expected(self):
        surface_width = 10
        y_position = 20
        surface = Mock()
        surface.blit = Mock()
        set_up = self.get_start_graphic_and_building_mocks(surface_width, y_position)
        set_up[0].image = 'image'

        set_up[0].draw(surface)

        surface.blit.assert_called_once_with('image', set_up[0].position)

