# -*- coding: utf-8 -*-
# pylint: disable=
"""
Created on Tue May  3 18:34:45 2016

@author: P. Rodriguez-Mier and T. Teijeiro
"""

import random
import sge
import game

PLAYER_YOFFSET = 50
PLAYER_SPEED = 4
BULLET_START_SPEED = 15
BULLET_ACCELERATION = 0.5
CITIUS_COLOR = sge.gfx.Color("#EF7D10")
WALL_YOFFSET = 80
WALL_HEIGHT = 8

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
        #Invaders size scaling
        elif key in ('up', 'down'):
            if key == 'down':
                invaders[2].image_xscale -= 1.0
                invaders[2].image_yscale -= 1.0
            elif key == 'up':
                invaders[2].image_xscale += 1.0
                invaders[2].image_yscale += 1.0
            invaders[2].bbox_width = (invaders[2].sprite.width *
                                                      invaders[2].image_xscale)
            invaders[2].bbox_height = (invaders[2].sprite.height *
                                                      invaders[2].image_yscale)
        #Invaders color changing
        elif key == 'd':
            v = invaders[2].image_blend.red
            if v > 10:
                invaders[2].image_blend = sge.gfx.Color([v-10, v-10, v-10])
        elif key == 'l':
            v = invaders[2].image_blend.red
            if v < 245:
                invaders[2].image_blend = sge.gfx.Color([v+10, v+10, v+10])

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
    attr_generators = {
        'scale': lambda: random.lognormvariate(0.5, 0.3)+1,
        'alpha': lambda: random.randint(100, 255),
        'xvelocity': lambda: random.lognormvariate(0.1, 0.4),
        'yvelocity': lambda: random.lognormvariate(0.1, 0.4),
        'x_prob_change_dir': lambda: random.uniform(0.001, 0.01),
        'y_prob_change_dir': lambda: random.uniform(0.001, 0.01)
    }

    def __init__(self, **kwargs):
        # Generate random values and update with the ones provided in kwargs
        self.attributes = {k: self.attr_generators.get(k)() for k in self.attr_generators.keys()}
        self.attributes.update(kwargs)
        print self.attributes

        super(Invader, self).__init__(sge.game.width / 2., sge.game.height / 2. - 80,
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

    def event_step(self, time_passed, delta_mult):
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
        if self.bbox_bottom > game.RESY-(WALL_YOFFSET+WALL_HEIGHT):
            self.bbox_bottom = game.RESY-(WALL_YOFFSET+WALL_HEIGHT)
            self.yvelocity = -abs(self.yvelocity)


class Player(sge.dsp.Object):

    def __init__(self):
        self.lkey = "left"
        self.rkey = "right"
        x = sge.game.width / 2.
        y = sge.game.height - PLAYER_YOFFSET
        super(Player, self).__init__(x, y, sprite=sge.gfx.Sprite(name='nao'),
                                     tangible=False)

    def event_step(self, time_passed, delta_mult):
        # Movement
        key_motion = (sge.keyboard.get_pressed(self.rkey) -
                      sge.keyboard.get_pressed(self.lkey))
        self.xvelocity = key_motion * PLAYER_SPEED
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
        super(PlayerBullet, self).__init__(x, player.y, sprite=ball_sprite)

    def event_create(self):
        self.yvelocity = -BULLET_START_SPEED

    def event_step(self, time_passed, delta_mult):
        if self.bbox_bottom < 0:
            self.destroy()

    def event_collision(self, other, xdirection, ydirection):
        if isinstance(other, Invader):
            self.destroy()
            other.destroy()

class GameRoom(sge.dsp.Room):
    def event_step(self, time_passed, delta_mult):
        pass


# Create Game object
Game(width=1024, height=768, fps=120, window_text="CITIUS-invaders")

# Load sprites
paddle_sprite = sge.gfx.Sprite(width=8, height=48, origin_x=4, origin_y=24)
ball_sprite = sge.gfx.Sprite(width=5, height=25, origin_x=4, origin_y=4)
paddle_sprite.draw_rectangle(0, 0, paddle_sprite.width, paddle_sprite.height,
                             fill=sge.gfx.Color("white"))
ball_sprite.draw_rectangle(0, 0, ball_sprite.width, ball_sprite.height,
                           fill=CITIUS_COLOR)
# Load backgrounds
wall_sprite = sge.gfx.Sprite(width=game.RESX, height=8)
wall_sprite.draw_rectangle(0, 0, wall_sprite.width, wall_sprite.height,
                           fill=CITIUS_COLOR)
layers = [sge.gfx.BackgroundLayer(wall_sprite, 0, game.RESY-WALL_YOFFSET)]
background = sge.gfx.Background(layers, sge.gfx.Color("black"))

# Create objects
invaders = [Invader() for _ in xrange(30)]
player = Player()
objects = invaders + [player]

# Create rooms
sge.game.start_room = GameRoom(objects, background=background)

sge.game.mouse.visible = False

if __name__ == '__main__':
    sge.game.start()
