# -*- coding: utf-8 -*-
# pylint: disable-msg=
"""
Created on Tue May 10 17:36:35 2016

This module contains the definition of all clases representing objects in the
game.

@author: T. Teijeiro
"""

import sge
import random
import game

class Invader(sge.dsp.Object):
    attr_generators = {
        'scale': lambda: random.lognormvariate(0.5, 0.3)+1,
        'alpha': lambda: random.randint(100, 255),
        'xvelocity': lambda: random.lognormvariate(0.0, 0.5)/2,
        'yvelocity': lambda: random.lognormvariate(0.0, 0.5)/2,
        'x_prob_change_dir': lambda: random.uniform(0.0, 0.05),
        'y_prob_change_dir': lambda: random.uniform(0.0, 0.05)
    }

    def __init__(self, **kwargs):
        # Generate random values and update with the ones provided in kwargs
        self.attributes = {k: self.attr_generators.get(k)()
                                          for k in self.attr_generators.keys()}
        self.attributes.update(kwargs)
        print self.attributes

        super(Invader, self).__init__(sge.game.width/2., sge.game.height/2.- 80,
                                      sprite=sge.gfx.Sprite(name='invader'),
                                      image_blend=sge.gfx.Color('white'),
                                      checks_collisions=False)

        self.xvelocity = self.attributes.get('xvelocity')
        self.yvelocity = self.attributes.get('yvelocity')
        blend = self.attributes.get('alpha')
        scale = self.attributes.get('scale')
        self.bbox_width = (self.sprite.width * scale)
        self.bbox_height = (self.sprite.height * scale)
        self.image_blend = sge.gfx.Color([blend, blend, blend])
        self.image_xscale = scale
        self.image_yscale = scale
        self.steps = 0

    def event_step(self, time_passed, delta_mult):
        self.steps += 1
        # Change directions
        if random.random() <= self.attributes.get('x_prob_change_dir'):
            self.xvelocity = -self.xvelocity
        if random.random() <= self.attributes.get('y_prob_change_dir'):
            self.yvelocity = -self.yvelocity

        # Bouncing off the edges and the wall
        if self.bbox_left < 0:
            self.bbox_left = 0
            self.xvelocity = abs(self.xvelocity)
        elif self.bbox_right > sge.game.current_room.width:
            self.bbox_right = sge.game.current_room.width
            self.xvelocity = -abs(self.xvelocity)
        if self.bbox_top < 0:
            self.bbox_top = 0
            self.yvelocity = abs(self.yvelocity)
        if self.bbox_bottom > game.RESY-(game.WALL_YOFFSET+game.WALL_HEIGHT):
            self.bbox_bottom = game.RESY-(game.WALL_YOFFSET+game.WALL_HEIGHT)
            self.yvelocity = -abs(self.yvelocity)

    def compare_fitness(self, other):
        if not isinstance(other, Invader):
            raise ValueError('Incomparable types')
        return self.steps.__cmp__(other.steps)


class Player(sge.dsp.Object):

    def __init__(self):
        self.lkey = "left"
        self.rkey = "right"
        x = sge.game.width / 2.
        y = sge.game.height - game.PLAYER_YOFFSET
        super(Player, self).__init__(x, y, sprite=sge.gfx.Sprite(name='nao'),
                                     tangible=False)

    def event_step(self, time_passed, delta_mult):
        # Movement
        key_motion = (sge.keyboard.get_pressed(self.rkey) -
                      sge.keyboard.get_pressed(self.lkey))
        self.xvelocity = key_motion * game.PLAYER_SPEED
        #"Animate" the sprite according to the moving direction
        if key_motion > 0 and self.image_xscale < 0:
            self.image_xscale = 1
        elif key_motion < 0 and self.image_xscale > 0:
            self.image_xscale = -1

        # Keep the paddle inside the window
        if self.bbox_left < 0:
            self.bbox_left = 0
        elif self.bbox_right > sge.game.current_room.width:
            self.bbox_right = sge.game.current_room.width

    def event_key_press(self, key, char):
        #Shooting
        if key == 'space':
            sge.game.current_room.add(PlayerBullet(self))


class PlayerBullet(sge.dsp.Object):

    def __init__(self, player):
        #The bullet appears out of the hands of nao
        x = (player.x if player.image_xscale == -1
                                             else player.x + player.bbox_width)
        ball_sprite = sge.gfx.Sprite(width=3, height=40, origin_x=4, origin_y=4)
        ball_sprite.draw_rectangle(0, 0, ball_sprite.width, ball_sprite.height,
                               fill=game.CITIUS_COLOR)
        super(PlayerBullet, self).__init__(x, player.y, sprite=ball_sprite)

    def event_create(self):
        self.yvelocity = -game.BULLET_START_SPEED

    def event_step(self, time_passed, delta_mult):
        if self.bbox_bottom < 0:
            self.destroy()

    def event_collision(self, other, xdirection, ydirection):
        if isinstance(other, Invader):
            self.destroy()
            other.destroy()
