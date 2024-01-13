import unittest
from unittest.mock import Mock, patch, call
from display_factory import DisplayFactory


class TestDisplayFactor(unittest.TestCase):
    @patch('pygame.image.load', return_value='image')
    @patch('pygame.transform.scale')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.display.set_icon')
    def get_display_factory_and_building_mocks(self, mocked_s_icon, mocked_s_caption, mocked_s_mode,
                                               mocked_scale, mocked_load):
        return DisplayFactory(), mocked_s_icon, mocked_s_caption, mocked_s_mode, mocked_scale, mocked_load

    def test_init_loads_background_image(self):
        display_factory, _, _, _, _, mocked_load = self.get_display_factory_and_building_mocks()

        mocked_load.assert_any_call(display_factory.BACKGROUND_FILE_PATH)

    def test_init_scales_background_image(self):
        display_factory, _, _, _, mocked_scale, _ = self.get_display_factory_and_building_mocks()

        mocked_scale.assert_called_once_with('image', (display_factory.SURFACE_WIDTH, display_factory.SURFACE_HEIGHT))

    def test_init_creates_application_surface(self):
        display_factory, _, _, mocked_s_mode, _, _ = self.get_display_factory_and_building_mocks()

        mocked_s_mode.assert_called_once_with((display_factory.SURFACE_WIDTH, display_factory.SURFACE_HEIGHT))

    def test_init_sets_application_caption(self):
        display_factory, _, mocked_s_caption, _, _, _ = self.get_display_factory_and_building_mocks()

        mocked_s_caption.assert_called_once_with('Flappy Bird')

    def test_init_set_application_icon(self):
        display_factory, mocked_s_icon, _, _, _, _ = self.get_display_factory_and_building_mocks()

        mocked_s_icon.assert_called_once_with('image')

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
    def get_mock_start_graphic():
        start_graphic = Mock()
        start_graphic.draw = Mock()
        return start_graphic

    def test_create_start_menu_sets_background(self):
        display_factory, _, _, _, _, _ = self.get_display_factory_and_building_mocks()
        self.add_mock_surface(display_factory)

        display_factory.create_start_menu(self.get_mock_grounds(), self.get_mock_start_graphic())

        display_factory.surface.blit.assert_called_once_with(display_factory.background, (0, 0))

    def test_create_start_menu_adds_ground(self):
        display_factory, _, _, _, _, _ = self.get_display_factory_and_building_mocks()
        self.add_mock_surface(display_factory)
        grounds = self.get_mock_grounds()

        display_factory.create_start_menu(grounds, self.get_mock_start_graphic())

        grounds[0].draw.assert_called_once_with(display_factory.surface)
        grounds[1].draw.assert_called_once_with(display_factory.surface)

    def test_create_start_menu_adds_start_graphic(self):
        display_factory, _, _, _, _, _ = self.get_display_factory_and_building_mocks()
        self.add_mock_surface(display_factory)
        start_graphic = self.get_mock_start_graphic()

        display_factory.create_start_menu(self.get_mock_grounds(), start_graphic)

        start_graphic.draw.assert_called_once_with(display_factory.surface)


