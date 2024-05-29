from app import screen, clock
from .settings import *
from .plasma import displayGlobe, beams
import pygame


def main():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        screen.fill(GRAY)
        displayGlobe(screen, beams)
        pygame.display.update()
        clock.tick(FPS)
