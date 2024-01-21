import unittest
from unittest.mock import Mock, patch, call
from display_factory import DisplayFactory


class TestDisplayFactor(unittest.TestCase):
    @patch('pygame.font.SysFont')
    @patch('pygame.image.load', return_value='image')
    @patch('pipes.ImageProcessing.load_and_scale_image', return_value='background')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.display.set_icon')
    def get_display_factory_and_building_mocks(self, mocked_s_icon, mocked_s_caption, mocked_s_mode,
                                               mocked_ip, mocked_load, mocked_font_init):
        mocked_font = Mock()
        mocked_font.render = Mock()
        mocked_font_init.return_value = mocked_font
        return DisplayFactory('file_path'), mocked_s_icon, mocked_s_caption, mocked_s_mode, mocked_ip, mocked_load,\
            mocked_font

    def test_init_loads_background_image(self):
        set_up = self.get_display_factory_and_building_mocks()

        set_up[4].assert_called_once_with(
            'file_path' + set_up[0].BACKGROUND_FILE_PATH, set_up[0].SURFACE_WIDTH, set_up[0].SURFACE_HEIGHT)

    def test_init_loads_font(self):
        set_up = self.get_display_factory_and_building_mocks()

        self.assertEqual(set_up[6], set_up[0].font)

    def test_init_creates_application_surface(self):
        set_up = self.get_display_factory_and_building_mocks()

        set_up[3].assert_called_once_with((set_up[0].SURFACE_WIDTH, set_up[0].SURFACE_HEIGHT))

    def test_init_sets_application_caption(self):
        set_up = self.get_display_factory_and_building_mocks()

        set_up[2].assert_called_once_with('Flappy Bird')

    def test_init_set_application_icon(self):
        set_up = self.get_display_factory_and_building_mocks()

        set_up[1].assert_called_once_with('image')

    @staticmethod
    def add_mock_surface(display_factory):
        surface = Mock()
        surface.blit = Mock()

        display_factory.surface = surface
        return display_factory

    @staticmethod
    def get_mock_grounds():
        grounds = list()
        ground_0 = Mock()
        ground_0.draw = Mock()
        ground_1 = Mock()
        ground_1.draw = Mock()

        grounds.append(ground_0)
        grounds.append(ground_1)

        return grounds

    @staticmethod
    def get_mock_asset():
        asset = Mock()
        asset.draw = Mock()
        return asset

    def test_create_start_menu_sets_background(self):
        set_up = self.get_display_factory_and_building_mocks()
        self.add_mock_surface(set_up[0])

        set_up[0].create_start_menu(self.get_mock_grounds(), self.get_mock_asset())

        set_up[0].surface.blit.assert_called_once_with(set_up[0].background, (0, 0))

    def test_create_start_menu_adds_ground(self):
        set_up = self.get_display_factory_and_building_mocks()
        self.add_mock_surface(set_up[0])
        grounds = self.get_mock_grounds()

        set_up[0].create_start_menu(grounds, self.get_mock_asset())

        grounds[0].draw.assert_called_once_with(set_up[0].surface)
        grounds[1].draw.assert_called_once_with(set_up[0].surface)

    def test_create_start_menu_adds_start_graphic(self):
        set_up = self.get_display_factory_and_building_mocks()
        self.add_mock_surface(set_up[0])
        start_graphic = self.get_mock_asset()

        set_up[0].create_start_menu(self.get_mock_grounds(), start_graphic)

        start_graphic.draw.assert_called_once_with(set_up[0].surface)

    def test_create_game_running_view_draws_pipes(self):
        set_up = self.get_display_factory_and_building_mocks()
        self.add_mock_surface(set_up[0])
        grounds = self.get_mock_grounds()
        pipes = self.get_mock_grounds()
        player = self.get_mock_asset()
        score = 25

        set_up[0].create_game_running_view(grounds, player, pipes, score)

        pipes[0].draw.assert_called_once_with(set_up[0].surface)
        pipes[1].draw.assert_called_once_with(set_up[0].surface)

    def test_create_game_running_view_draws_player(self):
        set_up = self.get_display_factory_and_building_mocks()
        self.add_mock_surface(set_up[0])
        grounds = self.get_mock_grounds()
        pipes = self.get_mock_grounds()
        player = self.get_mock_asset()
        score = 25

        set_up[0].create_game_running_view(grounds, player, pipes, score)

        player.draw.assert_called_once_with(set_up[0].surface)

    def test_create_game_running_view_draws_text(self):
        set_up = self.get_display_factory_and_building_mocks()
        self.add_mock_surface(set_up[0])
        grounds = self.get_mock_grounds()
        pipes = self.get_mock_grounds()
        player = self.get_mock_asset()
        score = 25

        rect = Mock()
        score_text = Mock()
        score_text.get_rect = Mock(return_value=rect)
        set_up[0].font = Mock()
        set_up[0].font.render = Mock(return_value=score_text)

        set_up[0].create_game_running_view(grounds, player, pipes, score)

        set_up[0].surface.blit.assert_any_call(score_text, rect)

    def test_game_over_view_draws_game_over_graphic(self):
        set_up = self.get_display_factory_and_building_mocks()
        self.add_mock_surface(set_up[0])
        grounds = self.get_mock_grounds()
        game_over = self.get_mock_asset()
        score = 25

        set_up[0].create_game_over(grounds, game_over, score)

        game_over.draw.assert_called_once_with(set_up[0].surface)


