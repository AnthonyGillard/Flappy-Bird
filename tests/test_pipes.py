import unittest
from unittest.mock import Mock, patch, call
from pipes import Pipes


class TestPipes(unittest.TestCase):
    call_number = 0

    def get_unique_hit_box_mock(self):
        if self.call_number == 0:
            self.call_number += 1
            return Mock()
        else:
            return Mock()

    @patch('random.random', return_value=0.5)
    @patch('pipes.ImageProcessing.load_and_scale_image')
    def get_pipes_and_building_mocks(self, height_available, surface_width, factor,
                                     mocked_ip_load, mocked_random):
        mocked_image = Mock()
        mocked_image.get_rect = Mock(side_effect=self.get_unique_hit_box_mock)
        mocked_ip_load.return_value = mocked_image
        pipes = Pipes('file_path', height_available, surface_width, factor)
        return pipes, mocked_ip_load, mocked_image

    def test_init_populates_surface_width_correctly(self):
        surface_width = 400
        set_up = self.get_pipes_and_building_mocks(400, surface_width, 1.5)

        self.assertEqual(surface_width, set_up[0].surface_width)

    def test_init_populates_height_available_correctly(self):
        height_available_for_pipes = 400
        set_up = self.get_pipes_and_building_mocks(height_available_for_pipes, 200, 1.5)

        self.assertEqual(height_available_for_pipes, set_up[0].height_available_for_pipes)

    def test_init_calcs_pipe_limitations_at_expected(self):
        set_up = self.get_pipes_and_building_mocks(400, 200, 1.5)

        self.assertEqual(80, set_up[0].min_pipe_displacement)
        self.assertEqual(140, set_up[0].available_range_for_centre)

    def test_init_loads_images_as_expected(self):
        set_up = self.get_pipes_and_building_mocks(400, 200, 1.5)

        set_up[1].assert_has_calls([call('file_path' + set_up[0].FILE_PATH_UPPER_PIPE,
                                         set_up[0].WIDTH, set_up[0].HEIGHT),
                                    call('file_path' + set_up[0].FILE_PATH_LOWER_PIPE,
                                         set_up[0].WIDTH, set_up[0].HEIGHT)])

    def test_init_creates_hit_boxes_as_expected(self):
        set_up = self.get_pipes_and_building_mocks(400, 200, 1.5)

        set_up[2].get_rect.assert_has_calls([call(), call()])

    def test_init_sets_lateral_pipe_position_as_expected(self):
        set_up = self.get_pipes_and_building_mocks(400, 200, 1.5)

        self.assertEqual(300, set_up[0].hit_boxes[0].x)

    def test_init_sets_upper_vertical_pipe_position_as_expected(self):
        set_up = self.get_pipes_and_building_mocks(400, 200, 1.5)

        self.assertEqual(-650, set_up[0].hit_boxes[0].y)

    def test_init_set_lower_vertical_pipe_position_as_expected(self):
        set_up = self.get_pipes_and_building_mocks(400, 200, 1.5)

        self.assertEqual(250, set_up[0].hit_boxes[1].y)

    def test_init_populates_previous_x_position_as_expected(self):
        set_up = self.get_pipes_and_building_mocks(400, 200, 1.5)

        self.assertEqual(300, set_up[0].previous_x)

    @patch('pipes.calculate_derivative_multi_by_time', return_value=20)
    def test_move_decrease_lateral_position_when_on_screen(self, mocked_calculation):
        set_up = self.get_pipes_and_building_mocks(400, 200, 1.5)
        set_up[0].hit_boxes[0].x = 100
        set_up[0].hit_boxes[1].x = 100

        set_up[0].move(1000)

        self.assertEqual(80, set_up[0].hit_boxes[0].x)
        self.assertEqual(80, set_up[0].hit_boxes[1].x)

    @patch('pipes.calculate_derivative_multi_by_time', return_value=2000)
    @patch.object(Pipes, 'reset')
    def test_move_resets_position_when_pipe_out_of_window(self, mocked_reset, mocked_calculation):
        set_up = self.get_pipes_and_building_mocks(400, 200, 1.5)
        set_up[0].hit_boxes[0].x = 100
        set_up[0].hit_boxes[1].x = 100

        set_up[0].move(1000)

        mocked_reset.assert_has_calls([call(), call()])

    def test_draw_draws_both_pipes(self):
        set_up = self.get_pipes_and_building_mocks(400, 200, 1.5)
        mock_surface = Mock()
        mock_surface.blit = Mock()

        set_up[0].draw(mock_surface)

        mock_surface.blit.assert_has_calls([call(set_up[0].pipes[0], set_up[0].hit_boxes[0]),
                                            call(set_up[0].pipes[1], set_up[0].hit_boxes[1])])

    def test_passed_over_player_returns_1_if_just_passed(self):
        set_up = self.get_pipes_and_building_mocks(400, 300, 1.5)
        set_up[0].hit_boxes[0].x = 98
        set_up[0].previous_x = 102

        self.assertTrue(set_up[0].passed_over_player())

    def test_passed_over_player_returns_0_if_passed(self):
        set_up = self.get_pipes_and_building_mocks(400, 200, 1.5)
        set_up[0].hit_boxes[0].x = 96
        set_up[0].previous_x = 98

        self.assertFalse(set_up[0].passed_over_player())

    def test_passed_over_player_returns_0_if_not_reached_player(self):
        set_up = self.get_pipes_and_building_mocks(400, 200, 1.5)
        set_up[0].hit_boxes[0].x = 102
        set_up[0].previous_x = 104

        self.assertFalse(set_up[0].passed_over_player())
