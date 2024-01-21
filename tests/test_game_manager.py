import unittest
from unittest.mock import Mock, patch, call
from game_manager import GameManager, GameStateBase, StartMenu, GameRunning, GameOver, Score


def single_input_two_outputs(_input):
    return 0, 0


def get_mock_application():
    application = Mock()
    application.create_start_menu = Mock()
    application.create_game_over = Mock()
    application.SURFACE_WIDTH = 100
    application.SURFACE_HEIGHT = 300
    application.surface = 'surface'
    return application


def get_mock_ground():
    ground = Mock()
    ground.draw = Mock()
    ground.move = Mock()
    return ground


class TestGameManager(unittest.TestCase):
    @patch('game_manager.GameOver')
    @patch('game_manager.GameRunning')
    @patch('game_manager.StartMenu')
    @patch('game_manager.Ground', return_value='ground')
    @patch('game_manager.Pipes', return_value='pipes')
    @patch('game_manager.Player', return_value='player')
    @patch('game_manager.Score', return_value='score')
    @patch('game_manager.DisplayFactory')
    def get_game_manager_and_building_mocks(self, mocked_display_factory_init, mocked_score, mocked_player,
                                            mocked_pipes, mocked_ground, mocked_start_menu_init,
                                            mocked_game_running_init, mocked_game_over_init):
        mocked_application = Mock()
        mocked_application.SURFACE_WIDTH = 100
        mocked_application.SURFACE_HEIGHT = 200
        mocked_display_factory_init.return_value = mocked_application

        mocked_start_menu = Mock()
        mocked_start_menu.handle_events = Mock(side_effect=single_input_two_outputs)
        mocked_start_menu.increment_game_through_time = Mock()
        mocked_start_menu_init.return_value = mocked_start_menu

        mocked_game_running = Mock()
        mocked_game_running.handle_events = Mock(side_effect=single_input_two_outputs)
        mocked_game_running.increment_game_through_time = Mock()
        mocked_game_running_init.return_value = mocked_game_running

        mocked_game_over = Mock()
        mocked_game_over.handle_events = Mock(side_effect=single_input_two_outputs)
        mocked_game_over.increment_game_through_time = Mock()
        mocked_game_over_init.return_value = mocked_game_over

        game_manager = GameManager('file_path')
        return game_manager, mocked_application, mocked_score, mocked_player, mocked_pipes, mocked_ground,\
            mocked_start_menu, mocked_game_running, mocked_game_over

    def test_init_application_populated_as_expected(self):
        set_up = self.get_game_manager_and_building_mocks()

        self.assertEqual(set_up[0].application, set_up[1])

    def test_init_grounds_populated_as_expected(self):
        set_up = self.get_game_manager_and_building_mocks()

        self.assertListEqual(['ground', 'ground'], set_up[0].grounds)

    def test_init_pipes_populated_as_expected(self):
        set_up = self.get_game_manager_and_building_mocks()

        self.assertListEqual(['pipes', 'pipes', 'pipes'], set_up[0].pipes)

    def test_init_player_populated_as_expected(self):
        set_up = self.get_game_manager_and_building_mocks()

        self.assertEqual('player', set_up[0].player)

    def test_init_score_counter_populated_as_expected(self):
        set_up = self.get_game_manager_and_building_mocks()

        self.assertEqual('score', set_up[0].score_counter)

    def test_init_game_states_populated_as_expected(self):
        set_up = self.get_game_manager_and_building_mocks()

        self.assertListEqual([set_up[6], set_up[7], set_up[8]], set_up[0].game_states)

    def test_init_sets_active_game_state_to_start_menu_index(self):
        set_up = self.get_game_manager_and_building_mocks()

        self.assertEqual(set_up[6], set_up[0].game_states[set_up[0].active_state_index])

    def test_manage_events_calls_active_game_state(self):
        set_up= self.get_game_manager_and_building_mocks()
        events = 'events'
        set_up[0].active_state_index = 0

        set_up[0].manage_events(events)

        set_up[0].game_states[0].handle_events.assert_called_once_with(events)

    def test_increment_game_through_time_calls_active_game_state(self):
        set_up = self.get_game_manager_and_building_mocks()
        time_ms = 'time_ms'
        set_up[0].active_state_index = 0

        set_up[0].increment_game_through_time(time_ms)

        set_up[0].game_states[0].increment_game_through_time.assert_called_once_with(time_ms, set_up[0].grounds)

    def test_increment_game_through_time_sets_active_state_to_2_when_game_over(self):
        set_up = self.get_game_manager_and_building_mocks()
        set_up[0].active_state_index = 0
        time_ms = 'time_ms'
        set_up[0].game_states[0].increment_game_through_time.return_value = True

        set_up[0].increment_game_through_time(time_ms)

        self.assertEqual(2, set_up[0].active_state_index)


class TestGameStateBase(unittest.TestCase):
    def test_quit_event_handler_true_when_no_exit_event(self):
        event = Mock()
        event.type = 0

        self.assertTrue(GameStateBase._quit_event_handler(event))

    def test_quit_event_handler_false_when_exit_event(self):
        event = Mock()
        event.type = 256

        self.assertFalse(GameStateBase._quit_event_handler(event))


class TestStartMenu(unittest.TestCase):
    @patch('game_manager.StartGraphic')
    def get_start_menu_and_building_mocks(self, mocked_start_graphic_init):
        application = get_mock_application()

        mocked_start_graphic = Mock()
        mocked_start_graphic_init.return_value = mocked_start_graphic

        return StartMenu('file_path', application), application, mocked_start_graphic

    def test_init_sets_application_as_expected(self):
        set_up = self.get_start_menu_and_building_mocks()

        self.assertEqual(set_up[1], set_up[0].application)

    def test_init_sets_start_graphic_as_expected(self):
        set_up = self.get_start_menu_and_building_mocks()

        self.assertEqual(set_up[2], set_up[0].start_graphic)

    def test_handle_events_returns_active_game_state_zero_when_no_key_pressed(self):
        set_up = self.get_start_menu_and_building_mocks()
        event = Mock()
        event.type = 0

        running, active_game_state = set_up[0].handle_events([event])

        self.assertEqual(0, active_game_state)

    def test_handle_events_returns_active_game_state_one_when_space_bar_pressed(self):
        set_up = self.get_start_menu_and_building_mocks()
        event = Mock()
        event.type = 768
        event.key = 32

        running, active_game_state = set_up[0].handle_events([event])

        self.assertEqual(1, active_game_state)

    def test_increment_game_through_time_moves_ground(self):
        set_up = self.get_start_menu_and_building_mocks()
        ground = get_mock_ground()
        time_ms = 'time_ms'

        set_up[0].increment_game_through_time(time_ms, [ground])

        ground.move.assert_called_once_with(time_ms)

    def test_increment_game_through_time_creates_start_menu(self):
        set_up = self.get_start_menu_and_building_mocks()
        ground = get_mock_ground()
        time_ms = 'time_ms'

        set_up[0].increment_game_through_time(time_ms, [ground])

        set_up[0].application.create_start_menu.assert_called_once_with([ground], set_up[0].start_graphic)


class TestGameRunning(unittest.TestCase):
    @staticmethod
    def get_game_running_and_building_mocks():
        application = get_mock_application()

        mocked_player = Mock()
        mocked_player.jump = Mock()
        mocked_player.move = Mock()

        mocked_pipes = Mock()
        mocked_pipes.move = Mock()
        mocked_pipes.hit_boxes = [Mock()]

        mocked_score_counter = Mock()

        return GameRunning(application, mocked_player, [mocked_pipes], mocked_score_counter),\
            application, mocked_player, mocked_pipes, mocked_score_counter

    def test_init_sets_application_as_expected(self):
        set_up = self.get_game_running_and_building_mocks()

        self.assertEqual(set_up[1], set_up[0].application)

    def test_init_sets_player_as_expected(self):
        set_up = self.get_game_running_and_building_mocks()

        self.assertEqual(set_up[2], set_up[0].player)

    def test_init_sets_pipes_as_expected(self):
        set_up = self.get_game_running_and_building_mocks()

        self.assertEqual([set_up[3]], set_up[0].pipes)

    def test_init_sets_score_counter_as_expected(self):
        set_up = self.get_game_running_and_building_mocks()

        self.assertEqual(set_up[4], set_up[0].score_counter)

    def test_handle_events_returns_active_game_state_one(self):
        set_up = self.get_game_running_and_building_mocks()
        event = Mock()
        event.type = 0

        running, active_game_state = set_up[0].handle_events([event])

        self.assertEqual(1, active_game_state)

    def test_handle_events_jumps_player_when_space_bar_pressed(self):
        set_up = self.get_game_running_and_building_mocks()
        event = Mock()
        event.type = 768
        event.key = 32

        set_up[0].handle_events([event])

        set_up[0].player.jump.assert_called_once_with()

    @patch('pygame.rect.Rect')
    def test_increment_game_through_time_moves_ground(self, mocked_rect):
        mocked_rect.colliderect = Mock(return_value=False)
        set_up = self.get_game_running_and_building_mocks()
        ground = get_mock_ground()
        time_ms = 'time_ms'

        set_up[0].increment_game_through_time(time_ms, [ground])

        ground.move.assert_called_once_with(time_ms)

    @patch('pygame.rect.Rect')
    def test_increment_game_through_time_moves_pipes(self, mocked_rect):
        mocked_rect.colliderect = Mock(return_value=False)
        set_up = self.get_game_running_and_building_mocks()
        ground = get_mock_ground()
        time_ms = 'time_ms'

        set_up[0].increment_game_through_time(time_ms, [ground])

        set_up[0].pipes[0].move.assert_called_once_with(time_ms)

    @patch('pygame.rect.Rect')
    @patch.object(GameRunning, '_move_pipes_and_check_for_player_collision', return_value=False)
    def test_increment_game_through_time_returns_true_when_ground_collision_detected(self, mocked_pipes_check,
                                                                                     mocked_rect):
        mocked_rect.colliderect = Mock(return_value=True)
        set_up = self.get_game_running_and_building_mocks()
        ground = get_mock_ground()

        self.assertTrue(set_up[0].increment_game_through_time(100, [ground]))

    @patch.object(GameRunning, '_move_ground_and_check_for_player_collision', return_value=False)
    @patch('pygame.rect.Rect')
    def test_increment_game_through_time_returns_false_when_pipe_collision_detected(self, mocked_rect,
                                                                                    mocked_ground_check):
        mocked_rect.colliderect = Mock(return_value=True)
        set_up = self.get_game_running_and_building_mocks()
        ground = get_mock_ground()

        self.assertTrue(set_up[0].increment_game_through_time(100, [ground]))

    @patch('pygame.rect.Rect')
    def test_increment_game_returns_false_when_no_collision_detected(self, mocked_rect):
        mocked_rect.colliderect = Mock(return_value=False)
        set_up = self.get_game_running_and_building_mocks()
        ground = get_mock_ground()

        self.assertFalse(set_up[0].increment_game_through_time(100, [ground]))

    @patch('pygame.rect.Rect')
    def test_increment_game_draws_game_running_when_no_collision_detected(self, mocked_rect):
        mocked_rect.colliderect = Mock(return_value=False)
        set_up = self.get_game_running_and_building_mocks()
        ground = get_mock_ground()

        set_up[0].increment_game_through_time(100, [ground])

        set_up[0].application.create_game_running_view.assert_called_once()


class TestGameOver(unittest.TestCase):
    @patch('game_manager.GameOverGraphic')
    def get_game_over_and_building_mocks(self, mocked_game_over_graphic_init):
        application = get_mock_application()

        mocked_game_over_graphic = Mock()
        mocked_game_over_graphic_init.return_value = mocked_game_over_graphic

        mocked_player = Mock()
        mocked_player.jump = Mock()
        mocked_player.move = Mock()

        mocked_pipes = Mock()
        mocked_pipes.move = Mock()
        mocked_pipes.hit_boxes = [Mock()]

        mocked_score_counter = Mock()

        return GameOver('file_path', application, mocked_player, [mocked_pipes], mocked_score_counter),\
            application, mocked_game_over_graphic, mocked_player, mocked_pipes, mocked_score_counter

    def test_init_sets_game_over_graphic_as_expected(self):
        set_up = self.get_game_over_and_building_mocks()

        self.assertEqual(set_up[2], set_up[0].game_over_graphic)

    def test_handle_events_resets_assets_when_r_is_pressed(self):
        set_up = self.get_game_over_and_building_mocks()
        event = Mock()
        event.type = 768
        event.key = 114

        running, active_game_state = set_up[0].handle_events([event])

        set_up[0].pipes[0].reset.asset_called_once_with(set_up[0].PIPE_START_FACTORS[0])
        set_up[0].score_counter.reset_score.assert_called_once_with()
        set_up[0].player.reset.assert_called_once_with()

    def test_handle_events_sets_active_state_to_one_when_r_is_pressed(self):
        set_up = self.get_game_over_and_building_mocks()
        event = Mock()
        event.type = 768
        event.key = 114

        running, active_game_state = set_up[0].handle_events([event])

        self.assertEqual(1, active_game_state)

    def test_handle_events_returns_active_game_state_to_2_when_no_event(self):
        set_up = self.get_game_over_and_building_mocks()
        event = Mock()
        event.type = 0

        running, active_game_state = set_up[0].handle_events([event])

        self.assertEqual(2, active_game_state)

    def test_increment_game_through_time_moves_ground(self):
        set_up = self.get_game_over_and_building_mocks()
        ground = get_mock_ground()
        time_ms = 'time_ms'

        set_up[0].increment_game_through_time(time_ms, [ground])

        ground.move.assert_called_once_with(time_ms)

    def test_increment_game_through_time_creates_game_over_menu(self):
        set_up = self.get_game_over_and_building_mocks()
        set_up[0].score_counter.get_score = Mock(return_value='score')
        ground = get_mock_ground()
        time_ms = 'time_ms'

        set_up[0].increment_game_through_time(time_ms, [ground])

        set_up[0].application.create_game_over.assert_called_once_with([ground], set_up[0].game_over_graphic, 'score')


class TestScore(unittest.TestCase):
    def test_init_sets_score_to_zero(self):
        score_counter = Score()

        self.assertEqual(0, score_counter.score)

    def test_increment_score_add_one_to_score(self):
        score_counter = Score()

        score_counter.increment_score()

        self.assertEqual(1, score_counter.score)

    def test_reset_score_resets_score_to_zero(self):
        score_counter = Score()
        score_counter.score = 100

        score_counter.reset_score()

        self.assertEqual(0, score_counter.score)

