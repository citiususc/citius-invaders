# -*- coding: utf-8 -*-
# pylint: disable=
"""
Created on Sat May  7 11:50:42 2016

@author: T. Teijeiro
"""

import sge

class InvadersGame(sge.dsp.Game):
    """
    Main class for the game. It manages the global actions affecting all the
    objects in the game.
    """

    def __init__(self):
        """Initializes a new InvadersGame, with all parameters properly set"""
        super(InvadersGame, self).__init__(width=1024, height=768, fps=120,
                                                 window_text="CITIUS-invaders")

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
            self.alarms['generation'] = 360
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

    def event_alarm(self, alarm_id):
        print alarm_id, self.alarms

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