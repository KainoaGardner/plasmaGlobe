import pygame
import math
from random import randint, choice
from .settings import *


def displayGlobe(screen, beams):
    add = randint(1, 100)
    if add < 15:
        beams.append(
            Beam(
                randint(1, 360),
                randint(1, 360),
                randint(1, 360),
                randint(RADIUS // 50, RADIUS // 25),
                randint(0, 300),
            )
        )

    for i in range(len(beams) - 1, -1, -1):
        beam = beams[i]
        if beam.life <= 0:
            beams.pop(i)
        else:
            beam.display(screen)

    pygame.draw.circle(
        screen, WHITE, (WIDTH // 2, HEIGHT // 2), RADIUS + RADIUS // 10, 10
    )
    pygame.draw.circle(screen, RED, (WIDTH // 2, HEIGHT // 2), RADIUS // 10)
    pygame.draw.circle(
        screen,
        PURPLE,
        (WIDTH // 2, HEIGHT // 2),
        RADIUS // 10 + randint(1, 5),
        randint(1, 5),
    )


class Beam:
    def __init__(self, xAng, yAng, zAng, size, life):
        self.x = RADIUS - size // 2
        self.y = 0
        self.z = 0
        self.xOff = 0
        self.yOff = 0
        self.zOff = 0
        self.size = size
        self.distance = RADIUS - size // 2
        self.angleX = xAng
        self.angleY = yAng
        self.angleZ = zAng
        self.camZ = RADIUS - size // 2
        self.life = life
        self.direction = randint(0, 2)
        self.posNeg = choice([-1, 1])
        self.speed = randint(5, 10)
        self.linePoints = []
        self.first = True
        self.xDisplay = 0
        self.yDisplay = 0
        self.zDisplay = 0

    def update(self):
        self.getRotation()
        self.life -= 1
        changeLine = randint(1, 100)
        # if self.first:
        #     self.first = False
        #     x =             y = self.y + self.yOff + HEIGHT // 2
        #     self.createLines((x, y))

        if changeLine < 10:
            self.size += randint(-1, 1)
            self.createLines()

        if self.direction == 0:
            self.angleX += self.posNeg / self.speed
        elif self.direction == 1:
            self.angleY += self.posNeg / self.speed
        elif self.direction == 2:
            self.angleZ += self.posNeg / self.speed

    def getRotation(self):
        angleRX = math.radians(self.angleX)
        angleRY = math.radians(self.angleY)
        angleRZ = math.radians(self.angleZ)

        zx = self.x * math.cos(angleRZ) - self.y * math.sin(angleRZ) - self.x
        zy = self.x * math.sin(angleRZ) + self.y * math.cos(angleRZ) - self.y

        yx = (
            (self.x + zx) * math.cos(angleRY)
            - self.z * math.sin(angleRY)
            - (self.x + zx)
        )
        yz = (self.x + zx) * math.sin(angleRY) + self.z * math.cos(angleRY) - self.z

        xy = (
            (self.y + zy) * math.cos(angleRX)
            - (self.z + yz) * math.sin(angleRX)
            - (self.y + zy)
        )
        xz = (
            (self.y + zy) * math.sin(angleRX)
            + (self.z + yz) * math.cos(angleRX)
            - (self.z + yz)
        )

        self.xOff = yx + zx
        self.yOff = zy + xy
        self.zOff = xz + yz

    def display(self, screen):
        if self.z == 0:
            self.z = 1
        self.xDisplay = (self.x + self.xOff) / self.z + WIDTH // 2
        self.yDisplay = (self.y + self.yOff) / self.z + HEIGHT // 2
        self.zDisplay = self.z + self.zOff + self.camZ

        self.update()
        if self.first:
            self.xDisplay = self.x + self.xOff + WIDTH // 2
            self.yDisplay = self.y + self.yOff + HEIGHT // 2
            self.createLines()
            self.first = False

        lineSize = self.size // 3 + randint(1, 10)

        for lineSeg in self.linePoints:
            # pygame.draw.line(screen, BLUE, (lineSeg[0]), (lineSeg[1]), lineSize + 3)
            pygame.draw.line(screen, PURPLE, (lineSeg[0]), (lineSeg[1]), lineSize)
        pygame.draw.circle(
            screen, RED, (self.xDisplay, self.yDisplay), self.size / self.z
        )
        pygame.draw.circle(
            screen,
            PURPLE,
            (self.xDisplay, self.yDisplay),
            self.size + randint(-3, 3),
            randint(1, 3),
        )

    def createLines(self):
        linePoint = []
        bends = randint(1, 5)

        last = [WIDTH // 2, HEIGHT // 2]
        xDif = self.xDisplay - last[0]
        yDif = self.yDisplay - last[1]
        distance = math.sqrt(xDif * xDif + yDif * yDif) / (bends + 1)

        angle = math.degrees(math.atan2(yDif, xDif))

        for _ in range(bends):
            newAngle = angle + randint(-25, 25)
            newX = distance * math.cos(math.radians(newAngle)) + last[0]
            newY = distance * math.sin(math.radians(newAngle)) + last[1]
            point = [last, (newX, newY)]
            linePoint.append(point)
            last = [newX, newY]

        linePoint.append([last, (self.xDisplay, self.yDisplay)])

        self.linePoints = linePoint


beams = []
# for i in range(30):
#     beam = Beam(randint(1, 360), randint(1, 360), randint(1, 360), 10, randint(0, 300))
#     beams.append(beam)
