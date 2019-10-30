import random
import arcade

from game_constants import *


class Paddle:

    def __init__(
            self,
            width=PADDLE_WIDTH, height=PADDLE_INITIAL_HEIGHT,
            color=arcade.color.WHITE,
            x=0, y=SCREEN_HEIGHT // 2,
            velocity_y=0):
        self.width = width
        self.height = height
        self.color = color
        self.x = x
        self.y = y
        self.velocity_y = velocity_y

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, x):
        self.__x = x

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, y):
        self.__y = y

    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self, width):
        self.__width = width

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, height):
        self.__height = height

    @property
    def velocity_y(self):
        return self.__velocity_y

    @velocity_y.setter
    def velocity_y(self, velocity_y):
        self.__velocity_y = velocity_y

    def draw(self):
        arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height, self.color)
        self.velocity_y = 0

    def move_to(self, y, dy=0):
        self.y = y
        self.velocity_y = dy


class Ball:

    def __init__(
            self,
            size=BALL_SIZE,
            color=arcade.color.WHITE,
            x=SCREEN_WIDTH // 2, y=SCREEN_HEIGHT // 2,
            velocity_x=0, velocity_y=0,
            paddles=None):
        self.size = size
        self.color = color
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.paddles = paddles                          # balls have to know about paddles to detect collisions
        self.sprite = arcade.Sprite("jackolantern.gif", 0.5)

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, x):
        self.__x = x

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, y):
        self.__y = y

    @property
    def velocity_x(self):
        return self.__velocity_x

    @velocity_x.setter
    def velocity_x(self, velocity_x):
        self.__velocity_x = velocity_x

    @property
    def velocity_y(self):
        return self.__velocity_y

    @velocity_y.setter
    def velocity_y(self, velocity_y):
        self.__velocity_y = velocity_y

    def update_velocity_after_hit(self, paddle):
        self.reverse_velocity_x()
        self.velocity_x *= HIT_ACCELERATION
        self.velocity_y += paddle.velocity_y // 4         # Todo: Change this to a sloped delta with max of 10 or smth

    def reverse_velocity_x(self):
        self.velocity_x = -self.velocity_x

    def reverse_velocity_y(self):
        self.velocity_y = -self.velocity_y

    def check_for_hit(self):
        for p in self.paddles:
            p_halfwidth = p.width // 2
            p_halfheight = p.height // 2
            # check for hit to the right or left paddle
            if (p.x > self.x and self.velocity_x > 0 and
                    self.x + self.size > p.x - p_halfwidth and
                    self.y + self.size < p.y + p_halfheight and
                    self.y - self.size > p.y - p_halfheight) \
                or (p.x < self.x and self.velocity_x < 0 and
                    self.x - self.size < p.x + p_halfwidth and
                    self.y + self.size < p.y + p_halfheight and
                    self.y - self.size > p.y - p_halfheight):
                self.update_velocity_after_hit(p)

    def update(self):
        # Bounce off the top and bottom edges
        if (self.y + self.size + self.velocity_y > SCREEN_HEIGHT and self.velocity_y > 0) \
                or (self.y - self.size + self.velocity_x < 0 and self.velocity_y < 0):
            self.reverse_velocity_y()

        self.x += self.velocity_x
        self.y += self.velocity_y

        self.check_for_hit()

    def draw(self):
        #print(self.x, self.y)
        #arcade.draw_circle_filled(self.x, self.y, self.size, self.color)
        self.sprite.center_x = self.x
        self.sprite.center_y = self.y
        self.sprite.draw()
