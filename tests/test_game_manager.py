import unittest
from unittest.mock import Mock, patch, call
from game_manager import GameManager, StartMenu


def single_input_two_outputs(_input):
    return 0, 0


class TestGameManager(unittest.TestCase):
    @patch('game_manager.StartMenu')
    @patch('game_manager.Ground', return_value='ground')
    @patch('game_manager.DisplayFactory')
    def get_game_manager_and_building_mocks(self, mocked_display_factory_init, mocked_ground, mocked_start_menu_init):
        mocked_application = Mock()
        mocked_application.SURFACE_WIDTH = 'surface_width'
        mocked_application.SURFACE_HEIGHT = 'surface_height'
        mocked_display_factory_init.return_value = mocked_application

        mocked_start_menu = Mock()
        mocked_start_menu.handle_events = Mock(side_effect=single_input_two_outputs)
        mocked_start_menu.increment_game_through_time = Mock()
        mocked_start_menu_init.return_value = mocked_start_menu

        game_manager = GameManager()
        return game_manager, mocked_application, mocked_ground, mocked_start_menu

    def test_init_application_populated_as_expected(self):
        game_manager, mocked_application, _, _ = self.get_game_manager_and_building_mocks()

        self.assertEqual(mocked_application, game_manager.application)

    def test_init_grounds_populated_as_expected(self):
        game_manager, _, _, _ = self.get_game_manager_and_building_mocks()

        self.assertListEqual( ['ground', 'ground'], game_manager.grounds)

    def test_init_game_states_populated_as_expected(self):
        game_manager, _, _, mocked_start_menu = self.get_game_manager_and_building_mocks()

        self.assertListEqual([mocked_start_menu], game_manager.game_states)

    def test_init_sets_active_game_state_to_start_menu_index(self):
        game_manager, _, _, mocked_start_menu = self.get_game_manager_and_building_mocks()

        self.assertEqual(mocked_start_menu, game_manager.game_states[game_manager.active_state_index])

    def test_init_sets_no_games_states_as_expected(self):
        game_manager, _, _, mocked_start_menu = self.get_game_manager_and_building_mocks()

        self.assertEqual(1, game_manager.no_game_states)

    def test_manage_events_calls_active_game_state(self):
        game_manager, _, _, mocked_start_menu = self.get_game_manager_and_building_mocks()
        events = 'events'
        game_manager.active_state_index = 0

        game_manager.manage_events(events)

        game_manager.start_menu.handle_events.assert_called_once_with(events)

    def test_increment_game_through_time_calls_active_game_state(self):
        game_manager, _, _, mocked_start_menu = self.get_game_manager_and_building_mocks()
        time_ms = 'time_ms'
        game_manager.active_state_index = 0

        game_manager.increment_game_through_time(time_ms)

        game_manager.start_menu.increment_game_through_time.assert_called_once_with(time_ms, game_manager.grounds)

    def test_increment_game_through_time_sets_active_state_to_2_when_game_over(self):
        game_manager, _, _, mocked_start_menu = self.get_game_manager_and_building_mocks()
        game_manager.active_state_index = 0
        time_ms = 'time_ms'
        game_manager.start_menu.increment_game_through_time.return_value = True

        game_manager.increment_game_through_time(time_ms)

        self.assertEqual(2, game_manager.active_state_index)



