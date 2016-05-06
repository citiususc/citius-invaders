# -*- coding: utf-8 -*-
# pylint: disable-msg=
"""
Created on Tue May  3 14:01:45 2016

@author: T. Teijeiro
"""

#!/usr/bin/env python3

# Pong Example
# Written in 2013, 2014, 2015 by Julian Marchant <onpon4@riseup.net>
#
# To the extent possible under law, the author(s) have dedicated all
# copyright and related and neighboring rights to this software to the
# public domain worldwide. This software is distributed without any
# warranty.
#
# You should have received a copy of the CC0 Public Domain Dedication
# along with this software. If not, see
# <http://creativecommons.org/publicdomain/zero/1.0/>.

import random

import sge

DATA = os.path.join(os.path.dirname(__file__), "data")
PADDLE_XOFFSET = 32
PADDLE_SPEED = 4
PADDLE_VERTICAL_FORCE = 1 / 12.
BALL_START_SPEED = 2
BALL_ACCELERATION = 0.2
BALL_MAX_SPEED = 15
POINTS_TO_WIN = 6
TEXT_OFFSET = 16

game_in_progress = True


class Game(sge.dsp.Game):

    def event_step(self, time_passed, delta_mult):
        self.project_sprite(hud_sprite, 0, self.width / 2, 0)

    def event_key_press(self, key, char):
        global game_in_progress

        if key == 'f8':
            sge.gfx.Sprite.from_screenshot().save('screenshot.jpg')
        elif key == 'f11':
            self.fullscreen = not self.fullscreen
        elif key == 'escape':
            self.event_close()
        elif key in ('p', 'enter'):
            if game_in_progress:
                self.pause()
            else:
                game_in_progress = True
                self.current_room.start()

    def event_close(self):
        self.end()

    def event_paused_key_press(self, key, char):
        if key == 'escape':
            # This allows the player to still exit while the game is
            # paused, rather than having to unpause first.
            self.event_close()
        else:
            self.unpause()

    def event_paused_close(self):
        # This allows the player to still exit while the game is paused,
        # rather than having to unpause first.
        self.event_close()


class Player(sge.dsp.Object):

    score = 0

    def __init__(self, player):
        if player == 1:
            self.joystick = 0
            self.up_key = "w"
            self.down_key = "s"
            x = PADDLE_XOFFSET
            self.hit_direction = 1
        else:
            self.joystick = 1
            self.up_key = "up"
            self.down_key = "down"
            x = sge.game.width - PADDLE_XOFFSET
            self.hit_direction = -1

        y = sge.game.height / 2
        super(Player, self).__init__(x, y, sprite=paddle_sprite,
                                                       checks_collisions=False)

    def event_create(self):
        self.score = 0
        refresh_hud()
        self.trackball_motion = 0

    def event_step(self, time_passed, delta_mult):
        # Movement
        key_motion = (sge.keyboard.get_pressed(self.down_key) -
                      sge.keyboard.get_pressed(self.up_key))
        axis_motion = sge.joystick.get_axis(self.joystick, 1)

        if (abs(axis_motion) > abs(key_motion) and
                abs(axis_motion) > abs(self.trackball_motion)):
            self.yvelocity = axis_motion * PADDLE_SPEED
        elif abs(self.trackball_motion) > abs(key_motion):
            self.yvelocity = self.trackball_motion * PADDLE_SPEED
        else:
            self.yvelocity = key_motion * PADDLE_SPEED

        self.trackball_motion = 0

        # Keep the paddle inside the window
        if self.bbox_top < 0:
            self.bbox_top = 0
        elif self.bbox_bottom > sge.game.current_room.height:
            self.bbox_bottom = sge.game.current_room.height

    def event_joystick_trackball_move(self, joystick, ball, x, y):
        if joystick == self.joystick:
            self.trackball_motion += y


class Ball(sge.dsp.Object):

    def __init__(self):
        x = sge.game.width / 2
        y = sge.game.height / 2
        super(Ball, self).__init__(x, y, sprite=ball_sprite)

    def event_create(self):
        self.serve()

    def event_step(self, time_passed, delta_mult):
        # Scoring
        if self.bbox_right < 0:
            player2.score += 1
            refresh_hud()
            #score_sound.play()
            self.serve(-1)
        elif self.bbox_left > sge.game.current_room.width:
            player1.score += 1
            refresh_hud()
            #score_sound.play()
            self.serve(1)

        # Bouncing off of the edges
        if self.bbox_bottom > sge.game.current_room.height:
            self.bbox_bottom = sge.game.current_room.height
            self.yvelocity = -abs(self.yvelocity)
            #bounce_wall_sound.play()
        elif self.bbox_top < 0:
            self.bbox_top = 0
            self.yvelocity = abs(self.yvelocity)
            #bounce_wall_sound.play()

    def event_collision(self, other, xdirection, ydirection):
        if isinstance(other, Player):
            if other.hit_direction == 1:
                self.bbox_left = other.bbox_right + 1
            else:
                self.bbox_right = other.bbox_left - 1

            self.xvelocity = min(abs(self.xvelocity) + BALL_ACCELERATION,
                                 BALL_MAX_SPEED) * other.hit_direction
            self.yvelocity += (self.y - other.y) * PADDLE_VERTICAL_FORCE
            #bounce_sound.play()

    def serve(self, direction=None):
        global game_in_progress

        if direction is None:
            direction = random.choice([-1, 1])

        self.x = self.xstart
        self.y = self.ystart

        if (player1.score < POINTS_TO_WIN and
                player2.score < POINTS_TO_WIN):
            # Next round
            self.xvelocity = BALL_START_SPEED * direction
            self.yvelocity = 0
        else:
            # Game Over!
            self.xvelocity = 0
            self.yvelocity = 0
            hud_sprite.draw_clear()
            x = hud_sprite.width / 2
            p1text = "WIN" if player1.score > player2.score else "LOSE"
            p2text = "WIN" if player2.score > player1.score else "LOSE"
            hud_sprite.draw_text(hud_font, p1text, x - TEXT_OFFSET,
                                 TEXT_OFFSET, color=sge.gfx.Color("white"),
                                 halign="right", valign="top")
            hud_sprite.draw_text(hud_font, p2text, x + TEXT_OFFSET,
                                 TEXT_OFFSET, color=sge.gfx.Color("white"),
                                 halign="left", valign="top")
            game_in_progress = False


def create_room():
    global player1
    global player2
    player1 = Player(1)
    player2 = Player(2)
    ball = Ball()
    return sge.dsp.Room([player1, player2, ball], background=background)


def refresh_hud():
    # This fixes the HUD sprite so that it displays the correct score.
    hud_sprite.draw_clear()
    x = hud_sprite.width / 2
    hud_sprite.draw_text(hud_font, str(player1.score), x - TEXT_OFFSET,
                         TEXT_OFFSET, color=sge.gfx.Color("white"),
                         halign="right", valign="top")
    hud_sprite.draw_text(hud_font, str(player2.score), x + TEXT_OFFSET,
                         TEXT_OFFSET, color=sge.gfx.Color("white"),
                         halign="left", valign="top")


# Create Game object
Game(width=1024, height=768, fps=120, window_text="Pong")

# Load sprites
paddle_sprite = sge.gfx.Sprite(width=8, height=48, origin_x=4, origin_y=24)
ball_sprite = sge.gfx.Sprite(width=8, height=8, origin_x=4, origin_y=4)
paddle_sprite.draw_rectangle(0, 0, paddle_sprite.width, paddle_sprite.height,
                             fill=sge.gfx.Color("white"))
ball_sprite.draw_rectangle(0, 0, ball_sprite.width, ball_sprite.height,
                           fill=sge.gfx.Color("white"))
hud_sprite = sge.gfx.Sprite(width=320, height=120, origin_x=160, origin_y=0)

# Load backgrounds
layers = [sge.gfx.BackgroundLayer(paddle_sprite, sge.game.width / 2, 0, -10000,
                                  repeat_up=True, repeat_down=True)]
background = sge.gfx.Background(layers, sge.gfx.Color("black"))

# Load fonts
hud_font = sge.gfx.Font("Droid Sans Mono", size=48)

# Load sounds
#bounce_sound = sge.snd.Sound(os.path.join(DATA, 'bounce.wav'))
#bounce_wall_sound = sge.snd.Sound(os.path.join(DATA, 'bounce_wall.wav'))
#score_sound = sge.snd.Sound(os.path.join(DATA, 'score.wav'))

# Create rooms
sge.game.start_room = create_room()

sge.game.mouse.visible = False


if __name__ == '__main__':
    sge.game.start()