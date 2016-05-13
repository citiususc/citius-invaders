# -*- coding: utf-8 -*-
# pylint: disable=
"""
Created on Sat May  7 11:50:42 2016

@author: T. Teijeiro
"""

import sge
import objects
import evolution
import time

#Resolution constants
RESX = 1024
RESY = 768
#Objects position
PLAYER_YOFFSET = 50
PLAYER_SPEED = 4
BULLET_START_SPEED = 20
WALL_YOFFSET = 70
WALL_HEIGHT = 2
#Number of frames between generations (it is reduced with each generation
#until a lower limit)
GENERATION_TIME = 600
MIN_GEN_TIME = 240
#Citius color
CITIUS_COLOR = sge.gfx.Color("#EF7D10")
#Number of invaders to change the shooting mode
MODE_THRES = 30

class InvadersGame(sge.dsp.Game):
    """
    Main class for the game. It manages the global actions affecting all the
    objects in the game.
    """


    def __init__(self):
        """Initializes a new InvadersGame, with all parameters properly set"""
        super(InvadersGame, self).__init__(width=RESX, height=RESY, fps=120,
                                           collision_events_enabled=False,
                                           window_text="CITIUS-invaders")
        self.gensprite = sge.gfx.Sprite(width=RESX, height=RESY, origin_x=0,
                                        origin_y=0)
        self.scoresprite = sge.gfx.Sprite(width=320, height=120,
                                          origin_x=100, origin_y=100)
        self.hud_font = sge.gfx.Font('minecraftia.ttf', size=20)

        self.alarms['generation'] = GENERATION_TIME
        self.pairs = None
        self.score = 0
        self.anim_sleep = None
        self.mode = 0

    def check_mode(self):
        n_inv = sum(1 for o in self.current_room.objects
                                             if isinstance(o, objects.Invader))
        self.mode = 1 if n_inv > MODE_THRES else 0


    def show_hud(self):
        hud_string = 'SCORE: {0:03d}  INVADERS: {1:03d}'
        num_invaders = sum(1 for o in
                   self.current_room.objects if isinstance(o, objects.Invader))
        self.project_text(self.hud_font, hud_string.format(self.score,
                                         num_invaders), 5, 5, anti_alias=False)

    def event_step(self, time_passed, delta_mult):
        self.show_hud()

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
            global GENERATION_TIME
            inv = {o for o in self.current_room.objects
                                             if isinstance(o, objects.Invader)}
            pairs = evolution.mating_pool_tournament(inv, len(inv)/2)
            if pairs:
                self.pairs = pairs
                self.pause(sprite=self.gensprite)
                #Let's make it a bit harder
                if GENERATION_TIME > MIN_GEN_TIME:
                    GENERATION_TIME -= 20
                self.alarms['generation'] = GENERATION_TIME

    def event_close(self):
        self.end()

    def event_paused_step(self, time_passed, delta_mult):
        self.show_hud()

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
            children_genes = evolution.recombinate([(i1, i2)],
                                                 objects.Invader.gene_props)[0]
            #And add the new individual
            desc = objects.Invader(**children_genes)
            desc.x, desc.y = (i1.x + i2.x)/2, (i1.y+i2.y)/2
            self.current_room.add(desc)
            #Slow down painting to visually improve the animation
            if self.anim_sleep is None:
                #The animation time is adjusted according to the number of new
                #individuals.
                self.anim_sleep = (1.0 if len(self.pairs) == 0
                                       else 0 if len(self.pairs) > 50
                                           else min(1.0, 3.0/len(self.pairs)))
                if self.score > 4:
                    self.anim_sleep = 0
            else:
                time.sleep(self.anim_sleep)
        elif self.pairs is not None:
            #Crossing is finished
            time.sleep(self.anim_sleep)
            self.pairs = self.anim_sleep = None
            self.score += 1
            self.check_mode()
            self.unpause()


    def event_paused_key_press(self, key, char):
        if key == 'escape':
            # This allows the player to still exit while the game is
            # paused, rather than having to unpause first.
            self.event_close()
        else:
            if self.pairs is None:
                self.unpause()

    def event_paused_close(self):
        # This allows the player to still exit while the game is paused,
        # rather than having to unpause first.
        self.event_close()

class GameRoom(sge.dsp.Room):
    def event_step(self, time_passed, delta_mult):
        pass
