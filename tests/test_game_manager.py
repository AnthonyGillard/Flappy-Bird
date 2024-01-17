import unittest
from unittest.mock import Mock, patch, call
from game_manager import GameManager, StartMenu, GameRunning


def single_input_two_outputs(_input):
    return 0, 0


class TestGameManager(unittest.TestCase):
    @patch('game_manager.GameRunning')
    @patch('game_manager.StartMenu')
    @patch('game_manager.Ground', return_value='ground')
    @patch('game_manager.DisplayFactory')
    def get_game_manager_and_building_mocks(self, mocked_display_factory_init, mocked_ground, mocked_start_menu_init,
                                            mocked_game_running_init):
        mocked_application = Mock()
        mocked_application.SURFACE_WIDTH = 'surface_width'
        mocked_application.SURFACE_HEIGHT = 'surface_height'
        mocked_display_factory_init.return_value = mocked_application

        mocked_start_menu = Mock()
        mocked_start_menu.handle_events = Mock(side_effect=single_input_two_outputs)
        mocked_start_menu.increment_game_through_time = Mock()
        mocked_start_menu_init.return_value = mocked_start_menu

        mocked_game_running = Mock()
        mocked_game_running.handle_events = Mock(side_effect=single_input_two_outputs)
        mocked_game_running.increment_game_through_time = Mock()
        mocked_game_running_init.return_value = mocked_game_running

        game_manager = GameManager()
        return game_manager, mocked_application, mocked_ground, mocked_start_menu, mocked_game_running

    def test_init_application_populated_as_expected(self):
        game_manager, mocked_application, _, _, _ = self.get_game_manager_and_building_mocks()

        self.assertEqual(mocked_application, game_manager.application)

    def test_init_grounds_populated_as_expected(self):
        game_manager, _, _, _, _ = self.get_game_manager_and_building_mocks()

        self.assertListEqual( ['ground', 'ground'], game_manager.grounds)

    def test_init_game_states_populated_as_expected(self):
        game_manager, _, _, mocked_start_menu, mocked_game_running = self.get_game_manager_and_building_mocks()

        self.assertListEqual([mocked_start_menu, mocked_game_running], game_manager.game_states)

    def test_init_sets_active_game_state_to_start_menu_index(self):
        game_manager, _, _, mocked_start_menu, _ = self.get_game_manager_and_building_mocks()

        self.assertEqual(mocked_start_menu, game_manager.game_states[game_manager.active_state_index])

    def test_init_sets_no_games_states_as_expected(self):
        game_manager, _, _, mocked_start_menu, _ = self.get_game_manager_and_building_mocks()

        self.assertEqual(2, game_manager.no_game_states)

    def test_manage_events_calls_active_game_state(self):
        game_manager, _, _, mocked_start_menu, _ = self.get_game_manager_and_building_mocks()
        events = 'events'
        game_manager.active_state_index = 0

        game_manager.manage_events(events)

        game_manager.start_menu.handle_events.assert_called_once_with(events)

    def test_increment_game_through_time_calls_active_game_state(self):
        game_manager, _, _, mocked_start_menu, _ = self.get_game_manager_and_building_mocks()
        time_ms = 'time_ms'
        game_manager.active_state_index = 0

        game_manager.increment_game_through_time(time_ms)

        game_manager.start_menu.increment_game_through_time.assert_called_once_with(time_ms, game_manager.grounds)

    def test_increment_game_through_time_sets_active_state_to_2_when_game_over(self):
        game_manager, _, _, mocked_start_menu, _ = self.get_game_manager_and_building_mocks()
        game_manager.active_state_index = 0
        time_ms = 'time_ms'
        game_manager.start_menu.increment_game_through_time.return_value = True

        game_manager.increment_game_through_time(time_ms)

        self.assertEqual(2, game_manager.active_state_index)


class TestStartMenu(unittest.TestCase):
    @patch('game_manager.StartGraphic')
    def get_start_menu_and_building_mocks(self, mocked_start_graphic_init):
        application = Mock()
        application.create_start_menu = Mock()
        application.SURFACE_WIDTH = 100
        application.surface = 'surface'

        mocked_start_graphic = Mock()
        mocked_start_graphic_init.return_value = mocked_start_graphic

        return StartMenu(application), application, mocked_start_graphic

    def test_init_sets_application_as_expected(self):
        start_menu, mocked_application, _ = self.get_start_menu_and_building_mocks()

        self.assertEqual(mocked_application, start_menu.application)

    def test_init_sets_start_graphic_as_expected(self):
        start_menu, _, mocked_start_graphic = self.get_start_menu_and_building_mocks()

        self.assertEqual(mocked_start_graphic, start_menu.start_graphic)

    def test_handle_events_returns_running_true_when_no_exit_event(self):
        start_menu, _, _ = self.get_start_menu_and_building_mocks()
        event = Mock()
        event.type = 0

        running, active_game_state = start_menu.handle_events([event])

        self.assertTrue(running)

    def test_handle_events_returns_running_false_when_exit_event(self):
        start_menu, _, _ = self.get_start_menu_and_building_mocks()
        event = Mock()
        event.type = 256

        running, active_game_state = start_menu.handle_events([event])

        self.assertFalse(running)

    def test_handle_events_returns_active_game_state_zero_when_no_key_pressed(self):
        start_menu, _, _ = self.get_start_menu_and_building_mocks()
        event = Mock()
        event.type = 0

        running, active_game_state = start_menu.handle_events([event])

        self.assertEqual(0, active_game_state)

    def test_handle_events_returns_active_game_state_one_when_space_bar_pressed(self):
        start_menu, _, _ = self.get_start_menu_and_building_mocks()
        event = Mock()
        event.type = 768
        event.key = 32

        running, active_game_state = start_menu.handle_events([event])

        self.assertEqual(1, active_game_state)

    @staticmethod
    def get_mock_ground():
        ground = Mock()
        ground.draw = Mock()
        ground.move = Mock()
        return ground

    def test_increment_game_through_time_moves_ground(self):
        start_menu, _, _ = self.get_start_menu_and_building_mocks()
        ground = self.get_mock_ground()
        time_ms = 'time_ms'

        start_menu.increment_game_through_time(time_ms, [ground])

        ground.move.assert_called_once_with(time_ms)

    def test_increment_game_through_time_creates_start_menu(self):
        start_menu, _, _ = self.get_start_menu_and_building_mocks()
        ground = self.get_mock_ground()
        time_ms = 'time_ms'

        start_menu.increment_game_through_time(time_ms, [ground])

        start_menu.application.create_start_menu.assert_called_once_with([ground], start_menu.start_graphic)


class TestGameRunning(unittest.TestCase):
    @patch('game_manager.Player')
    def get_game_running_and_building_mocks(self, mocked_player_init):
        application = Mock()
        application.create_game_running_view = Mock()
        application.SURFACE_WIDTH = 100
        application.surface = 'surface'

        mocked_player = Mock()
        mocked_player.jump = Mock()
        mocked_player_init.return_value = mocked_player

        return GameRunning(application), application, mocked_player

    def test_init_sets_application_as_expected(self):
        game_running, mocked_application, _ = self.get_game_running_and_building_mocks()

        self.assertEqual(mocked_application, game_running.application)

    def test_init_sets_player_as_expected(self):
        game_running, _, mocked_player = self.get_game_running_and_building_mocks()

        self.assertEqual(mocked_player, game_running.player)

    def test_handle_events_returns_running_true_when_no_exit_event(self):
        game_running, _, _ = self.get_game_running_and_building_mocks()
        event = Mock()
        event.type = 0

        running, active_game_state = game_running.handle_events([event])

        self.assertTrue(running)

    def test_handle_events_returns_running_false_when_exit_event(self):
        game_running, _, _ = self.get_game_running_and_building_mocks()
        event = Mock()
        event.type = 256

        running, active_game_state = game_running.handle_events([event])

        self.assertFalse(running)

    def test_handle_events_returns_active_game_state_one(self):
        game_running, _, _ = self.get_game_running_and_building_mocks()
        event = Mock()
        event.type = 0

        running, active_game_state = game_running.handle_events([event])

        self.assertEqual(1, active_game_state)

    def test_handle_events_jumps_player_when_space_bar_pressed(self):
        game_running, _, _ = self.get_game_running_and_building_mocks()
        event = Mock()
        event.type = 768
        event.key = 119

        game_running.handle_events([event])

        game_running.player.jump.assert_called_once_with()

    @staticmethod
    def get_mock_ground():
        ground = Mock()
        ground.draw = Mock()
        ground.move = Mock()
        return ground

    @patch('pygame.rect.Rect')
    def test_increment_game_through_time_moves_ground(self, mocked_rect):
        mocked_rect.colliderect = Mock(return_value=False)
        game_running, _, _ = self.get_game_running_and_building_mocks()
        ground = self.get_mock_ground()
        time_ms = 'time_ms'

        game_running.increment_game_through_time(time_ms, [ground])

        ground.move.assert_called_once_with(time_ms)

    @patch('pygame.rect.Rect')
    def test_increment_game_through_time_creates_game_running_view(self, mocked_rect):
        mocked_rect.colliderect = Mock(return_value=False)
        game_running, _, _ = self.get_game_running_and_building_mocks()
        ground = self.get_mock_ground()
        time_ms = 'time_ms'

        game_running.increment_game_through_time(time_ms, [ground])

        game_running.application.create_game_running_view.assert_called_once_with([ground], game_running.player)

    @patch('pygame.rect.Rect')
    def test_increment_game_through_time_returns_true_when_collision_detected(self, mocked_rect):
        mocked_rect.colliderect = Mock(return_value=True)
        game_running, _, _ = self.get_game_running_and_building_mocks()
        ground = self.get_mock_ground()
        time_ms = 'time_ms'

        self.assertTrue(game_running.increment_game_through_time(time_ms, [ground]))
