import unittest
from unittest.mock import Mock, patch, call
from player import Player


class TestPlayer(unittest.TestCase):
    @patch('pipes.ImageProcessing.load_and_scale_image')
    def get_player_and_building_mocks(self, window_width, mocked_ip):
        mocked_pg_rect = Mock()
        mocked_image = Mock()
        mocked_image.get_rect = Mock(return_value=mocked_pg_rect)
        mocked_ip.return_value = mocked_image

        return Player('file_path', window_width), mocked_ip, mocked_image, mocked_pg_rect

    def test_init_loads_bird_images(self):
        set_up = self.get_player_and_building_mocks(200)

        set_up[1].assert_has_calls([
            call('file_path' + set_up[0].FILE_PATH_IMAGE_UP, set_up[0].WIDTH, set_up[0].HEIGHT),
            call('file_path' + set_up[0].FILE_PATH_IMAGE_MID, set_up[0].WIDTH, set_up[0].HEIGHT),
            call('file_path' + set_up[0].FILE_PATH_IMAGE_DOWN, set_up[0].WIDTH, set_up[0].HEIGHT)])

    def test_init_sets_initial_player_position_to_expected(self):
        set_up = self.get_player_and_building_mocks(200)

        self.assertEqual(90, set_up[0].hit_box.x)
        self.assertEqual(0, set_up[0].hit_box.y)
        self.assertEqual(0, set_up[0].v)

    def test_jump_modifies_velocity_as_expected(self):
        set_up = self.get_player_and_building_mocks(200)
        set_up[0].v = 0

        set_up[0].jump()

        self.assertEqual(-200, set_up[0].v)

    @staticmethod
    def get_mock_surface():
        surface = Mock()
        surface.blit = Mock()
        return surface

    def test_draw_uses_up_image_with_positive_velocity(self):
        set_up = self.get_player_and_building_mocks(200)
        set_up[0].bird_up_image = 'bird_up_image'
        set_up[0].v = 20
        surface = self.get_mock_surface()

        set_up[0].draw(surface)

        surface.blit.assert_called_once_with('bird_up_image', set_up[0].hit_box)

    def test_draw_uses_mid_image_with_zero_velocity(self):
        set_up = self.get_player_and_building_mocks(200)
        set_up[0].bird_mid_image = 'bird_mid_image'
        set_up[0].v = 0
        surface = self.get_mock_surface()

        set_up[0].draw(surface)

        surface.blit.assert_called_once_with('bird_mid_image', set_up[0].hit_box)

    def test_draw_uses_down_image_with_negative_velocity(self):
        set_up = self.get_player_and_building_mocks(200)
        set_up[0].bird_down_image = 'bird_down_image'
        set_up[0].v = -20
        surface = self.get_mock_surface()

        set_up[0].draw(surface)

        surface.blit.assert_called_once_with('bird_down_image', set_up[0].hit_box)

    def test_reset_position_resets_player_position_as_expected(self):
        set_up = self.get_player_and_building_mocks(200)

        set_up[0].reset()

        self.assertEqual(90, set_up[0].hit_box.x)
        self.assertEqual(0, set_up[0].hit_box.y)
        self.assertEqual(0, set_up[0].v)