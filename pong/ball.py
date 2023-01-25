import pygame as pg
import random
import math


class Ball:
    COLOR = (255, 255, 255)
    RADIUS = 15
    MAX_VELOCITY = 5

    def __init__(self, x: int, y: int) -> None:
        self.x = self.original_x = x
        self.y = self.original_y = y

        angle = Ball._get_random_angle()
        direction = random.choice([-1, 1])

        self.x_velocity = direction * abs(math.cos(angle) * Ball.MAX_VELOCITY)
        self.y_velocity = math.sin(angle) * Ball.MAX_VELOCITY

    @staticmethod
    def _get_random_angle(low: int = -30, high: int = 30):
        angle = 0
        while angle == 0:
            angle = math.radians(random.randrange(low, high))
        return angle

    def draw(self, screen: pg.surface) -> None:
        pg.draw.circle(screen, Ball.COLOR, (self.x, self.y), Ball.RADIUS)

    def move(self) -> None:
        self.x += self.x_velocity
        self.y += self.y_velocity

    def reset(self) -> None:
        self.x = self.original_x
        self.y = self.original_y

        angle = Ball._get_random_angle()

        self.x_velocity *= -1
        self.y_velocity = math.sin(angle) * Ball.MAX_VELOCITY
