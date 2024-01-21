import pygame
from display_factory import DisplayFactory
from ground import Ground
from start_graphic import StartGraphic
from game_over_graphic import GameOverGraphic
from player import Player
from pipes import Pipes


class GameManager:
    GROUND_HEIGHT = 180

    def __init__(self, cwd):
        self.application = DisplayFactory(cwd)

        self._create_grounds(cwd)
        self._create_pipes(cwd)

        self.player = Player(cwd, self.application.SURFACE_WIDTH)
        self.score_counter = Score()

        self._create_game_states(cwd)
        self.active_state_index = 0

    def _create_game_states(self, cwd):
        self.game_states = list()
        self.game_states.append(StartMenu(cwd, self.application))
        self.game_states.append(GameRunning(self.application, self.player, self.pipes, self.score_counter))
        self.game_states.append(GameOver(cwd, self.application, self.player, self.pipes, self.score_counter))

    def _create_pipes(self, cwd):
        self.pipes = list()
        self.pipes.append(Pipes(cwd, self.application.SURFACE_HEIGHT - self.GROUND_HEIGHT,
                                self.application.SURFACE_WIDTH, 1))
        self.pipes.append(Pipes(cwd, self.application.SURFACE_HEIGHT - self.GROUND_HEIGHT,
                                self.application.SURFACE_WIDTH, 1.5))
        self.pipes.append(Pipes(cwd, self.application.SURFACE_HEIGHT - self.GROUND_HEIGHT,
                                self.application.SURFACE_WIDTH, 2.0))

    def _create_grounds(self, cwd):
        self.grounds = list()
        self.grounds.append(
            Ground(cwd, self.application.SURFACE_WIDTH, self.application.SURFACE_HEIGHT, self.GROUND_HEIGHT, 0))
        self.grounds.append(
            Ground(cwd, self.application.SURFACE_WIDTH, self.application.SURFACE_HEIGHT, self.GROUND_HEIGHT, 1))

    def manage_events(self, events):
        running, self.active_state_index = self.game_states[self.active_state_index].handle_events(events)
        return running

    def increment_game_through_time(self, time_ms):
        game_over = self.game_states[self.active_state_index].increment_game_through_time(time_ms, self.grounds)
        if game_over:
            self.active_state_index = 2


class GameStateBase:
    @staticmethod
    def _quit_event_handler(event):
        if event.type == pygame.QUIT:
            return False
        else:
            return True


class StartMenu(GameStateBase):
    def __init__(self, cwd, application):
        self.application = application
        self.start_graphic = StartGraphic(cwd, self.application.SURFACE_WIDTH, 100)

    def handle_events(self, events):
        running = True
        active_game_state = 0
        for event in events:
            running = self._quit_event_handler(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    active_game_state = 1

        return running, active_game_state

    def increment_game_through_time(self, time_ms, grounds):
        for ground in grounds:
            ground.move(time_ms)
        self._draw(grounds)
        return False

    def _draw(self, grounds):
        self.application.create_start_menu(grounds, self.start_graphic)


class GameRunning(GameStateBase):
    def __init__(self, application, player, pipes, score_counter):
        self.application = application

        self.player = player
        self.pipes = pipes

        self.score_counter = score_counter

    def handle_events(self, events):
        running = True
        active_game_state = 1
        for event in events:
            running = self._quit_event_handler(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()

        return running, active_game_state

    def increment_game_through_time(self, time_ms, grounds):
        self.player.move(time_ms)

        if self._move_ground_and_check_for_player_collision(time_ms, grounds) or \
                self._move_pipes_and_check_for_player_collision(time_ms):
            return True
        else:
            self._draw(grounds)
            return False

    def _move_ground_and_check_for_player_collision(self, time_ms, grounds):
        for ground in grounds:
            ground.move(time_ms)
            if pygame.rect.Rect.colliderect(ground.hit_box, self.player.hit_box):
                return True
        return False

    def _move_pipes_and_check_for_player_collision(self, time_ms):
        for pipe in self.pipes:
            pipe.move(time_ms)
            for hit_box in pipe.hit_boxes:
                if pygame.rect.Rect.colliderect(hit_box, self.player.hit_box):
                    return True
            if pipe.passed_over_player():
                self.score_counter.increment_score()
        return False

    def _draw(self, grounds):
        self.application.create_game_running_view(grounds, self.player, self.pipes, self.score_counter.get_score())


class GameOver(GameRunning):
    PIPE_START_FACTORS = [1, 1.5, 2.0]

    def __init__(self, cwd, application, player, pipes, score_counter):
        super().__init__(application, player, pipes, score_counter)
        self.game_over_graphic = GameOverGraphic(cwd, self.application.SURFACE_WIDTH, 100)

    def handle_events(self, events):
        running = True
        active_game_state = 2
        for event in events:
            running = self._quit_event_handler(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    for index, pipe in enumerate(self.pipes):
                        pipe.reset(self.PIPE_START_FACTORS[index], 0)
                    self.score_counter.reset_score()
                    self.player.reset()
                    active_game_state = 1

        return running, active_game_state

    def increment_game_through_time(self, time_ms, grounds):
        for ground in grounds:
            ground.move(time_ms)
        self._draw(grounds)
        return False

    def _draw(self, grounds):
        self.application.create_game_over(grounds, self.game_over_graphic, self.score_counter.get_score())


class Score:
    def __init__(self):
        self.score = 0

    def increment_score(self):
        self.score += 1

    def reset_score(self):
        self.score = 0

    def get_score(self):
        return self.score
