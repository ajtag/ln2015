#! /usr/bin/env python3
import logging
logging.basicConfig()

from ln_objects import *
import pygame
from pygame.event import Event

import subprocess as sp
import platform
import glob
import sys


__author__ = 'ajtag'

black = 0, 0, 0
white = 255, 255, 255

FPS = 24
MADRIX_X = 132
MADRIX_Y = 70
SCALE = 8

STARS_START_EVENT = Event(pygame.USEREVENT + 1,  {'objects': 'starrysky', 'method': 'start'})
STARS_FADE_EVENT = Event(pygame.USEREVENT + 2, {'objects': 'starrysky', 'method': 'fade'})
STARS_END_EVENT = Event(pygame.USEREVENT + 3, {'objects': 'starrysky', 'method': 'end'})

STARS_START = FPS * 0 #Star Sounds and Crickets Start
SUNRISE_START = FPS * 30 #Bird Song Dawn Chorus Start
STARS_FADE = FPS * 30 #Stars and Crickets Fade End
STARS_END = FPS * 40 #Star Sounds and Crickets End
SUNRISE_END = FPS * 50 #Sun is Risen
CLOUDS_START = FPS * 60 #Clouds and Wind Sounds Start
LIGHTNING_START = FPS * 100 #Fork and Sheet Lightning Sounds Start
RAIN_START = FPS * 110 #Rain Sounds Start
LIGHTNING_END = FPS * 140 #Lightning Sounds End
WAVES_START = FPS * 150 #Wave and Ambient Sounds Start
CLOUDS_END = FPS * 180 #Clouds Fade End
RAIN_END = FPS * 180 #Rain Sounds End
BOUYS_START = FPS * 200 #Waves Ring Bouys to Make Sounds
BIRDS_START = FPS * 220 #Sea Birds Sounds Start
BOUYS_END = FPS * 240 #Buoys Sounds Stop
WAVES_END = FPS * 260 #Waves Sounds End
FOREST_START = FPS * 250 #Forest Sounds Starts
BIRDS_END = FPS * 260 #Sea Birds Sounds End
FOREST_END = FPS * 270 #Forest Sounds End
SUNSET_START = FPS * 260 #
CONSTALATION_START = FPS * 270 #Night Crickets and Star Sounds Start
SUNSET_END = FPS * 280 #
NORTHERNLIGHTS_START = FPS * 290 #Northern Lights Sounds Start (Ambient Sine Bass Notes ?)
NORTHERNLIGHTS_END = FPS * 310 #Northern Lights Sounds End
MOONRISE_START = FPS * 300 #
MOONRISE_END = FPS * 320 #
CONSTALATION_END = FPS * 320 #Night Crickets and Star Sounds End

class LN2015:
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)

    def __init__(self, title, width, height, fps, mask=True, save=False):
        self.title = title
        self.width = width
        self.height = height
        self.size = width, height
        self.lightmask = mask
        self.ceiling = Ceiling('Resources/pixels.csv')
        self.screen = pygame.Surface(self.size)
        self.display = pygame.display.set_mode((SCALE*MADRIX_X, SCALE*MADRIX_Y))
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.objects = {}
        self.ticks = 0
        self.background = black
        self.log.info('done init')
        self.save_images = True
        self.save_video = save

    def save(self, x, y, ffmpegexe = None):
        if not self.save_video:
            return

        if ffmpegexe is None:
            if 'windows' in platform.platform().lower():
                ffmpegexe = 'C:\\Users\\admin\\Desktop\\ffmpeg-20150921-git-74e4948-win64-static\\bin\\ffmpeg.exe'
            else:
                ffmpegexe = 'ffmpeg'

        command = [ ffmpegexe,
        '-y', # (optional) overwrite output file if it exists
        '-r', '{}'.format(self.fps), # frames per second
        '-i', os.path.join('images','{}_%d.png'.format(self.title)),
        '-an', # Tells FFMPEG not to expect any audio
        '-c:v', 'libx264',
        '-s',  '{}x{}'.format(x, y), # size of one frame
        '{}.mp4'.format(self.title)
        ]
        pipe = sp.call(command)



    def run(self):
        for event in pygame.event.get():

            # Check for quit
            if event.type == pygame.QUIT:
                return False
            #  Check Keys
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False

                elif event.key == pygame.K_QUESTION:
                    self.log.info('''
F1 - save video on exit
F2 - view mask
esc - quit
''')

                elif event.key == pygame.K_F1:
                    self.save_video = not(self.save_video)
                    self.log.warning('save video: {}'.format(self.save_video))

                elif event.key == pygame.K_F2:
                    self.lightmask = not self.lightmask

                elif event.key == pygame.K_s:
                    pygame.event.post(STARS_START_EVENT)

                elif event.key == pygame.K_a:
                    pygame.event.post(STARS_FADE_EVENT)

                elif event.key == pygame.K_d:
                    pygame.event.post(STARS_END_EVENT)


            #  Check for animation events
            if event == STARS_START_EVENT:
                self.objects['starrynight'] = StarrySky((self.width, self.height), self.ceiling)
                self.log.info('======= STARS START =======')

            if event == STARS_FADE_EVENT:
                try:
                    self.objects['starrynight'].end()
                    self.log.info('======= STARS FADE =======')
                except KeyError:
                    self.log.warning('stars isnt running')

            if event == STARS_END_EVENT:
                try:
                    del(self.objects['starrynight'])
                    self.log.info('======= STARS END =======')
                except KeyError:
                    self.log.warning('stars isnt running')


        self.background = black
        self.screen.fill( self.background )





        #Scene 1 millis: 0 -> 40000  stars fading in and out, shooting stars in whites and yellows

        if self.ticks == STARS_START:
            pygame.event.post(STARS_START_EVENT)

        if self.ticks == STARS_END:
            pygame.event.post(STARS_END_EVENT)

        if self.ticks == STARS_FADE:
            pygame.event.post(STARS_FADE_EVENT)
       # elif self.ticks == STARS_END:
       #     del(self.objects['starrynight'])

        #Scene 2  sunrise millis: 20000 -> 70000  Sunrise from south to full basking sun from in the center
        if (SUNRISE_START) <= self.ticks < (SUNRISE_END):
            if self.ticks == SUNRISE_START:
                self.log.info('======= SUNRISE START =======')
                radius = 80

                self.objects['sun'] = RisingSun(400, 100, pygame.Rect(400, 330, 20, 150), radius, 40)

            # sunrise from 6AM to 12noon -> 0 to pi/2

            self.objects['sun'].set_height(((self.ticks - SUNRISE_START)/(SUNRISE_END - SUNRISE_START)))
            self.objects['sun'].draw(self.screen)

        elif self.ticks == SUNRISE_END:
            del(self.objects['sun'])

        # Scene 3: clouds  millis: 55 -> 100 white clouds come in from arms and pass, then getting denser, finally covering the sun and going grey.
        if (CLOUDS_START) <= self.ticks < (CLOUDS_END):
            if (self.ticks == CLOUDS_START):
                self.objects['clouds'] = Clouds(self.size)
                self.log.info('======= CLOUDS START =======')

            self.objects['clouds'].update()
            self.objects['clouds'].draw(self.screen)

        # Scene 4: lightning sheet and fork lightning happen
        if (LIGHTNING_START) < self.ticks < (LIGHTNING_END):
            if (self.ticks == LIGHTNING_START):
                self.objects['ligtning'] = Lightning()
                self.log.info('======= LIGHTNING START =======')

        # # Scene 5: rain  rain starts falling with blue splashes, to a torrent, flooding the ceiling
        if (RAIN_START) <= self.ticks < (RAIN_END):
            if RAIN_START == self.ticks:
                self.objects['raindrops'] = Raindrops(self.size)
            self.objects['raindrops'].update()
            self.objects['raindrops'].draw(self.screen)

        # Scene 6: wash     cresting waves crash over the ceiling
        # if (CLOUDS_START) < self.ticks < (CLOUDS_END):
        #     pass
        # # Scene 7: waves calm to a steady roll
        # if (CLOUDS_START) < self.ticks < (CLOUDS_END):
        #     pass
        # # Scene 8:   bouys clank, flashing green and red, as they rock.
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
        if (MOONRISE_START) <= self.ticks < (MOONRISE_END):
            if self.ticks == MOONRISE_START:
                self.objects['moon'] = HSMoon()

            self.objects['moon'].update()
            self.objects['moon'].draw(self.screen)
            pass



        if 'starrynight' in self.objects:
            self.objects['starrynight'].update()
            self.objects['starrynight'].draw(self.screen)

        self.ticks += 1



        pygame.transform.scale(self.screen, self.display.get_size(), self.display)

        pygame.display.flip()

        if self.save_images:
            savepath = os.path.join('images')

            if not(os.path.isdir(savepath)):
                os.mkdir(savepath)

            savefile = os.path.join('images', '{}_{}.png'.format(self.title, self.ticks))
            pygame.image.save(self.screen, savefile)

        self.clock.tick(self.fps)
        return True


if __name__ == "__main__":
    pygame.init()

    ## delete any files saved from previous runs
    [os.unlink(i) for i in glob.glob(os.path.join('images', '*.png'))]

    scene = LN2015('objects', MADRIX_X, MADRIX_Y, FPS, mask=True)

    alive = True
    while alive:
        alive = scene.run()
    scene.save(MADRIX_X, MADRIX_Y)
    pygame.quit()



sys.exit()

