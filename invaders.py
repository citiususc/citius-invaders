# -*- coding: utf-8 -*-
# pylint: disable=
"""
Created on Tue May  3 18:34:45 2016

@author: P. Rodriguez-Mier and T. Teijeiro
"""

import sge
import game
import objects

if __name__ == '__main__':
    # Create Game object
    game.InvadersGame()

    # Load backgrounds
    wall_sprite = sge.gfx.Sprite(width=game.RESX, height=8)
    wall_sprite.draw_rectangle(0, 0, wall_sprite.width, wall_sprite.height,
                               fill=game.CITIUS_COLOR)
    layers = [sge.gfx.BackgroundLayer(wall_sprite, 0,
                                      game.RESY-game.WALL_YOFFSET)]
    background = sge.gfx.Background(layers, sge.gfx.Color("black"))

    # Create objects
    invaders = [objects.Invader() for _ in xrange(6)]
    player = objects.Player()
    obj = invaders + [player]

    # Create room
    sge.game.start_room = game.GameRoom(obj, background=background)
    # Remove the mouse to increase performance by avoiding collision detection
    sge.game.mouse.visible = False
    sge.game.start_room.remove(sge.game.mouse)

    # Here we go!
    sge.game.start()
