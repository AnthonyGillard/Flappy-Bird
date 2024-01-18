import pygame
from display_factory import DisplayFactory
from ground import Ground
from start_graphic import StartGraphic
from player import Player
from pipes import Pipes


class GameManager:
    GROUND_HEIGHT = 180

    def __init__(self):
        self.application = DisplayFactory()

        self.grounds = list()
        self.grounds.append(
            Ground(self.application.SURFACE_WIDTH, self.application.SURFACE_HEIGHT, self.GROUND_HEIGHT, 0))
        self.grounds.append(
            Ground(self.application.SURFACE_WIDTH, self.application.SURFACE_HEIGHT, self.GROUND_HEIGHT, 1))

        self.start_menu = StartMenu(self.application)
        self.game_running = GameRunning(self.application, self.GROUND_HEIGHT)

        self.game_states = list()
        self.game_states.append(self.start_menu)
        self.game_states.append(self.game_running)

        self.active_state_index = 0
        self.no_game_states = len(self.game_states)

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
    def __init__(self, application):
        self.application = application
        self.start_graphic = StartGraphic(self.application.SURFACE_WIDTH, 100)

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

    @staticmethod
    def _quit_event_handler(event):
        if event.type == pygame.QUIT:
            return False
        else:
            return True


class GameRunning(GameStateBase):
    def __init__(self, application, ground_height):
        self.application = application
        self.player = Player(self.application.SURFACE_WIDTH)

        self.pipes = list()
        self.pipes.append(Pipes(self.application.SURFACE_HEIGHT - ground_height, self.application.SURFACE_WIDTH, 1))
        self.pipes.append(Pipes(self.application.SURFACE_HEIGHT - ground_height, self.application.SURFACE_WIDTH, 1.5))
        self.pipes.append(Pipes(self.application.SURFACE_HEIGHT - ground_height, self.application.SURFACE_WIDTH, 2.0))

    def handle_events(self, events):
        running = True
        active_game_state = 1
        for event in events:
            running = self._quit_event_handler(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.player.jump()

        return running, active_game_state

    def increment_game_through_time(self, time_ms, grounds):
        collision_detected = False

        self.player.move(time_ms)

        for ground in grounds:
            ground.move(time_ms)
            if pygame.rect.Rect.colliderect(ground.hit_box, self.player.hit_box):
                collision_detected = True

        for pipe in self.pipes:
            pipe.move(time_ms)

        self._draw(grounds)

        return collision_detected

    def _draw(self, grounds):
        self.application.create_game_running_view(grounds, self.player, self.pipes)
