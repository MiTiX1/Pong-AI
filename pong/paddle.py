from typing import List
import pygame as pg


class Paddle:
    COLOR = (255, 255, 255)
    WIDTH = 25
    HEIGHT = 150
    VELOCITY = 4

    def __init__(self, x: int, y: int) -> None:
        self.x = self.original_x = x
        self.y = self.original_y = y

    def draw(self, screen: pg.Surface) -> None:
        pg.draw.rect(screen, Paddle.COLOR, [self.x, self.y, Paddle.WIDTH, Paddle.HEIGHT])

    def move(self, up: bool = True) -> None:
        if up:
            self.y -= Paddle.VELOCITY
        else:
            self.y += Paddle.VELOCITY

    def reset(self) -> None:
        self.x = self.original_x
        self.y = self.original_y
