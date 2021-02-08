#slither getattr
import pygame
import math #needed for sqrt
import random

pygame.init()#initializes Pygame
pygame.display.set_caption("Slithery snake")#window title
screen = pygame.display.set_mode((400,400))#game screen
clock = pygame.time.Clock()#starts game clock

#game variables
doExit = False

#player variables
xPos = 200
yPos = 200
Vx = 1
Vy = 1

#old variables
oldX = 200
oldY = 200
counter = 0

#player 2 variables 
xPos2 = 200
yPos2 = 200
Vx2 = 1
Vy2 = 1

oldX2 = 200
oldY2 = 200
#++++++++++++++++++++++++++++++++++++++++++++++++++++
class pellet:
  def __init__(self, xpos, ypos, red, green, blue, radius):
    self.xpos = xpos
    self.ypos = ypos
    self.red = red
    self.green = green
    self.blue = blue
    self.radius = radius
  def draw(self):
    pygame.draw.circle(screen, (self.red,self.green,self.blue), (self.xpos, self.ypos), self.radius)
  def collide(self, x, y):
    if math.sqrt((x-self.xpos)*(x-self.xpos)+(y-self.ypos)*(y-self.ypos)) < self.radius + 6:
      self.xpos = random.randrange(0, 400)
      self.ypos = random.randrange(0, 400)
      self.red = random.randrange(0, 255)
      self.green = random.randrange(0, 255)
      self.blue = random.randrange(0, 255)
      self.radius = random.randrange(0, 30)
      return True
#end class pellet++++++++++++++++++++++++++++++++++++
#tailSeg class++++++++++++++++++++++++++++++++++++++++++++++++++
class TailSeg:
  def __init__(self, xpos, ypos):
    self.xpos = xpos
    self.ypos = ypos
  def update(self, xpos, ypos):
    self.xpos = xpos
    self.ypos = ypos
  def draw(self):
    pygame.draw.circle(screen, (200, 0, 200), (self.xpos, self.ypos), 12)
  def collide(self, x, y):
    if math.sqrt((x-self.xpos)*(x-self.xpos)+(y-self.ypos)*(y-self.ypos)) < 6:
      return True
#tailSeg class end+++++++++++++++++++++++++++++++++++++++++++++++===
pelletBag = list()#create a list of data structures
tail = list()
tail2 = list()
#push 10 pellets into the list 
for i in range(10):
  pelletBag.append(pellet(random.randrange(0, 400), random.randrange(0, 400), random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 30)))
#game loop ###################################################
while not doExit:

#event/input section------------------------------------------
  clock.tick(60)

  for event in pygame.event.get():#grabs events
    if event.type == pygame.QUIT:#lets you exit from game screen
      doExit = True
    if event.type == pygame.MOUSEMOTION:
      mousePos = event.pos

      if mousePos[0]>xPos:
        Vx = 1
      else:
        Vx = -1
      if mousePos[1]>yPos:
        Vy = 1
      else:
        Vy = -1
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
      xPos2 -= 1
    if keys[pygame.K_RIGHT]:
      xPos2 += 1
    if keys[pygame.K_UP]:
      yPos2 -= 1
    if keys[pygame.K_DOWN]:
      yPos2 += 1

#physics section----------------------------------------------
  #make nodes follow
  counter += 1 #update counter
  if counter == 20: #create a delay so the segments follow behind
    counter = 0 #reset counter every 20 ticks
    oldX = xPos #hold onto players position from 20 ticks ago
    oldY = yPos
    oldX2 = xPos2
    oldY2 = yPos2

    if (len(tail)>2): #don't push numbers if there are no nodes yet
      for i in range(len(tail)): #loop for each slot in list
        #start in LAST position, push the *second to last* into it, repeat till at beginning
        tail[len(tail)-i-1].xpos = tail[len(tail)-i-2].xpos
        tail[len(tail)-i-1].ypos = tail[len(tail)-i-2].ypos
    if (len(tail2)>2):
      for i in range(len(tail2)):
        tail2[len(tail2)-i-1].xpos = tail2[len(tail2)-i-2].xpos
        tail2[len(tail2)-i-1].ypos = tail2[len(tail2)-i-2].ypos
    if (len(tail)>0): #If you have at least one segment, push old head position into that 
      tail[0].update(oldX, oldY) #push head position to first position on list
    if (len(tail2)>0):
      tail2[0].update(oldX2, oldY2)
  #update circle position
  xPos += Vx
  yPos += Vy

  #colliion
  for i in range(10):
    if pelletBag[i].collide(xPos, yPos) == True:
      tail.append(TailSeg(oldX, oldY))
    if pelletBag[i].collide(xPos2, yPos2) == True:
      tail2.append(TailSeg(oldX2, oldY2))

  if xPos < 10 or xPos > 390 or yPos < 10 or yPos > 390:
    doExit = True
  if xPos2 < 10 or xPos2 > 390 or yPos2 < 10 or yPos2 > 390:
    doExit = True

  #check if p1 has hit p2's tail
  for i in range(len(tail2)):
    if tail2[i].collide(xPos, yPos) == True:
      print("p1 has hit p2's tail!!")
      doExit = True
  for i in range(len(tail)):
    if tail[i].collide(xPos2, yPos2) == True:
      print("p2 has hit p1's tail!!")
      doExit = True
#render section-----------------------------------------------
  screen.fill((255,255,255))

  pygame.draw.circle(screen, (200,0,200), (xPos, yPos), 12)
  pygame.draw.circle(screen, (200,10,100), (xPos2, yPos2), 12)
  
  for i in range(10):
    pelletBag[i].draw()
  
  for i in range(len(tail)):
    tail[i].draw()
  for i in range(len(tail2)):
    tail2[i].draw()

  pygame.display.flip()

#end game loop################################################

pygame.quit()
