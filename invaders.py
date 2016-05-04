# -*- coding: utf-8 -*-
# pylint: disable=
"""
Created on Tue May  3 18:34:45 2016

@author: T. Teijeiro
"""

import random

import sge

PLAYER_YOFFSET = 50
PLAYER_SPEED = 4
BULLET_START_SPEED = 2
BULLET_ACCELERATION = 0.5

class Game(sge.dsp.Game):

    def event_key_press(self, key, char):
        global game_in_progress
        if key == 'f8':
            sge.gfx.Sprite.from_screenshot().save('screenshot.jpg')
        elif key == 'f11':
            self.fullscreen = not self.fullscreen
        elif key == 'escape':
            self.event_close()
        elif key in ('p', 'enter'):
            self.pause()

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

class Invader(sge.dsp.Object):

    def __init__(self):
        super(Invader, self).__init__(sge.game.width/2., sge.game.height/2.-80,
                                      sprite=sge.gfx.Sprite(name='invader'))

    def event_step(self, time_passed, delta_mult):
        self.xvelocity = random.random() * 4 * random.choice((-1, 1))
        self.yvelocity = random.random() * 4 * random.choice((-1, 1))
        #Bouncing off the edges:
        if self.bbox_left < 0:
            self.bbox_left = 0
            self.xvelocity = abs(self.xvelocity)
        elif self.bbox_right > sge.game.current_room.width:
            self.bbox_right = sge.game.current_room.width
            self.xvelocity = -abs(self.xvelocity)
        if self.bbox_top < 0:
            self.bbox_top = 0
            self.yvelocity = abs(self.yvelocity)

    def event_collision(self, other, xdirection, ydirection):
        if isinstance(other, Wall):
            self.yvelocity = max(-abs(self.yvelocity)-BULLET_ACCELERATION, -10)
            self.xvelocity = random.choice([-1, 1]) * random.random()
        elif isinstance(other, Bullet):
            self.destroy()



class Player(sge.dsp.Object):

    def __init__(self):
        self.lkey = "left"
        self.rkey = "right"
        x = sge.game.width / 2.
        y = sge.game.height - PLAYER_YOFFSET
        super(Player, self).__init__(x, y, sprite=sge.gfx.Sprite(name='nao'),
                                     checks_collisions=False)

    def event_step(self, time_passed, delta_mult):
        # Movement
        key_motion = (sge.keyboard.get_pressed(self.rkey) -
                      sge.keyboard.get_pressed(self.lkey))

        self.xvelocity = key_motion * PLAYER_SPEED

        # Keep the paddle inside the window
        if self.bbox_left < 0:
            self.bbox_left = 0
        elif self.bbox_right > sge.game.current_room.width:
            self.bbox_right = sge.game.current_room.width

class Wall(sge.dsp.Object):

    def __init__(self):
        wall_sprite = sge.gfx.Sprite(width=1024, height=8)
        wall_sprite.draw_rectangle(0, 0, wall_sprite.width, wall_sprite.height,
                                   fill=sge.gfx.Color("#EF7D10"))
        super(Wall, self).__init__(0, sge.game.height - 80,
                                   sprite=wall_sprite)

class Bullet(sge.dsp.Object):

    def __init__(self):
        x = sge.game.width / 2
        y = sge.game.height / 2
        super(Bullet, self).__init__(x, y, sprite=ball_sprite)

    def event_create(self):
        self.yvelocity = BULLET_START_SPEED

    def event_step(self, time_passed, delta_mult):
        # Bouncing off of the edges
        if self.bbox_left < 0:
            self.bbox_left = 0
            self.xvelocity = abs(self.xvelocity)
        elif self.bbox_right > sge.game.current_room.width:
            self.bbox_right = sge.game.current_room.width
            self.xvelocity = -abs(self.xvelocity)
        if self.bbox_top < 0:
            self.bbox_top = 0
            self.yvelocity = abs(self.yvelocity)

    def event_collision(self, other, xdirection, ydirection):
        if isinstance(other, Wall):
            self.yvelocity = max(-abs(self.yvelocity)-BULLET_ACCELERATION, -10)
            self.xvelocity = random.choice([-1, 1]) * random.random()


# Create Game object
Game(width=1024, height=768, fps=120, window_text="CITIUS-invaders")

# Load sprites
paddle_sprite = sge.gfx.Sprite(width=8, height=48, origin_x=4, origin_y=24)
ball_sprite = sge.gfx.Sprite(width=8, height=8, origin_x=4, origin_y=4)
paddle_sprite.draw_rectangle(0, 0, paddle_sprite.width, paddle_sprite.height,
                             fill=sge.gfx.Color("white"))
ball_sprite.draw_rectangle(0, 0, ball_sprite.width, ball_sprite.height,
                           fill=sge.gfx.Color("#EF7D10"))

# Load backgrounds
layers = [sge.gfx.BackgroundLayer(paddle_sprite, sge.game.width / 2, 0, -10000,
                                  repeat_up=True, repeat_down=True)]
background = sge.gfx.Background([], sge.gfx.Color("black"))

# Create objects
invaders = [Invader() for _ in xrange(5)]
player = Player()
wall = Wall()
bullet = Bullet()
objects = invaders + [player, wall, bullet]

# Create rooms
sge.game.start_room = sge.dsp.Room(objects, background=background)

sge.game.mouse.visible = False

if __name__ == '__main__':
    sge.game.start()