import random
import arcade

from game_constants import *
from game_objects import Paddle, Ball
from game_players import HumanPlayer, ComputerPlayer


def make_ball(paddles=[], speed=INITIAL_BALL_SPEED):
    speed = int(speed)
    vel_x = random.randrange(-speed*100, speed*100+1) / 100
    if vel_x > 0:
        vel_x += speed
    else:
        vel_x -= speed
    ball = Ball(
        velocity_x=vel_x,
        velocity_y=random.randrange(-speed*100, speed*100+1) / 100,
        paddles=paddles
    )
    return ball


class MyGame(arcade.Window):

    def __init__(self, width, height):
        super().__init__(width, height, 'ArcadePong!')
        self.set_update_rate(1/144)

        arcade.set_background_color(arcade.color.BLACK)

        self.ball_list = []
        self.paddle_list = []
        self.object_list = []
        self.computer_opponent = None
        self.human_player = None
        self.ball_init_speed = 0

    def __get_kills(self, balls):
        for b in balls:
            if b.x > SCREEN_WIDTH + BALL_KILL_THRESH or \
                    b.x < -BALL_KILL_THRESH:
                yield b

    def __award_point(self, ball):
        if ball.x <= BALL_KILL_THRESH:
            self.human_player.points += 1
        else:
            self.computer_opponent.points += 1

    def __draw_points(self):
        arcade.draw_text(f'{self.human_player.points}', SCREEN_WIDTH-POINTS_DISPLAY_X_MARGIN, POINTS_DISPLAY_Y, arcade.color.ORANGE, 28)
        arcade.draw_text(f'{self.computer_opponent.points}', POINTS_DISPLAY_X_MARGIN, POINTS_DISPLAY_Y, arcade.color.ORANGE, 28)

    def setup(self):
        human_paddle = Paddle(color=arcade.color.BLUE, x=SCREEN_WIDTH-PADDLE_WIDTH//2-PADDLE_MARGIN)
        computer_paddle = Paddle(color=arcade.color.RED, x=PADDLE_WIDTH//2+PADDLE_MARGIN)
        self.ball_init_speed = INITIAL_BALL_SPEED

        self.human_player = HumanPlayer(paddle=human_paddle)
        self.computer_opponent = ComputerPlayer(paddle=computer_paddle)

        self.paddle_list = [self.human_player.paddle, self.computer_opponent.paddle]
        self.ball_list = [make_ball(paddles=self.paddle_list, speed=self.ball_init_speed) for _ in range(INITIAL_NUMBER_OF_BALLS)]
        self.object_list = self.paddle_list + self.ball_list


    def on_draw(self):
        arcade.start_render()

        for obj in self.object_list:
            obj.draw()
            self.__draw_points()

        if DEBUG:
            self.debug_output()

    def update(self, delta_time):
        for ball in self.ball_list:
            ball.update()

        self.computer_opponent.react(self.ball_list)

        for b in self.__get_kills(self.ball_list):
            self.__award_point(b)
            self.computer_opponent.increase_speed()
            self.ball_init_speed *= BALL_SPEED_INCREASE
            self.ball_list.remove(b)
            self.object_list.remove(b)

    def on_key_press(self, key, key_modifiers):
        pass

    def on_key_release(self, key, key_modifiers):
        pass

    def on_mouse_motion(self, x, y, dx, dy):
        self.human_player.paddle.move_to(y, dy)

    def on_mouse_press(self, x, y, button, key_modifiers):
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        if len(self.ball_list) < INITIAL_NUMBER_OF_BALLS:
            print(self.ball_init_speed)
            self.ball_list = [make_ball(paddles=self.paddle_list, speed=self.ball_init_speed) for _ in range(1)]
            self.object_list += self.ball_list

    def debug_output(self):
        # arcade.draw_text(f'Paddle2 velocity: {self.human_player.paddle.velocity_y}', 800, 20, arcade.color.WHITE, 14)
        # arcade.draw_text(f'Number of balls in game: {len(self.ball_list)}', 800, 40, arcade.color.WHITE, 14)
        # arcade.draw_text(f'Calc impact pos: {self.computer_opponent.impact_pos}', 800, 20, arcade.color.WHITE, 14)
        pass

def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()