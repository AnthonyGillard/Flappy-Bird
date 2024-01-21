import unittest
from unittest.mock import Mock, patch
from ground import Ground


class TestGround(unittest.TestCase):
    @patch('pipes.ImageProcessing.load_and_scale_image')
    def get_ground_and_building_mocks(self, width, height, ground_height, start_out_of_window, mocked_ip):
        mocked_pg_rect = Mock()
        mocked_image = Mock()
        mocked_image.get_rect = Mock(return_value=mocked_pg_rect)
        mocked_ip.return_value = mocked_image

        return Ground('file_path', width, height, ground_height, start_out_of_window), mocked_ip,\
            mocked_image, mocked_pg_rect

    def test_init_populates_width_as_expected(self):
        width = 200

        set_up = self.get_ground_and_building_mocks(width, 500, 50, 1)

        self.assertEqual(width * 1.05, set_up[0].width)

    def test_init_populates_height_as_expected(self):
        height = 50

        set_up = self.get_ground_and_building_mocks(200, 500, height, 1)

        self.assertEqual(height, set_up[0].height)

    def test_init_loads_image(self):
        set_up = self.get_ground_and_building_mocks(200, 500, 50, 1)

        set_up[1].assert_called_once_with('file_path' + set_up[0].FILE_PATH, 210, 50)

    def test_init_generates_hit_box(self):
        set_up = self.get_ground_and_building_mocks(200, 500, 50, 1)

        self.assertEqual(set_up[3], set_up[0].hit_box)

    def test_init_populates_hit_box_x_as_expected(self):
        width = 200
        start_out_of_window = 1
        set_up = self.get_ground_and_building_mocks(width, 500, 50, start_out_of_window)

        self.assertEqual(210, set_up[0].hit_box.x)

    def test_init_populates_hit_box_y_as_expected(self):
        window_height = 500
        ground_height = 50
        set_up = self.get_ground_and_building_mocks(200, window_height, ground_height, 1)

        self.assertEqual(450, set_up[0].hit_box.y)

    @patch('ground.calculate_derivative_multi_by_time', return_value=20)
    def test_move_changes_x_by_expected_when_on_screen(self, mocked_delta_calc):
        set_up = self.get_ground_and_building_mocks(200, 500, 50, 1)
        set_up[0].hit_box.x = 50

        set_up[0].move(1000)

        self.assertEqual(30, set_up[0].hit_box.x)

    @patch('ground.calculate_derivative_multi_by_time', return_value=200)
    def test_move_resets_x_when_hit_box_has_left_screen(self, mocked_delta_calc):
        width = 100
        set_up = self.get_ground_and_building_mocks(width, 500, 50, 1)
        set_up[0].hit_box.x = 50

        set_up[0].move(1000)

        self.assertEqual(105, set_up[0].hit_box.x)

    def test_draw_calls_blit_function_as_expected(self):
        set_up = self.get_ground_and_building_mocks(200, 500, 50, 1)
        surface = Mock()
        surface.blit = Mock()

        set_up[0].draw(surface)

        surface.blit.assert_called_once_with(set_up[2], set_up[3])
