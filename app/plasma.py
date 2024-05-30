import pygame
import math
from random import randint, choice
from .settings import *

size = 1


def displayGlobe(screen, beams):
    global size
    makeBeam = randint(1, 100)
    if makeBeam < 50 and len(beams) < 20:
        size = randint(1, 10)
        beams.append(
            Beam(
                randint(-360, 360),
                randint(-360, 360),
                RADIUS / 650,
                randint(1, 100),
                (randint(-1, 1), randint(-1, 1)),
                randint(5, 10),
            )
        )

    for i in range(len(beams) - 1, -1, -1):
        beam = beams[i]
        if beam.z < 500:
            if beam.life <= 0:
                beams.pop(i)
            beam.update()

        beam.display(screen)
    pygame.draw.circle(screen, PURPLE, (WIDTH // 2, HEIGHT // 2), RADIUS // 10 + size)
    pygame.draw.circle(screen, RED, (WIDTH // 2, HEIGHT // 2), RADIUS // 10)
    pygame.draw.circle(screen, PINK, (WIDTH // 2, HEIGHT // 2), RADIUS // 30 + size)
    for i in range(len(beams) - 1, -1, -1):
        beam = beams[i]
        if beam.z >= 500:
            if beam.life <= 0:
                beams.pop(i)
            beam.update()
            beam.display(screen)

    pygame.draw.circle(screen, WHITE, (WIDTH // 2, HEIGHT // 2), RADIUS + 15, 15)


class Beam:
    def __init__(self, angleA, angleB, size, life, direction, speed):
        self.angleA = angleA
        self.angleB = angleB
        self.color = RED
        self.scale = size
        self.size = 1
        self.speed = speed

        self.life = life

        self.x = 0
        self.y = 0
        self.z = 0
        self.xBase = 0
        self.yBase = 0
        self.zBase = 0

        self.direction = direction

        self.getPos(self.angleA, self.angleB)
        self.lines = self.createLines()

    def update(self):
        change = randint(1, 100)
        if change < 10:
            self.size += randint(-10, 10)
            self.angleA += randint(-10, 10)
            self.angleB += randint(-10, 10)
            self.lines = self.createLines()

        self.life -= 1
        self.angleA += self.direction[0] / self.speed
        self.angleA += self.direction[1] / self.speed
        sizeChange = self.z / 25
        self.size = sizeChange * self.scale
        self.size += randint(-1, 1)
        self.getPos(self.angleA, self.angleB)

    def getPos(self, angleA, angleB):
        self.x = (
            RADIUS
            * math.cos(math.radians(self.angleA))
            * math.sin(math.radians(self.angleB))
            + WIDTH // 2
        )
        self.y = RADIUS * math.sin(math.radians(self.angleA)) + HEIGHT // 2
        self.z = (
            RADIUS
            * math.cos(math.radians(self.angleA))
            * math.cos(math.radians(self.angleB))
            + WIDTH // 2
        )
        self.xBase = (
            RADIUS
            // 10
            * math.cos(math.radians(self.angleA))
            * math.sin(math.radians(self.angleB))
            + WIDTH // 2
        )
        self.yBase = RADIUS // 10 * math.sin(math.radians(self.angleA)) + HEIGHT // 2

    def createLines(self):
        points = []
        xDif = self.x - WIDTH // 2
        yDif = self.y - HEIGHT // 2
        angle = math.degrees(math.atan2(yDif, xDif))
        totalDist = math.sqrt(xDif * xDif + yDif * yDif)
        beams = randint(1, 5)
        distance = totalDist // (beams + 1)
        last = (self.xBase, self.yBase)
        for _ in range(beams):
            beamDist = distance + randint(
                int(-distance // (beams + 1)), int(distance // (beams + 1))
            )
            beamAngle = angle + randint(-15, 15)
            newX = beamDist * math.cos(math.radians(beamAngle)) + last[0]
            newY = beamDist * math.sin(math.radians(beamAngle)) + last[1]

            point = [(last), (newX, newY)]
            points.append(point)
            last = (newX, newY)
            points.append(point)

        return points

    def display(self, screen):
        for line in self.lines:
            pygame.draw.line(
                screen,
                PURPLE,
                line[0],
                line[1],
                int(self.size) // 2,
            )

            pygame.draw.line(
                screen,
                WHITE,
                line[0],
                line[1],
                int(self.size) // 10,
            )
        pygame.draw.line(
            screen,
            PURPLE,
            self.lines[-1][1],
            (self.x, self.y),
            int(self.size),
        )
        pygame.draw.line(
            screen,
            WHITE,
            self.lines[-1][1],
            (self.x, self.y),
            int(self.size) // 10,
        )

        pygame.draw.circle(screen, PURPLE, (self.x, self.y), self.size + 5)
        pygame.draw.circle(screen, RED, (self.x, self.y), self.size)
        pygame.draw.circle(screen, PINK, (self.x, self.y), self.size // 2)


beams = []
