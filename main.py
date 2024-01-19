
# Modification date: Tue May  3 17:22:14 2022

# Production date: Sun Sep  3 15:43:43 2023

import pygame
from random import randint, choice
from math import sqrt


ww = 600
wh = 600
win = pygame.display.set_mode((ww, wh + 100))
pygame.init()


"""
class Spawn:
    def __init__(self, x, y, w, h, unit, cooldown, base):
        self.x, self.y, self.w, self.h, self.unit, self.cooldown, self.pressed = x, y, w, h, unit, cooldown, base, False
    
    def draw(self, win):
        if self.pressed:

        if self.unit == "worker":

"""







class Button:
    def __init__(self, x, y, w, h, text, textColour, buttonColour, task):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text
        self.textColour = textColour
        self.buttonColour = buttonColour
        self.task = task
        self.pressed = False
        
    def draw(self, win):
        pygame.draw.rect(win, self.buttonColour, pygame.Rect(self.x, self.y, self.w, self.h))
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        textsurface = myfont.render(self.text, False, self.textColour)
        
        pygame.draw.rect(win, (120, 160, 200), pygame.Rect(self.x, self.y, self.w, self.h), 2)
        win.blit(textsurface, (self.x + self.w//7, self.y + self.h//3))
        return
    def check_pressing(self, da_point):
        
        if da_point[0] > self.x and da_point[0] < self.x + self.w:
            #print("got first ", self.task)
            if da_point[1] > self.y and da_point[1] < self.y + self.h:
                #print("got second", self.task)
                self.pressed = True
                return
        self.pressed = False
            
        return
    def fpressed(self, humans):
        if self.task == "attack":
            for human in humans:
                if human.team == "blue" and human.job == "soldier":
                    human.strategy = "attack"
        if self.task == "defend":
            for human in humans:
                if human.team == "blue" and human.job == "soldier":
                    human.strategy = "defend"
        if self.task == "start mining":
            for human in humans:
                if human.team == "blue" and human.job == "worker":
                    human.strategy = "start mining"
        if self.task == "stop mining":
            for human in humans:
                if human.team == "blue" and human.job == "worker":
                    human.strategy = "stop mining"




class Ressource:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.job = "ressource"
        self.team = None

    def draw(self, win):
        pygame.draw.rect(win, (255,215,0), pygame.Rect(self.x, self.y, self.w, self.h))






class Base:
    def __init__(self, x, y, w, h, team):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.team = team
        self.hitbox = (self.x - 12, self.y - 12, self.w + 24, self.h + 24)
        self.job = "base"
        self.counter = 0
        if self.team == "blue":
            self.ressource = 0
        else:
            self.ressource = 0
        self.spawncost = 100

        self.hp = 30000
        self.maxhp = 30000


        self.skin = (136, 140, 141)
        if self.team == "blue":
            self.tc = (0, 0, 255)
        elif self.team == "red":
            self.tc = (255, 0, 0)
    

    def spawn(self, humans):#gonna change?
        #print(self.team, self.counter)
        self.ressource += 1
        if self.maxhp >= self.hp + 1:
            self.hp += 1
        if self.ressource >= self.spawncost:
            da_choice = choice(["soldier", "worker"])
            if self.team == "blue":
                if da_choice == "soldier":
                    strat = "defend"
                elif da_choice == "worker":
                    strat = "stop mining"
            else:
                if da_choice == "soldier":
                    strat = "attack"
                elif da_choice == "worker":
                    strat = "start mining"
            humans.append(Human(self.x + self.w//2, self.y + self.h//2, self.team, da_choice, strat))
            self.ressource -= self.spawncost




    def draw(self, win, humans):
        workerc = 0
        soldierc = 0
        for human in humans:
            if human.team == self.team:
                if human.job == "soldier":
                    soldierc += 1
                elif human.job == "worker":
                    workerc += 1


        if self.hp == 0:
            self.hp = -1
        self.hc = [int(abs(((self.maxhp / self.hp) * 255) - 255)), int(abs((self.hp / self.maxhp) * 255)), 0]
        for colour in self.hc:
            if colour > 254:
                colour = 255
        if self.hc[0] > 255:
            self.hc[0] = 255
        self.hc = tuple(self.hc)

        self.hpbl = int(abs(self.hp / self.maxhp) * self.w//2)

        pygame.draw.rect(win, self.skin, pygame.Rect(self.x, self.y, self.w, self.h))

        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        textsurface = myfont.render(str(self.ressource), False, self.tc)
        win.blit(textsurface, (self.x + self.w//4, self.y + self.h//2 - 50))
        myfont = pygame.font.SysFont('Comic Sans MS', 15)
        textsurface = myfont.render(f"W: {workerc},  S: {soldierc}", False, self.tc)
        win.blit(textsurface, (self.x + 20, self.y + self.h - 30))

        if self.team == "red":
            pygame.draw.rect(win, (255, 0, 0), pygame.Rect(self.x + 3, self.y + 3, self.w - 4, self.h - 4), 2)
        elif self.team == "blue":
            pygame.draw.rect(win, (0, 0, 255), pygame.Rect(self.x + 3, self.y + 3, self.w - 4, self.h - 4), 2)
        pygame.draw.rect(win, (0, 0, 0), pygame.Rect(self.x + self.w//4, self.y + self.h//2, self.w//2, 16))
        pygame.draw.rect(win, self.hc, pygame.Rect(self.x + self.w//4 + 2, self.y + self.h//2 + 2, self.hpbl - 4, 12))
        #pygame.draw.rect(win, (255, 255, 255), pygame.Rect(self.hitbox), 2)

        self.hc = list(self.hc)



class Human:
    def __init__(self, x, y, team, job, strategy):
        #props(?)
        self.x = x
        self.y = y
        self.w = 16
        self.h = 16
        self.team = team
        self.job = job
        if self.job == "worker":
            self.inventory = 0
            self.last_res = None
        self.strategy = strategy
        

        #colours
        if self.team == "blue":
            self.tc = (0, 0, 255)
        elif self.team == "red":
            self.tc = (255, 0, 0)
        self.hc = [0, 255, 0]
        if self.job != "base":
            self.color = randint(0, 150)
            self.skin = (45 + self.color, 34 + self.color, 30 + self.color)
            

        #damage and health
        if self.job == "worker":
            self.hp = 150
            self.maxhp = 150
            self.dmg = 5
        elif self.job == "soldier":
            self.hp = 300
            self.maxhp = 300
            self.dmg = 15


        #movement
        if self.job == "worker":
            self.vel = 5
        elif self.job == "soldier":
            self.vel = 7
        self.walkvel = self.vel - 2
        self.direction = "right"
        self.tdir = "right"
        self.directions = ["right", "left", "up", "down"]
        self.cd = True
        self.target = None
    
    
    def distance(self, sh):
        return sqrt(((sh.x + sh.w//2) - (self.x + self.w//2)) ** 2 + ((sh.y + sh.h//2) - (self.y + self.h//2)) ** 2)
    
    def distance_of_2(self, fh, sh):
        return sqrt(((sh.x + sh.w//2) - (fh.x + fh.w//2)) ** 2 + ((sh.y + sh.h//2) - (fh.y + fh.h//2)) ** 2)

    
    def ctarget(self, humans, ressources, bases):
        #self.allies = []
        self.enemies = []
        self.ally_bases = []
        self.enemy_bases = []
        self.ressources = []
        for human in humans:
            #if human.team == self.team:
                #self.allies.append([self.distance(human), human])
            if human.team != self.team and self.distance(human) < 256:
                self.enemies.append([self.distance(human), human])
        for base in bases:
            if base.team == self.team:
                self.ally_bases.append([self.distance(base), base])
            elif base.team != self.team:
                self.enemy_bases.append([self.distance(base), base])
        
        for ressource in ressources:
            if self.distance(ressource) < 256:
                self.ressources.append([self.distance(ressource), ressource])
        


        #print(len(self.allies), len(self.ally_bases), len(self.enemy_bases), len(self.enemies))
        if self.job == "soldier":
            if self.strategy == "attack":
                if len(self.enemies) > 0:
                    closest = 0
                    for couple in range(len(self.enemies)):
                        if self.enemies[closest][0] > self.enemies[couple][0]:
                            closest = couple
                    self.target = self.enemies[closest][1]
                    return
                elif len(self.enemy_bases) > 0:
                    closest = 0
                    for couple in range(len(self.enemy_bases)):
                        if self.enemy_bases[closest][0] > self.enemy_bases[couple][0]:
                            closest = couple
                    self.target = self.enemy_bases[closest][1]
                    #print(self.target.job)
                    return
            if self.strategy == "defend":
                if self.ally_bases:
                    closest = 0
                    for couple in range(len(self.ally_bases)):
                        if self.ally_bases[closest][0] > self.ally_bases[couple][0]:
                            closest = couple
                    self.target = self.ally_bases[closest][1]
                    
                    #print(self.target.job)
                    if self.enemies:
                        self.enemy_and_base = []
                        for enemy in self.enemies:
                            for enemy in self.enemies:
                                if self.distance_of_2(enemy[1], self.target) < 256:
                                    self.enemy_and_base.append([enemy[1], self.distance_of_2(enemy[1], self.target)])
                        if self.enemy_and_base:
                            closest2 = 0
                            for couple in range(len(self.enemy_and_base)):
                                if self.enemy_and_base[closest2][1] > self.enemy_and_base[couple][1]:
                                    closest2 = couple
                            self.target = self.enemy_and_base[closest2][0]

                    return
                
                
            self.target = None
            return

        elif self.job == "worker":
            if self.strategy == "start mining":
                if self.inventory < 50:
                    if len(self.ressources) > 0:
                        closest = 0
                        for couple in range(len(self.ressources)):
                            if self.ressources[closest][0] > self.ressources[couple][0]:
                                closest = couple
                        self.target = self.ressources[closest][1]
                        self.last_res = self.ressources[closest][1]
                        return
                    else:
                        self.target = None
                        return
                else:
                    if len(self.ally_bases) > 0:
                        closest = 0
                        for couple in range(len(self.ally_bases)):
                            if self.ally_bases[closest][0] > self.ally_bases[couple][0]:
                                closest = couple
                        self.target = self.ally_bases[closest][1]
                    else:
                        bases.append(Base(self.x, self.y, 128, 128, self.team))
            if self.strategy == "stop mining":
                if len(self.ally_bases) > 0:
                    closest = 0
                    for couple in range(len(self.ally_bases)):
                        if self.ally_bases[closest][0] > self.ally_bases[couple][0]:
                            closest = couple
                        self.target = self.ally_bases[closest][1]
                else:
                    bases.append(Base(self.x, self.y, 128, 128, self.team))
                
        
    
    def mover(self):
        if self.ally_bases:
            for base in self.ally_bases:
                if base[0] < 192:
                    if self.hp + 1 <= self.maxhp: 
                        self.hp += 1
        #print(self.target)
        if not self.target:
            #print("wandering")
            if self.direction == "right" and self.x < ww - 30:
                self.x += self.walkvel
            elif self.direction == "right":
                self.cd = True
            if self.direction == "left" and self.x > 30:
                self.x -= self.walkvel
            elif self.direction == "left":
                self.cd = True
            if self.direction == "up" and self.y > 30:
                self.y -= self.walkvel
            elif self.direction == "up":
                self.cd = True
            if self.direction == "down" and self.y < wh - 30:
                self.y += self.walkvel
            elif self.direction == "down":
                self.cd = True

        if self.x < 0 or self.x > ww or self.y < 0 or self.y > wh:
            self.x = randint(0, ww)
            self.y = randint(0, wh)
        else:
            if self.target and self.distance(self.target) > 32:
                if self.target.job == "base":
                    if self.target.x >= self.x:
                        self.x += self.vel
                        self.direction = "right"
                        return
                    if self.target.x + self.target.w <= self.x:
                        self.x -= self.vel
                        self.direction = "left"
                        return
                    if self.target.y >= self.y + self.h:
                        self.y += self.vel
                        self.direction = "down"
                        return
                    if self.target.y + self.target.h <= self.y:
                        self.y -= self.vel
                        self.direction = "up"
                        return

                    #print(f"({self.target.hitbox[0]} < {self.x + self.w*2} and {self.target.hitbox[0] + self.target.hitbox[2]} > {self.x}) and ({self.target.hitbox[1]} < {self.y + self.h*2} and {self.target.hitbox[1] + self.target.hitbox[3]} > {self.y})")
                    #print((self.target.hitbox[0] < self.x + self.w*2 and self.target.hitbox[0] + self.target.hitbox[2] > self.x) and (self.target.hitbox[1] < self.y + self.h*2 and self.target.hitbox[1] + self.target.hitbox[3] > self.y))
                    if self.target.team != self.team:
                        if (self.target.hitbox[0] < self.x + self.w*2 and self.target.hitbox[0] + self.target.hitbox[2] > self.x) and (self.target.hitbox[1] < self.y + self.h*2 and self.target.hitbox[1] + self.target.hitbox[3] > self.y):
                            self.target.hp -= self.dmg
                            #return
                    else:
                        if self.target.job == "base" and self.job == "worker" and self.inventory > 0:
                            self.target.ressource += self.inventory
                            
                            if self.target.maxhp >= self.target.hp + 50:
                                self.target.hp += self.inventory
                            else:
                                self.target.hp = self.target.maxhp
                            self.inventory = 0

                        
                else:
                    if self.target.x >= self.x + self.w//2:
                        self.x += self.vel
                        self.direction = "right"
                        return
                    if self.target.x + self.w <= self.x + self.w//2:
                        self.x -= self.vel
                        self.direction = "left"
                        return
                    if self.target.y >= self.y + self.h//2:
                        self.y += self.vel
                        self.direction = "down"
                        return
                    if self.target.y + self.h <= self.y + self.h//2:
                        self.y -= self.vel
                        self.direction = "up"
                        return
            
            elif self.target and self.distance(self.target) < 32:
                if self.target.team:
                    if self.target.team != self.team:
                        self.target.hp -= self.dmg
                        #pygame.draw.rect(win, (self.dmg * 20, 100, 100), pygame.Rect(self.target.x, self.target.y - 8, 8, 8))
                        return #attack
                else:
                    self.inventory += 1
        if randint(0, 150) == 1 or self.cd:
            self.tdir = self.direction
            self.directions.remove(self.direction)
            self.direction = choice(self.directions)
            self.directions.append(self.tdir)
            self.tdir = self.direction
            self.cd = False
        
            
    
    
    def draw(self, win):
        if self.hp == 0:
            self.hp = -1
        self.hc = [int(abs(((self.maxhp / self.hp) * 255) - 255)), int(abs((self.hp / self.maxhp) * 255)), 0]
        for colour in self.hc:
            if colour > 254:
                colour = 255
        if self.hc[0] > 255:
            self.hc[0] = 255
        self.hc = tuple(self.hc)

        if self.job == "soldier" or self.job == "worker":
            self.hpbl = int(abs(self.hp / self.maxhp) * 24)
        else:
            self.hpbl = int(abs(self.hp / self.maxhp) * 128)
        

        if self.direction == "right" or self.direction == "left":
            #pygame.draw.rect(win, (30, 20, 170), pygame.Rect(self.x + 4, self.y - 8, 8, 8))
            #pygame.draw.rect(win, (30, 20, 170), pygame.Rect(self.x + 4, self.y + 16, 8, 8))
            pygame.draw.rect(win, self.tc, pygame.Rect(self.x + 4, self.y - 8, 8, 8))
            pygame.draw.rect(win, self.tc, pygame.Rect(self.x + 4, self.y + 16, 8, 8))
            pygame.draw.rect(win, self.skin, pygame.Rect(self.x, self.y, 16, 16))
            #print(self.hc)
            pygame.draw.rect(win, (0, 0, 0), pygame.Rect(self.x - 9, self.y - 9, 26, 6))
            try:
                pygame.draw.rect(win, self.hc, pygame.Rect(self.x - 8, self.y - 8, self.hpbl, 4))
            except:
                print(f"health error lmao: {self.hc}")
            if self.job == "worker":
                pygame.draw.line(win, (102, 51, 0), (self.x + 8, self.y), (self.x + 8, self.y + 10))
                pygame.draw.line(win, (142, 142, 142), (self.x + 1, self.y + 1), (self.x + 15, self.y + 1))
            elif self.job == "soldier":
                pygame.draw.line(win, (102, 51, 0), (self.x + 2, self.y + 10), (self.x + 6, self.y + 14))
                pygame.draw.line(win, (142, 142, 142), (self.x, self.y + 14), (self.x + 14, self.y))
                

            
        if self.direction == "up" or self.direction == "down":
            #pygame.draw.rect(win, (30, 20, 170), pygame.Rect(self.x - 8, self.y + 4, 8, 8))
            #pygame.draw.rect(win, (30, 20, 170), pygame.Rect(self.x + 16, self.y + 4, 8, 8))
            pygame.draw.rect(win, self.tc, pygame.Rect(self.x - 8, self.y + 4, 8, 8))
            pygame.draw.rect(win, self.tc, pygame.Rect(self.x + 16, self.y + 4, 8, 8))
            pygame.draw.rect(win, self.skin, pygame.Rect(self.x, self.y, 16, 16))
            pygame.draw.rect(win, (0, 0, 0), pygame.Rect(self.x - 9, self.y - 9, 26, 6))
            try:
                pygame.draw.rect(win, self.hc, pygame.Rect(self.x - 8, self.y - 8, self.hpbl, 4))
            except:
                print(f"health error lmao: {self.hc}")
            if self.job == "worker":
                pygame.draw.line(win, (102, 51, 0), (self.x + 8, self.y), (self.x + 8, self.y + 10))
                pygame.draw.line(win, (142, 142, 142), (self.x + 1, self.y + 1), (self.x + 15, self.y + 1))
            elif self.job == "soldier":
                pygame.draw.line(win, (102, 51, 0), (self.x + 2, self.y + 10), (self.x + 6, self.y + 14))
                pygame.draw.line(win, (142, 142, 142), (self.x, self.y + 14), (self.x + 14, self.y))

        
        self.hc = list(self.hc)

    



humans = []
ressources = []
ressources.append(Ressource(ww - 32, 0, 32, 32))
#ressources.append(Ressource(ww//2 - 16, 0, 32, 32))
#ressources.append(Ressource(ww//2 - 16, wh//4, 32, 32))
ressources.append(Ressource(ww//2 - 16, wh//2 - 16, 32, 32))
#ressources.append(Ressource(ww//2 - 16, wh//4*3 - 32, 32, 32))
#ressources.append(Ressource(ww//2 - 16, wh - 32, 32, 32))
ressources.append(Ressource(0, wh - 32, 32, 32))
"""
for i in range(15):
    dax = randint(0, ww - 16)
    day = randint(0, wh - 16)
    ressources.append(Ressource(dax, day, 32, 32))
"""


"""
for i in range(30):
    dax = randint(0, ww - 16)
    day = randint(0, wh - 16)
    if i % 2 == 0:
        humans.append(Human(dax, day, "red", choice(["soldier", "worker"])))
    else:
        humans.append(Human(dax, day, "blue", choice(["soldier", "worker"])))
"""

bases = []
bases.append(Base(0, 0, 128, 128, "red"))
bases.append(Base(ww - 128, wh - 128, 128, 128, "blue"))



defend_button = Button(300, 600, 150, 100, "Defend", (0, 50, 150), (100, 120, 130), "defend")
attack_button = Button(450, 600, 150, 100, "Attack", (0, 50, 150), (100, 120, 130), "attack")
start_mining_button =  Button(0, 600, 150, 100, "Start Mining", (0, 50, 150), (100, 120, 130), "start mining")
stop_mining_button =  Button(150, 600, 150, 100, "Stop Mining", (0, 50, 150), (100, 120, 130), "stop mining")
buttons = [defend_button, attack_button, start_mining_button, stop_mining_button]




clock = pygame.time.Clock()
running = True
ayeee = 0
while running:
    clock.tick(20)
    ayeee += 1
    if ayeee == 120:
        #print(5/0)
        continue
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            break
        elif event.type == pygame.FINGERDOWN or event.type == pygame.MOUSEBUTTONDOWN:# and pygame.FINGERMOVE:#mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.FINGERDOWN:

                tx = int(event.x * ww)#ww + 100)
                ty = int(event.y * wh + 100)#600 + 360)#wh)
                for button in buttons:
                    button.check_pressing((tx, ty))
                    if button.pressed:
                        button.fpressed(humans)
            else:
                mouse_pos = pygame.mouse.get_pos()
                for button in buttons:
                    button.check_pressing((mouse_pos[0], mouse_pos[1]))
                    if button.pressed:
                        button.fpressed(humans)


    if not running:
        break
    win.fill((150, 200, 70))
    
    for ressource in ressources:
        ressource.draw(win)
    for base in bases:
        base.spawn(humans)
        if base.hp <= 0:
            bases.remove(base)
            continue
        base.draw(win, humans)
    for human in humans:
        if human.hp <= 0:
            humans.remove(human)
            continue
        human.ctarget(humans, ressources, bases)
    for human in humans:
        human.mover()
        human.draw(win)
    
    for button in buttons:
        button.draw(win)

    """
    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    textsurface = myfont.render(f"ressource of the {bases[-1].team} base: {bases[-1].ressource}", False, bases[-1].tc)
    win.blit(textsurface, (150, 30))
    """
    pygame.draw.rect(win, (0, 0, 0), pygame.Rect(0, 0, ww, wh), 2)
    pygame.draw.rect(win, (0, 0, 0), pygame.Rect(0, 0, ww, wh + 100), 2)
    pygame.display.flip()
