# -*- coding: utf-8 -*-
# pylint: disable=
"""
Created on Sat May  7 11:50:42 2016

@author: T. Teijeiro
"""

import sge
import random
import objects
import evolution

#Resolution constants
RESX = 1024
RESY = 768
#Objects position
PLAYER_YOFFSET = 50
PLAYER_SPEED = 4
BULLET_START_SPEED = 20
WALL_YOFFSET = 80
WALL_HEIGHT = 8
#Number of frames between generations
GENERATION_TIME = 360
#Citius color
CITIUS_COLOR = sge.gfx.Color("#EF7D10")

class InvadersGame(sge.dsp.Game):
    """
    Main class for the game. It manages the global actions affecting all the
    objects in the game.
    """

    def __init__(self):
        """Initializes a new InvadersGame, with all parameters properly set"""
        super(InvadersGame, self).__init__(width=RESX, height=RESY, fps=120,
                                           window_text="CITIUS-invaders")
        self.gensprite = sge.gfx.Sprite(width=RESX, height=RESY, origin_x=0,
                                        origin_y=0)
        self.alarms['generation'] = GENERATION_TIME
        self.pairs = None

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

    def event_alarm(self, alarm_id):
        if alarm_id == 'generation':
            lst = [o for o in self.current_room.objects
                                             if isinstance(o, objects.Invader)]
            pairs = evolution.mating_pool(lst, num_of_pairs=len(lst)/2)

            #pairs = []
            #while len(lst) > 1:
            #    i1 = lst.pop(random.randrange(0, len(lst)))
            #    i2 = lst.pop(random.randrange(0, len(lst)))
            #    pairs.append((i1, i2))

            self.pairs = pairs
            self.pause(sprite=self.gensprite)
            self.alarms['generation'] = GENERATION_TIME

    def event_close(self):
        self.end()

    def event_paused_step(self, time_passed, delta_mult):
        if self.pairs:
            #Draw the next cross operation
            i1, i2 = self.pairs.pop()
            self.gensprite.draw_clear()
            self.gensprite.draw_circle(i1.x+i1.bbox_width/2,
                                       i1.y+i1.bbox_height/2,
                                       i1.bbox_width, outline=CITIUS_COLOR)
            self.gensprite.draw_circle(i2.x+i2.bbox_width/2,
                                       i2.y+i2.bbox_height/2,
                                       i2.bbox_width, outline=CITIUS_COLOR)
            self.gensprite.draw_line(i1.x+i1.bbox_width/2,
                                     i1.y+i1.bbox_height/2,
                                     i2.x+i2.bbox_width/2,
                                     i2.y+i2.bbox_height/2,
                                     CITIUS_COLOR, thickness=2)
            children_genes = evolution.recombinate([(i1, i2)])[0]
            #And add the new individual
            desc = objects.Invader(**children_genes)
            desc.x, desc.y = (i1.x + i2.x)/2., (i1.y+i2.y)/2.
            self.current_room.add(desc)
        else:
            self.unpause()

    def event_paused_key_press(self, key, char):
        if not self.pairs:
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

class GameRoom(sge.dsp.Room):
    def event_step(self, time_passed, delta_mult):
        pass
