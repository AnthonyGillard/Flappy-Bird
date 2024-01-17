import unittest
from unittest.mock import Mock, patch, call
from player import Player


class TestPlayer(unittest.TestCase):
    @patch('pygame.image.load')
    @patch('pygame.transform.scale')
    def get_player_and_building_mocks(self, window_width,
                                      mocked_pg_scale, mocked_pg_load):
        mocked_pg_rect = Mock()
        mocked_image = Mock()
        mocked_image.get_rect = Mock(return_value=mocked_pg_rect)
        mocked_pg_load.return_value = 'bird'
        mocked_pg_scale.return_value = mocked_image

        return Player(window_width), mocked_pg_load, mocked_pg_scale, \
            mocked_image, mocked_pg_rect

    def test_init_loads_bird_up_image(self):
        player, mocked_pg_load, _, _, _ = self.get_player_and_building_mocks(200)

        mocked_pg_load.assert_any_call(player.FILE_PATH_IMAGE_UP)

    def test_init_loads_bird_mid_image(self):
        player, mocked_pg_load, _, _, _ = self.get_player_and_building_mocks(200)

        mocked_pg_load.assert_any_call(player.FILE_PATH_IMAGE_MID)

    def test_init_loads_bird_down_image(self):
        player, mocked_pg_load, _, _, _ = self.get_player_and_building_mocks(200)

        mocked_pg_load.assert_any_call(player.FILE_PATH_IMAGE_DOWN)

    def test_init_scales_loaded_images(self):
        player, _, mocked_pg_scale, _, _ = self.get_player_and_building_mocks(200)

        mocked_pg_scale.assert_has_calls([call('bird', (player.WIDTH, player.HEIGHT)),
                                          call('bird', (player.WIDTH, player.HEIGHT)),
                                          call('bird', (player.WIDTH, player.HEIGHT))])

    def test_init_sets_initial_player_position_to_expected(self):
        player, _, _, _, _ = self.get_player_and_building_mocks(200)

        self.assertEqual(90, player.hit_box.x)
        self.assertEqual(0, player.hit_box.y)
        self.assertEqual(0, player.v)

    def test_jump_modifies_velocity_as_expected(self):
        player, _, _, _, _ = self.get_player_and_building_mocks(200)
        player.v = 0

        player.jump()

        self.assertEqual(-300, player.v)

    @staticmethod
    def get_mock_surface():
        surface = Mock()
        surface.blit = Mock()
        return surface

    def test_draw_uses_up_image_with_positive_velocity(self):
        player, _, _, _, _ = self.get_player_and_building_mocks(200)
        player.bird_up_image = 'bird_up_image'
        player.v = 20
        surface = self.get_mock_surface()

        player.draw(surface)

        surface.blit.assert_called_once_with('bird_up_image', player.hit_box)

    def test_draw_uses_mid_image_with_zero_velocity(self):
        player, _, _, _, _ = self.get_player_and_building_mocks(200)
        player.bird_mid_image = 'bird_mid_image'
        player.v = 0
        surface = self.get_mock_surface()

        player.draw(surface)

        surface.blit.assert_called_once_with('bird_mid_image', player.hit_box)

    def test_draw_uses_down_image_with_negative_velocity(self):
        player, _, _, _, _ = self.get_player_and_building_mocks(200)
        player.bird_down_image = 'bird_down_image'
        player.v = -20
        surface = self.get_mock_surface()

        player.draw(surface)

        surface.blit.assert_called_once_with('bird_down_image', player.hit_box)

    def test_reset_position_resets_player_position_as_expected(self):
        player, _, _, _, _ = self.get_player_and_building_mocks(200)

        player.reset()

        self.assertEqual(90, player.hit_box.x)
        self.assertEqual(0, player.hit_box.y)
        self.assertEqual(0, player.v)