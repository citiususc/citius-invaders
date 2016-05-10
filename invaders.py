# -*- coding: utf-8 -*-
# pylint: disable=
"""
Created on Tue May  3 18:34:45 2016

@author: P. Rodriguez-Mier and T. Teijeiro
"""

import sge
import game
import objects


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


if __name__ == '__main__':
    # Create Game object
    #Game(width=1024, height=768, fps=120, window_text="CITIUS-invaders")
    game.InvadersGame()

    # Load backgrounds
    wall_sprite = sge.gfx.Sprite(width=game.RESX, height=8)
    wall_sprite.draw_rectangle(0, 0, wall_sprite.width, wall_sprite.height,
                               fill=CITIUS_COLOR)
    layers = [sge.gfx.BackgroundLayer(wall_sprite, 0, game.RESY-WALL_YOFFSET)]
    background = sge.gfx.Background(layers, sge.gfx.Color("black"))

    # Create objects
    invaders = [objects.Invader() for _ in xrange(30)]
    player = objects.Player()
    obj = invaders + [player]

    # Create rooms
    sge.game.start_room = GameRoom(obj, background=background)

    sge.game.mouse.visible = False
    sge.game.start()
