import pygame
import random
import decimal
import math
import time
import os
pygame.init()

width = 1466
height = 768

size = (width, height)

FPS = 120

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
myfont = pygame.font.SysFont('Comic Sans MS', 30)

angle = []
angle.append(10)
angle.append(24)
angle.append(44)
angle.append(73)
angle.append(73)
angle.append(44)
angle.append(24)
angle.append(10)

ballSpeed = 1

clicked = False

screen = pygame.display.set_mode(size)

pygame.display.set_caption("Rotating Factory Escape")

Clock = pygame.time.Clock()

homeScreenMode = [True, False]

global scoreModifier
global score
score = 0
scoreModifier = 50
global highscore
highscore = 0

global playerNum
playerNum = 0
pickPlayer = [False, True]

speed1 = 10
speed2 = 20
speed = 0

cheatMenu = False

playerSpeed = 8
beforeSpeed = playerSpeed

lost = False

doorHeight = height/2 - 100

global levelNum
levelNum = 0

exit = False

pygame.mixer.init()

game_folder = os.path.dirname("../../img")
MySpritesFolder = os.path.join(game_folder, "img")
gear = ["gear.png", "gear1.png", "gear2.png", "gear3.png", "gear4.png", "gear5.png", "gear6.png"]
back = ["back1.jpg","back2.jpg","back3.jpg","back4.jpg","back5.jpg","back6.jpg","back7.jpg","back8.jpg",\
    "back9.jpg","back10.jpg","back11.jpg","back12.jpg","back13.jpg","back14.jpg","back15.jpg"]
players = ["player.png", "player1.png", "player2.png", "player3.png", "player4.png", "player5.png", "player6.png","player7.png", "player8.png", "player9.png"]

#---------------------------------HOMESCREEN CLASS-----------------------HOMESCREEN CLASS----------------------------------
class homeScreen(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.background = pygame.image.load(os.path.join(MySpritesFolder, "homeGear.jpg")).convert()
        self.background_rect = self.background.get_rect()
        screen.blit(self.background, self.background_rect)
        self.playButton = pygame.image.load(os.path.join(MySpritesFolder, "play_200x100.png")).convert()
        self.play_rect = self.playButton.get_rect()
        self.play_rect.centerx = width / 2
        self.play_rect.centery = height / 2
        self.playButton.set_colorkey(WHITE)
        screen.blit(self.playButton, self.play_rect)
        self.title = pygame.image.load(os.path.join(MySpritesFolder, "title.png")).convert()
        self.title_rect = self.title.get_rect()
        self.title_rect.centerx = width / 2
        self.title.set_colorkey(WHITE)
        screen.blit(self.title, self.title_rect)

    def update(self):
        self.keystate = pygame.key.get_pressed()
        if self.keystate[pygame.K_RETURN] or self.keystate[pygame.K_SPACE]:
            pickPlayer.remove(False)
            

    def choosePlayer(self):
        self.image = pygame.Surface((width/len(players) * len(players) - width/len(players) + 80, (height/2)/len(players) * len(players) - (height/2)/len(players) -80))
        self.image.fill(WHITE)
        #self.rect = self.image.get_rect
        #self.rect.left = width/len(players)
        #self.rect.top = height/2 + 150
        screen.blit(self.image, (width/len(players)- 100, height/2 + 80))
        dis = width/(len(players)+0)
        for g in range(0,len(players)):
            self.textSurface = myfont.render("Player " + str((g+1)), False, BLACK)
            screen.blit(self.textSurface,(dis,(height/2) + 100))
            self.image = pygame.image.load(os.path.join(MySpritesFolder, players[g])).convert()
            self.image.set_colorkey(WHITE)
            self.rect = self.image.get_rect()
            self.rect.top = (height / 2) + 150
            self.rect.x = dis
            screen.blit(self.image, self.rect)
            dis += width/(len(players)+0)

        self.keystate = pygame.key.get_pressed()
        keys = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0]
        for com in range(len(keys)):
            if self.keystate[keys[com]]:
                global playerNum
                playerNum = com
                print(str(playerNum))
                homeScreenMode.remove(True)
                time.sleep(0.5)
                Level.nextLevel()

            


#---------------------------------PLAYER CLASS-----------------------PLAYER CLASS----------------------------------
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #ALL IMAGES ARE 120x146 pixels or 120x114 or 120x150
        self.image = pygame.image.load(os.path.join(MySpritesFolder, players[playerNum])).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.top = height / 2
        self.rect.left = width - 50


    def update(self):
        self.speedx = 0
        self.speedy = 0
        self.keystate = pygame.key.get_pressed()
        global playerSpeed
        keys = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_a, pygame.K_d, pygame.K_UP, pygame.K_DOWN, pygame.K_w, pygame.K_s]
        for a in range(len(keys)):
            if self.keystate[keys[a]] and a < len(keys)/2:
                if (a % 2) == 0:
                    self.speedx = playerSpeed * -1
                if (a % 2) == 1:
                    self.speedx = playerSpeed
            if self.keystate[keys[a]] and a >= len(keys)/2:
                if (a % 2) == 0:
                    self.speedy = playerSpeed * -1
                if (a % 2) == 1:
                    self.speedy = playerSpeed
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > width:
            self.rect.right = width 
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > height:
            self.rect.bottom = height        

 

#---------------------------------BALL CLASS-----------------------BALL CLASS----------------------------------
class Ball(pygame.sprite.Sprite):
    def __init__(self, speed):
        pygame.sprite.Sprite.__init__(self)
        num = random.randrange(0, len(gear))
        self.image_orig = pygame.image.load(os.path.join(MySpritesFolder, gear[num])).convert()
        self.image_orig.set_colorkey(WHITE)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.cirRadius = random.randint(70, 400)
        global scoreModifier
        for d in range(0, int(len(gear)/2)):
            if num == d:
                scoreModifier += 25
                print("Score Big Modified")
        for d in range(int(len(gear)/2), len(gear)):
            if num == d:
                scoreModifier += 15
                print("Score Small Modified")
        self.smoothness = random.randint(3, 20)
        if self.smoothness > 8 and self.smoothness < 11:
            scoreModifier += 18
        if self.smoothness > 11:
            scoreModifier += 28
        self.rect_x = []
        self.rect_y = []
        self.change_x = []
        self.change_y = []
        self.turn = 1
        self.cp_x = random.randint(50, width / 2)
        self.cp_y = random.randint(10, height - 10)
        print("Check 1")
        for count in range(0, 4):
            for z in range(0,4):
                if self.turn > 0 and self.turn <= 4:
                    self.rect_x.append(self.cp_x - (math.cos(math.radians(angle[z])) * self.cirRadius))
                    self.rect_y.append(self.cp_y + (math.sin(math.radians(angle[z])) * self.cirRadius))
                if self.turn > 4 and self.turn <= 8:
                    self.rect_x.append(self.cp_x + (math.cos(math.radians(angle[z+4])) * self.cirRadius))
                    self.rect_y.append(self.cp_y + (math.sin(math.radians(angle[z+4])) * self.cirRadius))
                if self.turn > 8 and self.turn <= 12:
                    self.rect_x.append(self.cp_x + (math.cos(math.radians(angle[z])) * self.cirRadius))
                    self.rect_y.append(self.cp_y - (math.sin(math.radians(angle[z])) * self.cirRadius))
                if self.turn > 12 and self.turn <= 16:
                    self.rect_x.append(self.cp_x - (math.cos(math.radians(angle[z+4])) * self.cirRadius))
                    self.rect_y.append(self.cp_y - (math.sin(math.radians(angle[z+4])) * self.cirRadius))
                self.turn += 1
        self.rect_x.append(self.rect_x[0])
        self.rect_y.append(self.rect_y[0])
        print("Check 2")

        for c in range(0, 16):
            self.change_x.append(((self.rect_x[c+1] - self.rect_x[c]) / self.smoothness) * speed) 
            self.change_y.append(((self.rect_y[c+1] - self.rect_y[c]) / self.smoothness) * speed) 
            print(str(speed))
        
        print("Check 3")
        self.gear_x = self.rect_x[0]
        self.gear_y = self.rect_y[0]
        self.number = 0

        #Rotation Stuff
        self.rot = 0
        self.rot_speed = random.randrange(-30, 30)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50: #In milliseconds
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        global ballSpeed
        self.gear_x += self.change_x[self.number] / ballSpeed
        self.gear_y += self.change_y[self.number] / ballSpeed
        self.rect.x = self.gear_x
        self.rect.y = self.gear_y
        if self.number <= 4 and self.number >= 0:
            if self.gear_x >= self.rect_x[self.number + 1] and self.gear_y >= self.rect_y[self.number + 1]:
                self.number += 1
        if self.number <= 9 and self.number > 4:
            if self.gear_x >= self.rect_x[self.number + 1] and self.gear_y <= self.rect_y[self.number + 1]:
                self.number += 1
        if self.number <= 13 and self.number > 9:
            if self.gear_x <= self.rect_x[self.number + 1] and self.gear_y <= self.rect_y[self.number + 1]:
                self.number += 1
        if self.number <= 16 and self.number > 13:
            if self.gear_x <= self.rect_x[self.number + 1] and self.gear_y >= self.rect_y[self.number + 1]:
                self.number += 1
        if self.number >= 16:
            self.number = 0
            self.gear_x = self.rect_x[0]
            self.gear_y = self.rect_y[0]
        #print("UPDATE")


#---------------------------------LEVEL CLASS-----------------------LEVEL CLASS----------------------------------
class Level(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        
    def nextLevel(self):
        
        global levelNum
        levelNum += 1
        print("Done" + str(levelNum))
        global speed1
        global speed2
        speed1 += 10
        speed2 += 10
        print(speed1)
        print(speed2)

        global playerSpeed
        if levelNum > 11:
            playerSpeed += 0.5
        global backNum
        backNum = random.randrange(0, len(back))
        
        #background_rect = self.background.get_rect()
        global clicked
        speed = float(decimal.Decimal(random.randrange(speed1, speed2))/100)

        global scoreModifier
        global score
        print("Speed " + str(speed))
        if speed > 0.4:
            scoreModifier += int(45  * speed)
            print("Speed Modifier " + str(int(45*speed)))
        score += scoreModifier
        b = Ball(speed)
        all_sprites.add(b)
        balls.add(b)
       
        Player.__init__()

    def nextBack(self):
        self.background = pygame.image.load(os.path.join(MySpritesFolder, back[0])).convert_alpha()
        self.back_rect = self.background.get_rect()
        screen.blit(self.background, self.back_rect)
        



    #def nextLevel(self):
        
#---------------------------------LEVEL DOOR CLASS-----------------------LEVEL DOOR CLASS----------------------------------       
class levelDoor(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(MySpritesFolder, "levelDoor.jpg")).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.top = doorHeight
        self.rect.x = 100
        self.radius = int(self.rect.width * .85 / 2)
        textSurface = myfont.render("Level " + str(levelNum), False, BLACK)
        screen.blit(textSurface,(width/2 - 50,height / 100))
        
        #screen.blit(self.doorLevel, self.doorLevelRect)
        #all_sprites.add(levelDoor())

#---------------------------------GAME OVER CLASS-----------------------GAME OVER CLASS----------------------------------
class gameOver(pygame.sprite.Sprite):
    def __init__(self):
        global levelNum
        self.textSurface = myfont.render("Game Over", False, BLACK)
        screen.blit(self.textSurface,(width/2,height/2))
        self.textSurface = myfont.render("You made it to level " + str(levelNum), False, BLACK)
        screen.blit(self.textSurface,(width/2,height/2 + 100))
        self.textSurface = myfont.render("Press R to Retry", False, BLACK)
        screen.blit(self.textSurface,(width/2,height/2 + 200))
        #global levelNum
        global speed
        global speed1
        global speed2
        global playerNum
        global playerSpeed
        global beforeSpeed
        global gear
        global ballSpeed
        global score
        global scoreModifier
        score = 0
        scoreModifier = 50
        ballSpeed = 1
        playerSpeed = beforeSpeed
        levelNum = 0
        speed = 0
        speed1 = 10
        speed2 = 20
        gear = ["gear.png", "gear1.png", "gear2.png", "gear3.png", "gear4.png", "gear5.png", "gear6.png"]
        all_sprites.remove(balls)
        balls.remove(balls)
        playerNum = 0


#---------------------------------HIGH SCORE CLASS-----------------------HIGH SCORE CLASS----------------------------------
class highScore(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        global highscore
        self.textSurface = myfont.render("HighScore: " + str(highscore), False, BLACK)
        screen.blit(self.textSurface,(width/2 + (width/5), height/100))
        global score
        self.textSurface = myfont.render("Score: " + str(score), False, BLACK)
        screen.blit(self.textSurface,(width/2 - ((width/5)+100), height/100))
    def update(self):
        global highscore
        global levelNum
        if score > highscore:
            highscore += 1

 #---------------------------------CHEATS CLASS-----------------------CHEATS CLASS----------------------------------       
class cheats(pygame.sprite.Sprite):
    
    def update(self):
        pygame.sprite.Sprite.update(self)
        self.keystate = pygame.key.get_pressed()
        global clicked
        global playerSpeed
        if self.keystate[pygame.K_LCTRL] and self.keystate[pygame.K_l] and clicked==False:
            Level.nextLevel()
            time.sleep(0.150)
        if self.keystate[pygame.K_LCTRL] and self.keystate[pygame.K_c]:
            all_sprites.remove(balls)
            balls.remove(balls)
        if self.keystate[pygame.K_LCTRL] and self.keystate[pygame.K_e]:
            playerSpeed += 0.5
        if self.keystate[pygame.K_LCTRL] and self.keystate[pygame.K_q]:
            playerSpeed -= 0.5
        if self.keystate[pygame.K_LCTRL] and self.keystate[pygame.K_r]:
            playerSpeed = beforeSpeed
        if self.keystate[pygame.K_LCTRL] and self.keystate[pygame.K_t]:
            global gear
            gear = ["gear5.png", "gear6.png"]
            all_sprites.remove(balls)
            amtBalls = len(balls)
            balls.remove(balls)
            global speed1
            global speed2
            global speed
            global b
            for ba in range(amtBalls):
                speed = float(decimal.Decimal(random.randrange(speed1, speed2))/100)
                b = Ball(speed)
                all_sprites.add(b)
                balls.add(b)
        if self.keystate[pygame.K_LCTRL] and self.keystate[pygame.K_f]:
            global ballSpeed
            ballSpeed += 0.2
        if self.keystate[pygame.K_LCTRL] and self.keystate[pygame.K_g]:
           # global ballSpeed
            ballSpeed -= 0.05
            if ballSpeed <= 0:
                ballSpeed = 1
        if self.keystate[pygame.K_LCTRL] and self.keystate[pygame.K_h]:
           # global ballSpeed
            ballSpeed = 1
        if self.keystate[pygame.K_LCTRL] and self.keystate[pygame.K_m]:
            self.textSurface = myfont.render("Cheat Menu:", False, BLACK)
            screen.blit(self.textSurface,(10,0))
            self.textSurface = myfont.render("CTRL + L: Next Level", False, BLACK)
            screen.blit(self.textSurface,(10,50))
            self.textSurface = myfont.render("CTRL + C: Clear Gears", False, BLACK)
            screen.blit(self.textSurface,(10,100))
            self.textSurface = myfont.render("CTRL + E/Q/R: Increase/Decrease/Default Player Speed", False, BLACK)
            screen.blit(self.textSurface,(10,150))
            self.textSurface = myfont.render("CTRL + T: All Gears Small", False, BLACK)
            screen.blit(self.textSurface,(10,200))
            self.textSurface = myfont.render("CTRL + F/G/H: Decrease/Increase/Default Gear Speed", False, BLACK)
            screen.blit(self.textSurface,(10,250))
            

   






all_sprites = pygame.sprite.Group()
#balls = pygame.sprite.Group()
homescreen = pygame.sprite.Group()
highscores = pygame.sprite.Group()
balls = pygame.sprite.Group()
levels = pygame.sprite.Group()
levelDoors = pygame.sprite.Group()
l = levelDoor()
levelDoors.add(l)
all_sprites.add(l)
Player = Player()
Level = Level()
gameOver = gameOver()
all_sprites.add(Player)
h = highScore()
c = cheats()
#all_sprites.add(c)
#all_sprites.add(h)
##all_sprites.add(gameOver)



running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
             if event.key == pygame.K_ESCAPE:
                running = False


    if homeScreenMode[0]:
        if pickPlayer[0]:
            homescreen.choosePlayer()
        
        else:
            homeScreen()
            homescreen = homeScreen()
            homescreen.update()
        
    if homeScreenMode[0] == False:
        screen.fill(WHITE)
        #Level.nextBack()
        l.__init__()
        h.__init__()
        h.update()
        all_sprites.update()
        c.update()
        
        

        hits = pygame.sprite.spritecollide(Player, balls, False, pygame.sprite.collide_circle)
        if hits:
            gameOver.__init__()
            time.sleep(2)
            homeScreenMode = [True, False]
            pickPlayer =[False, True]
            #running = False
   

        hitDoor = pygame.sprite.spritecollide(Player, levelDoors, pygame.sprite.collide_circle, pygame.sprite.collide_circle)
        if hitDoor:
            Level.nextLevel()
            
        all_sprites.draw(screen)



        

    Clock.tick(FPS)

    pygame.display.flip()

pygame.quit()
