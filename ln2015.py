import pygame
from ln_objects import *
from random import randint
import math
import numpy as np
__author__ = 'ajtag'

black = 0, 0, 0
white = 255, 255, 255


FPS = 30

STARS_START = 0
SUNRISE_START = FPS * 30
STARS_FADE = FPS * 30
STARS_END = FPS * 40
CLOUDS_START = FPS * 70
SUNRISE_END = FPS * 90
LIGHTNING_START = FPS * 100
RAIN_START = FPS * 110
LIGHTNING_END = FPS * 120
WAVES_START = FPS * 125
CLOUDS_END = FPS * 130
RAIN_END = FPS * 140

BOUYS_START = FPS * 180
BIRDS_START = FPS * 220
BOUYS_END = FPS * 260

## todo fill this space

WAVES_END = FPS * 370
FOREST_START = FPS * 380
BIRDS_END = FPS * 410

FOREST_END = FPS * 440
SUNSET_START = FPS * 440

CONSTALATION_START = FPS * 490
SUNSET_END = FPS * 510

NORTHERNLIGHTS_START = FPS * 520
NORTHERNLIGHTS_END = FPS * 570

MOONRISE_START = FPS * 550
MOONRISE_END = FPS * 600
CONSTALATION_END = FPS * 600


class LN2015:
    def __init__(self, width, height, fps, mask=True):
        self.width = width
        self.height = height
        self.size = width, height
        self.lightmask = mask
        self.ceiling = Ceiling(self.width, self.height)
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.objects = {}
        self.ticks = 0

    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return False
                elif event.key == pygame.K_m:
                    self.lightmask = not self.lightmask

            if event.type == pygame.QUIT:
                return False

        #background
        if self.ticks < self.fps * 100:
            background = hls_to_rgb(221, 77, min(self.ticks / 500 * 60, 60))

        self.screen.fill( background )

        #Scene 1  millis: 0 -> 40000  stars fading in and out, shooting stars in whites and yellows
        if self.ticks < STARS_END:
            if self.ticks == STARS_START:
                self.objects['starrynight'] = StarrySky((self.width, self.height), self.ceiling)

            self.objects['starrynight'].update()
            self.objects['starrynight'].draw(self.screen)
            if self.ticks == STARS_FADE:
                self.objects['starrynight'].end()
        elif self.ticks == STARS_END:
            del(self.objects['starrynight'])

        #Scene 2  sunrise millis: 20000 -> 70000  Sunrise from south to full basking sun from in the center
        if (SUNRISE_START) <= self.ticks < (SUNRISE_END):
            if self.ticks == SUNRISE_START:
                radius = 100
                self.objects['sun'] = RisingSun((self.width/2) - radius, self.height, radius)

            self.objects['sun'].set_height((  ((self.ticks - SUNRISE_START)/(SUNRISE_END - SUNRISE_START))  * 4 / 6 *pi ) % (4 / 6 *pi))
            self.objects['sun'].draw(self.screen)

        elif self.ticks == SUNRISE_END:
            del(self.objects['sun'])





        # Scene 3: clouds  millis: 55 -> 100 white clouds come in from arms and pass, then getting denser, finally covering the sun and going grey.
        if (CLOUDS_START) < self.ticks < (CLOUDS_END):
            pass



        # Scene 4: lightning sheet and fork lightning happen
        # if (LIGHTNING_START) < self.ticks < (LIGHTNING_END):
        #     pass
        # # Scene 5: rain  rain starts falling with blue splashes, to a torrent, flooding the ceiling
        # if (RAIN_START) < self.ticks < (RAIN_END):
        #     pass
        # Scene 6: wash     cresting waves crash over the ceiling
        # if (CLOUDS_START) < self.ticks < (CLOUDS_END):
        #     pass
        # # Scene 7: waves calm to a steady roll
        # if (CLOUDS_START) < self.ticks < (CLOUDS_END):
        #     pass
        # # Scene 8:   beueuys clank, flashing green and red, as they rock.
        # if (CLOUDS_START) < self.ticks < (CLOUDS_END):
        #     pass
        # # Scene 9  birds come into shot, and takes off, flying inland to the forest,
        # if (CLOUDS_START) < self.ticks < (CLOUDS_END):
        #     pass
        # # Scene 10  forest fades into evening sunlight
        # if (CLOUDS_START) < self.ticks < (CLOUDS_END):
        #     pass
        # # Scene 11  sunset
        # if (CLOUDS_START) < self.ticks < (CLOUDS_END):
        #     pass
        # # Scene 12  northern lights
        # if (CLOUDS_START) < self.ticks < (CLOUDS_END):
        #     pass
        # # Scene 13  north star + night sky
        # if (CLOUDS_START) < self.ticks < (CLOUDS_END):
        #     pass
        # # Scene 14 moon rise with hackspace logo.
        # if (CLOUDS_START) < self.ticks < (CLOUDS_END):
        #     pass


        self.ticks += 1

        if self.lightmask:
            self.screen.blit(source=self.ceiling.mask, dest=(0, 0))
        pygame.display.flip()
        self.clock.tick(self.fps)
        return True


if __name__ == "__main__":
    pygame.init()

    scene = LN2015(800, 600, FPS, mask=True)

    alive = True
    while alive:
        alive = scene.run()
