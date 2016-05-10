# -*- coding: utf-8 -*-
# pylint: disable=
"""
Created on Sat May  7 11:50:42 2016

@author: T. Teijeiro
"""

import sge
import random

#Resolution constants
RESX = 1024
RESY = 768

#Number of frames between generations
GENERATION_TIME = 360

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
        self.gensprite.draw_text(sge.gfx.Font("Droid Sans Mono", size=48), 'hi', 0, 0)
        self.alarms['generation'] = GENERATION_TIME

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
            lst = self.invaders[:]
            pairs = []
            while len(lst) > 1:
                i1 = lst.pop(random.randrange(0, len(lst)))
                i2 = lst.pop(random.randrange(0, len(lst)))
                pairs.append((i1, i2))
            self.gensprite.draw_clear()
            for i1, i2 in pairs:
                self.gensprite.draw_line(i1.x, i1.y, i2.x, i2.y,
                                         i1.image_blend, thickness=1, anti_alias=True)
            self.pause(sprite=self.gensprite)
            self.alarms['generation'] = GENERATION_TIME

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