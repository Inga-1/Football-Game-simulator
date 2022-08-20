import sys
import pygame
from random import randint, uniform
from pygame.locals import *
import math
import os
from tkinter import *
from tkinter import messagebox

class Point:
    def __init__(self, x=0, y=0):
      self.x = x
      self.y = y
    
    def asPair(self):
        return (self.x, self.y)

    def __repr__(self):
        return self.asPair()

#model 

def point(side, x, y):
    if side==1:
        return Point(x,y)
    else:
        return Point (1160-x, y)

class World:
    def __init__(self, numDefenders=0, numSimulations=0):
        self.numDefenders= numDefenders 
        self.numSimulations= numSimulations
        self.defenders = []
        self.end = False
        self.numGoals = 0
        self.percentage = 0.0
        self.simThusFar = 0

    def initializePlayers(self):
        self.end = False
        self.side= randint(1,2)           
        self.goalkeeper= point(self.side, 92, randint(300, 435))
        self.goalkeeper_dest = point(self.side, 92, randint(300, 435))
        self.simThusFar += 1
        self.defenders = []

        if self.side==1: # and self.striker.x-100 > 166:
            self.striker= Point (randint(250, 600), randint (150, 700))  
            self.ball=Point(self.striker.x-1, self.striker.y)
            # self.defenders= [Point(randint(100, self.striker.x-100), randint (60, 740)) for _ in range(self.numDefenders)]
            while len(self.defenders) < self.numDefenders:
                deff = Point(randint(100, 600), randint(60, 740))
                dist = self.getDist(deff, self.striker)
                if dist >= 100:
                    self.defenders.append(deff)
            self.goal = Point (40, randint(140, 660))

        elif self.side==2: # and self.striker.x+100 < 1043:
            self.striker= Point (randint(600, 950), randint (150, 700))
            self.ball=Point(self.striker.x+1, self.striker.y)
            # self.defenders=[Point(randint(self.striker.x+100, 1100), randint (60, 740)) for _ in range(self.numDefenders)]
            while len(self.defenders) < self.numDefenders:
                deff = Point(randint(600, 1100), randint(60, 740))
                dist = self.getDist(deff, self.striker)
                if dist >= 100:
                    self.defenders.append(deff)
            self.goal = Point (1160, randint(140, 660))


        dist = self.getDist(self.ball, self.goal)

        self.ballVelX = 3 / dist * (self.goal.x - self.ball.x)
        self.ballVelY = 3 / dist * (self.goal.y - self.ball.y)
    
        self.goalkeeperVelY = uniform(-2, 2)

        self.defendVelX_list, self.defendVelY_list = [], []

        for deff in self.defenders:
            bound= math.sqrt((deff.x- self.ball.x)**2 + (deff.y - self.ball.y)**2)
            self.defendVelX_list.append(randint(1, 4)/bound * (self.ball.x - deff.x))
            self.defendVelY_list.append(randint(1, 4)/bound * (self.ball.y - deff.y))
            
    def update(self):
        if self.intercepted():
            self.end = True
        elif self.isGoal():
            self.numGoals += 1
            self.percentage = (self.numGoals / self.simThusFar)*100.0
            self.end = True

        if not self.end:
            if 40<= self.ball.x <=1130 and 40<= self.ball.y <=760: # if ball is in bounds
                # move ball
                self.ball.x +=self.ballVelX
                self.ball.y += self.ballVelY
            else:
                self.end = True

            for i in range(self.numDefenders): # move defenders
                if 40<= self.defenders[i].x <=1120 and 40 <= self.defenders[i].y <= 700:
                    self.defenders[i].x += self.defendVelX_list[i]
                    self.defenders[i].y += self.defendVelY_list[i]

            # move goalkeeper
            self.goalkeeper.y += self.goalkeeperVelY
            if not 300 <= self.goalkeeper.y <= 435: 
                self.goalkeeperVelY *= -1 # switch direction

    def isGoal(self):
        if self.side == 1:
            return self.ball.x <= 40 and 306<= self.ball.y <=493
        elif self.side == 2:
            return self.ball.x >=1120 and 306<= self.ball.y <=493

    def getDist(self, p1, p2):
        return math.sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2)

    # checks if ball got intercepted by an opponent
    def intercepted(self):
        for defender in self.defenders:
            if self.getDist(defender, self.ball) <15: # < radius
                print('Intercepted by defender!')
                return True # a defender intercepted the ball
        
        if self.getDist(self.goalkeeper, self.ball) < 12:
            print('Caught by goalkeeper!')
            return True # the goalkeeper caught the ball

        return False # no one intercepted the ball
    


#view

world = World() # initialize

White= (255, 255, 255)
Green= (80, 200, 80) 
Blue=(0, 0, 255)
Black= (0, 0, 0)
Cyan= (0, 255, 255)
Shadow = (0, 77, 0)

pygame.init()
pygame.display.set_caption('Football game simulation')
window= pygame.display.set_mode((1200, 800))
curDir = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")
sergio = pygame.image.load(curDir + '/sergio_new.png')
sergio_small = pygame.transform.smoothscale(sergio, (40, 60))
sergio_small_flipped = pygame.transform.flip(sergio_small, True, False)
ball=pygame.image.load(curDir + '/ball.png')
ball_small=pygame.transform.smoothscale(ball, (30, 30))
ronaldo= pygame.image.load(curDir + '/ronaldo.png')
ronaldo_small= pygame.transform.smoothscale(ronaldo, (40, 60))
ronaldo_small_flipped= pygame.transform.flip(ronaldo_small, True, False)
mbappe= pygame.image.load(curDir + '/mbappe.png')
mbappe_small= pygame.transform.smoothscale(mbappe, (40, 60))
mbappe_small_flipped= pygame.transform.flip(mbappe_small, True, False)

def drawWorld(world, window, defenders=True, click=False, stats=False):

    def drawDefenders(world, window):
        for i in range(len(world.defendVelX_list)):
            if world.defendVelX_list[i] >= 0:
                window.blit(sergio_small, world.defenders[i].asPair())
            else:
                window.blit(sergio_small_flipped, world.defenders[i].asPair())
        
        if world.side == 1:        
            window.blit(ronaldo_small, (int(world.striker.x), int(world.striker.y)))
            window.blit(mbappe_small_flipped, (int(world.goalkeeper.x), int(world.goalkeeper.y)))
            window.blit(ball_small, (int(world.ball.x), int(world.ball.y)))
        elif world.side == 2:
            window.blit(ronaldo_small_flipped, (int(world.striker.x), int(world.striker.y)))
            window.blit(mbappe_small, (int(world.goalkeeper.x), int(world.goalkeeper.y)))
            window.blit(ball_small, (int(world.ball.x), int(world.ball.y)))

        return window

    pygame.display.get_surface()
    window.fill(Green)
    pygame.draw.lines(window, White, True, [(40, 40), (1160, 40), (1160, 760), (40, 760)], 2)
    
    pygame.draw.line(window, White, (600, 40), (600, 760), 2)
    pygame.draw.circle(window, White, (600, 400), 95, 2)
    pygame.draw.lines(window, White, True, [(40, 195), (243, 195), (243, 605), (40, 605)], 2)
    pygame.draw.lines(window, White, True, [(955, 195), (1160, 195), (1160, 605), (955, 605)], 2)
    pygame.draw.lines(window, White, True, [(40, 305), (95, 305), (95, 493), (40, 493)], 2)    
    pygame.draw.lines(window, White, True, [(1105, 305), (1160, 305), (1160, 493), (1105, 493)], 2)
    pygame.draw.circle(window, White, (150, 400), 3)
    pygame.draw.circle(window, White, (1050, 400), 3)

    arc1=pygame.Surface((190, 190))
    arc1.fill(Green)
    pygame.draw.circle(arc1, White, (95, 95), 95, 2)
    pygame.draw.rect(arc1, Blue, (0, 0, 150, 190))
    arc1.set_colorkey(Blue)
    window.blit(arc1, (96, 305))

    arc2=pygame.transform.rotate(arc1, 180)
    window.blit(arc2, (914, 305))

    if defenders:
        window = drawDefenders(world, window) 
    else:
        pygame.draw.rect(window, Shadow, (403, 353, 400, 100)) # shadow
        pygame.draw.rect(window, Cyan, (400, 350, 400, 100)) # banner
        font = pygame.font.SysFont('Consolas', 20)
        if stats:
            prompt = font.render('PERCENTAGE OF GOALS SCORED:', True, Black)
            font = pygame.font.SysFont('Consolas', 35)
            percent = font.render(f'{world.percentage:.2f}%', True, Blue)
            font = pygame.font.SysFont('Consolas', 15)
            clickAnywhere = font.render('CLICK ANYWHERE TO RESTART', True, Shadow)
            window.blit(prompt, (450, 365))
            window.blit(percent, (545, 390))
            window.blit(clickAnywhere, (500, 428))
        else:
            if click == False:
                prompt = font.render('HOW MANY DEFENDERS AND SIMULATIONS?', True, Black)
                font = pygame.font.SysFont('Consolas', 15)
                subtext = font.render('(OPEN THE TERMINAL FOR INPUT)', True, Shadow)
                window.blit(prompt, (408, 380))
                window.blit(subtext, (483, 405))
            else:
                prompt = font.render(' CLICK ANYWHERE TO BEGIN ANIMATION', True, Black)
                window.blit(prompt, (408, 395))


    window.blit(window, (0, 0))
    
    pygame.display.update()


drawWorld(world, window, defenders=False)   

clock = pygame.time.Clock()
defenders_simulations = False
stats= False
while True:
    if defenders_simulations == False:
        if stats:
            drawWorld(world, window, defenders=False, stats=True)
            while True:
                event = pygame.event.wait()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    break

        world = World()
        drawWorld(world, window, defenders=False)   

        print('How many defenders on the field?')
        numDef = int(input())
        print('How many simulations would you like to run?')
        numSim = int(input())
        print('On a scale of 1 (slow) to 10 (fast),')
        print('how fast would you like the animation to run?')
        Hz = float(input())
        Hz = int(6.167*math.e**(0.436*Hz))
        # print(f"Actual Hz: {Hz}")
        print('Click on game window to see animation')
        world = World(numDef, numSim)
        drawWorld(world, window, defenders=False, click=True) 
        defenders_simulations = True
        stats = False

    event = pygame.event.wait()

    if event.type == pygame.MOUSEBUTTONDOWN:
        for _ in range(world.numSimulations):
            world.initializePlayers()
            drawWorld(world, window)
            pygame.display.update()
            while not world.end:
                world.update()
                drawWorld(world, window)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                clock.tick(Hz)
        defenders_simulations = False
        stats = True

    elif event.type == pygame.QUIT:
        sys.exit()