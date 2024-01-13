import unittest
from unittest.mock import Mock, patch
from ground import Ground


class TestGround(unittest.TestCase):
    @patch('pygame.image.load')
    @patch('pygame.transform.scale')
    def get_ground_and_building_mocks(self, width, height, ground_height, start_out_of_window,
                                      mocked_pg_scale, mocked_pg_load):
        mocked_pg_rect = Mock()
        mocked_image = Mock()
        mocked_image.get_rect = Mock(return_value=mocked_pg_rect)
        mocked_pg_load.return_value = 'ground'
        mocked_pg_scale.return_value = mocked_image

        return Ground(width, height, ground_height, start_out_of_window), mocked_pg_load, mocked_pg_scale,\
            mocked_image, mocked_pg_rect

    def test_init_populates_width_as_expected(self):
        width = 200

        ground, _, _, _, _ = self.get_ground_and_building_mocks(width, 500, 50, 1)

        self.assertEqual(width, ground.width)

    def test_init_populates_height_as_expected(self):
        height = 50

        ground, _, _, _, _ = self.get_ground_and_building_mocks(200, 500, height, 1)

        self.assertEqual(height, ground.height)

    def test_init_loads_image(self):
        ground, mocked_pg_load, _, _, _ = self.get_ground_and_building_mocks(200, 500, 50, 1)

        mocked_pg_load.assert_called_once_with(ground.FILE_PATH)

    def test_init_scales_images_as_expected(self):
        ground, _, mocked_pg_scale, _, _ = self.get_ground_and_building_mocks(200, 500, 50, 1)

        mocked_pg_scale.assert_called_once_with('ground', (ground.width, ground.height))

    def test_init_generates_hit_box(self):
        ground, _, _, _, mocked_pg_rect = self.get_ground_and_building_mocks(200, 500, 50, 1)

        self.assertEqual(mocked_pg_rect, ground.hit_box)

    def test_init_populates_hit_box_x_as_expected(self):
        width = 200
        start_out_of_window = 1
        ground, _, _, _, _ = self.get_ground_and_building_mocks(width, 500, 50, start_out_of_window)

        self.assertEqual(ground.hit_box.x, 200)

    def test_init_populates_hit_box_y_as_expected(self):
        window_height = 500
        ground_height = 50
        ground, _, _, _, _ = self.get_ground_and_building_mocks(200, window_height, ground_height, 1)

        self.assertEqual(ground.hit_box.y, 450)

    @patch('ground.calculate_derivative_multi_by_time', return_value=20)
    def test_move_changes_x_by_expected_when_on_screen(self, mocked_delta_calc):
        ground, _, _, _, _ = self.get_ground_and_building_mocks(200, 500, 50, 1)
        ground.hit_box.x = 50

        ground.move(1000)

        self.assertEqual(ground.hit_box.x, 30)

    @patch('ground.calculate_derivative_multi_by_time', return_value=150)
    def test_move_resets_x_when_hit_box_has_left_screen(self, mocked_delta_calc):
        width = 100
        ground, _, _, _, _ = self.get_ground_and_building_mocks(width, 500, 50, 1)
        ground.hit_box.x = 50

        ground.move(1000)

        self.assertEqual(ground.hit_box.x, 100)

    def test_draw_calls_blit_function_as_expected(self):
        ground, _, _, mocked_image, mocked_pg_rect = self.get_ground_and_building_mocks(200, 500, 50, 1)
        surface = Mock()
        surface.blit = Mock()

        ground.draw(surface)

        surface.blit.assert_called_once_with(mocked_image, mocked_pg_rect)
