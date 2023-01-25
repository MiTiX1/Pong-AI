from dataclasses import dataclass

import pygame as pg

from pong.ball import Ball
from pong.paddle import Paddle


@dataclass
class GameInformation:
    left_score: int = 0
    left_hits: int = 0
    right_score: int = 0
    right_hits: int = 0


class CoreGame:
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    BACKGROUND = (0, 0, 0)
    FONT_COLOR = (255, 255, 255)
    FONT_COLOR_2 = (255, 0, 0)
    FONT = "Arial"

    def __init__(self) -> None:
        pg.font.init()
        self.screen = pg.display.set_mode((CoreGame.SCREEN_WIDTH, CoreGame.SCREEN_HEIGHT))
        self.font = pg.font.SysFont(CoreGame.FONT, 64)
        self.left_paddle = Paddle(10, CoreGame.SCREEN_HEIGHT // 2 - Paddle.HEIGHT // 2)
        self.right_paddle = Paddle(CoreGame.SCREEN_WIDTH - Paddle.WIDTH - 10,
                                   CoreGame.SCREEN_HEIGHT // 2 - Paddle.HEIGHT // 2)
        self.ball = Ball(CoreGame.SCREEN_WIDTH // 2, CoreGame.SCREEN_HEIGHT // 2)
        self.game_information = GameInformation()

    def _draw_score(self) -> None:
        left_score = self.font.render(str(self.game_information.left_score), True, CoreGame.FONT_COLOR)
        right_score = self.font.render(str(self.game_information.right_score), True, CoreGame.FONT_COLOR)

        self.screen.blit(left_score, (CoreGame.SCREEN_WIDTH // 2 - left_score.get_width()*2, 20))
        self.screen.blit(right_score, (CoreGame.SCREEN_WIDTH // 2 + left_score.get_width(), 20))

    def _draw_hits(self) -> None:
        hits = self.font.render(
            str(self.game_information.left_hits + self.game_information.right_hits),
            True,
            CoreGame.FONT_COLOR_2
        )
        self.screen.blit(hits, (CoreGame.SCREEN_WIDTH // 2 - hits.get_width() // 2, 20))

    def _draw_center_line(self) -> None:
        for i in range(10, CoreGame.SCREEN_HEIGHT, CoreGame.SCREEN_HEIGHT // 20):
            if i % 2 == 1:
                continue
            pg.draw.rect(self.screen, self.FONT_COLOR, (CoreGame.SCREEN_WIDTH // 2 - 5, i, 10, 20))

    def draw(self, draw_score: bool = True, draw_hits: bool = False) -> None:
        self.screen.fill(CoreGame.BACKGROUND)

        if draw_score:
            self._draw_score()

        if draw_hits:
            self._draw_hits()

        self._draw_center_line()
        self.left_paddle.draw(self.screen)
        self.right_paddle.draw(self.screen)
        self.ball.draw(self.screen)

    def _handle_collision(self) -> None:
        if self.ball.y + Ball.RADIUS >= CoreGame.SCREEN_HEIGHT:
            self.ball.y_velocity *= -1

        if self.ball.y - Ball.RADIUS <= 0:
            self.ball.y_velocity *= -1

        if self.ball.x_velocity < 0:
            if self.left_paddle.y <= self.ball.y <= self.left_paddle.y + Paddle.HEIGHT:
                if self.ball.x - Ball.RADIUS <= self.left_paddle.x + Paddle.WIDTH:
                    self.ball.x_velocity *= -1
                    paddle_center = self.left_paddle.y + Paddle.HEIGHT / 2
                    delta_y = paddle_center - self.ball.y
                    reduction_factor = (Paddle.HEIGHT / 2) / Ball.MAX_VELOCITY
                    y_velocity = delta_y / reduction_factor
                    self.ball.y_velocity = -1 * y_velocity
                    self.game_information.left_hits += 1

        else:
            if self.right_paddle.y <= self.ball.y <= self.right_paddle.y + Paddle.HEIGHT:
                if self.ball.x + Ball.RADIUS >= self.right_paddle.x:
                    self.ball.x_velocity *= -1
                    paddle_center = self.right_paddle.y + Paddle.HEIGHT / 2
                    delta_y = paddle_center - self.ball.y
                    reduction_factor = (Paddle.HEIGHT / 2) / Ball.MAX_VELOCITY
                    y_velocity = delta_y / reduction_factor
                    self.ball.y_velocity = -1 * y_velocity
                    self.game_information.right_hits += 1

    def move_paddle(self, left=True, up=True) -> bool:
        if left:
            if up and self.left_paddle.y - Paddle.VELOCITY < 0:
                return False
            if not up and self.left_paddle.y + Paddle.HEIGHT > CoreGame.SCREEN_HEIGHT:
                return False
            self.left_paddle.move(up)
        else:
            if up and self.right_paddle.y - Paddle.VELOCITY < 0:
                return False
            if not up and self.right_paddle.y + Paddle.HEIGHT > CoreGame.SCREEN_HEIGHT:
                return False
            self.right_paddle.move(up)
        return True

    def loop(self) -> GameInformation:
        self.ball.move()
        self._handle_collision()

        if self.ball.x < 0:
            self.ball.reset()
            self.game_information.right_score += 1
        elif self.ball.x > CoreGame.SCREEN_WIDTH:
            self.ball.reset()
            self.game_information.left_score += 1

        return self.game_information

    def reset(self) -> None:
        self.left_paddle.reset()
        self.right_paddle.reset()
        self.ball.reset()
        self.game_information = GameInformation()


"""clock = pg.time.Clock()
game = CoreGame()
while True:
    clock.tick(144)
    _ = game.loop()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()

    keys = pg.key.get_pressed()
    if keys[pg.K_w]:
        game.move_paddle(left=True, up=True)
    if keys[pg.K_s]:
        game.move_paddle(left=True, up=False)

    game.draw(draw_score=True, draw_hits=False)
    pg.display.update()"""
