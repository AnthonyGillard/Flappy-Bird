import unittest
from unittest.mock import Mock, patch
from start_graphic import StartGraphic


class TestStartGraphic(unittest.TestCase):
    @patch('pygame.image.load')
    @patch('pygame.transform.scale')
    def get_start_graphic_and_building_mocks(self, x_position, y_position, mocked_pg_scale, mocked_pg_load):
        mocked_pg_rect = Mock()
        mocked_image = Mock()
        mocked_pg_load.return_value = 'image'

        return StartGraphic(x_position, y_position), mocked_pg_load, mocked_pg_scale

    def test_init_loads_image(self):
        start_graphic, mocked_pg_load, _ = self.get_start_graphic_and_building_mocks(10, 20)

        mocked_pg_load.assert_called_once_with(start_graphic.FILE_PATH)

    def test_init_scales_image(self):
        start_graphic, _, mocked_pg_scale = self.get_start_graphic_and_building_mocks(10, 20)

        mocked_pg_scale.assert_called_once_with('image', (start_graphic.WIDTH, start_graphic.HEIGHT))

    def test_init_populates_position_as_expected(self):
        width = 400
        height = 20

        start_graphic, _, _ = self.get_start_graphic_and_building_mocks(width, height)

        self.assertTupleEqual((112, height), start_graphic.position)

    def test_draw_calls_blit_function_as_expected(self):
        width = 10
        height = 20
        surface = Mock()
        surface.blit = Mock()
        start_graphic, _, _ = self.get_start_graphic_and_building_mocks(width, height)
        start_graphic.image = 'image'

        start_graphic.draw(surface)

        surface.blit.assert_called_once_with('image', start_graphic.position)

