import random
import arcade
import math
from operator import itemgetter

from game_constants import *


class Player:

    def __init__(self, paddle, points=0):
        self.paddle = paddle
        self.points = points

    @property
    def paddle(self):
        return self.__paddle

    @paddle.setter
    def paddle(self, paddle):
        self.__paddle = paddle

    @property
    def points(self):
        return self.__points

    @points.setter
    def points(self, points):
        self.__points = points


class HumanPlayer(Player):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ComputerPlayer(Player):

    def __init__(self, speed=DEFAULT_OPPONENT_SPEED, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.speed = speed

    @property
    def speed(self):
        return self.__speed

    @speed.setter
    def speed(self, speed):
        self.__speed = speed

    def __get_nearest_ball(self, ball_list):
        # get distance of all balls moving towards paddle
        # store them as a list of tuples (Ball, distance from paddle middle)
        c = [(b, math.sqrt((b.x - self.paddle.x)**2 + (b.y - self.paddle.y)**2)) for b in ball_list if b.velocity_x < 0]
        if len(c) > 0:
            nearest_ball = sorted(c, key=itemgetter(1))[0][0]
            return nearest_ball

    def __get_impact_position(self, ball):
        # curent_y = self.paddle.y
        dx = ball.x - ball.size - self.paddle.x
        dy = abs(dx//ball.velocity_x) * ball.velocity_y
        return int(ball.y + dy)

    def __get_move_distance(self, impact_pos):
        dist_y = impact_pos - self.paddle.y
        if dist_y > 10:
            return self.speed
        elif dist_y < -10:
            return -self.speed
        else:
            return 0

    def increase_speed(self):
        self.speed *= OPPONENT_SPEED_INCREASE

    def react(self, ball_list):
        if ball_list:
            nearest_ball = self.__get_nearest_ball(ball_list)
            if nearest_ball:
                self.impact_pos = self.__get_impact_position(ball=nearest_ball)
            else:
                self.impact_pos = SCREEN_HEIGHT // 2
        move_distance = self.__get_move_distance(impact_pos=self.impact_pos)
        self.paddle.move_to(y=self.paddle.y + move_distance)

