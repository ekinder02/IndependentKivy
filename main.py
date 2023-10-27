from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.clock import Clock
import math
from kivy.config import Config
import random
from kivy.animation import Animation
from kivy.uix.label import Label
import time
from functools import partial
from kivy.uix.progressbar import ProgressBar

Config.set('graphics', 'width', '1200')
Config.set('graphics', 'height', '800')
Config.write()

class PVZApp(App): 
    def build(self):
        game = GameManager()
        return game

rounds = [[8,2,0],[12,6,2],[17,10,8]]
roundsF = [10,20,35]
roundsT = [10,20,35]
timeRounds = [[180,300],[120,240],[90,210]]
selection = ""
isSliding = False
troops = []
troopHealth = []
troopCalls = []
balls = []
calls = 0
sec = 180
energy = 100
enemies = []
enemyHealth = []
enemyCalls = []
mowers = []
mowersUsed = []
callsSpawn = 0
i = 0
roundProgress = ProgressBar(max = 100, value = 0, size = (100, 100), pos = (0, 0))
class GameManager(Widget):
    def __init__(self, **args):
        super(GameManager, self).__init__(**args)
        self.mainScreen()
    
    def mainScreen(self):
        global layout
        layout = Widget()
        for i in layout.children:
            layout.remove_widget(i)
        layout.add_widget(Image(source = "background.png",size = (1200, 800), pos = (0,0)))
        startGame = Button(background_normal = "clickButton.png" ,size = (600,200),pos = (0,550))
        startGame.bind(on_press = lambda x: self.startGame())
        instructions = Button(background_normal = "instructButton.png" ,size = (600,200),pos = (600,550))
        instructions.bind(on_press = lambda x: self.instructions())
        layout.add_widget(startGame)
        layout.add_widget(instructions)
        self.add_widget(layout)
    
    def instructions(self):
        global layout
        for i in layout.children:
            layout.remove_widget(i)
        layout.add_widget(Image(source = "instrutionsBack.png",size = (1200, 800), pos = (0,0)))
        back = Button(background_normal = "back.png" ,size = (600,200),pos = (0,600))
        back.bind(on_press = lambda x: self.mainScreen())
        layout.add_widget(back)
    
    def startGame(self):
        for i in self.children:
            self.remove_widget(i)
        self.add_widget(Image(source = "background.png",size = (1200, 800), pos = (0,0)))
        self.SelectionBar()
        self.roundBar()
        self.energyDisplay()
        self.court()
        self.clock = Clock.schedule_interval(self.update, 1.0/56.5)
    
    def SelectionBar(self):
        layout = GridLayout(cols = 5, rows = 1,size = (500, 100),center = (600,50))

        btn = Button(text ="JR Smith\nCost: 50",
                        color =(1, 0, .65, 1),
                        size = (100, 100),
                        pos = (0,0),
                    )
        btn.bind(on_press = lambda x: self.troopSelection("jraw"))
        
        btn2 = Button(text ="Lebron James\nCost: 200",
                        color =(1, 0, .65, 1),
                        size = (100, 100),
                        pos = (100,0),
                    ) 
        btn2.bind(on_press = lambda x: self.troopSelection("newbron"))
        
        btn3 = Button(text ="Kyrie Irving\nCost: 100",
                        color =(1, 0, .65, 1),
                        size = (100, 100),
                        pos = (200,0),
                    )
        btn3.bind(on_press = lambda x: self.troopSelection("irving"))
        
        btn4 = Button(text ="Kevin Love\nCost: 75",
                        color =(1, 0, .65, 1),
                        size = (100, 100),
                        pos = (300,0),
                    ) 
        btn4.bind(on_press = lambda x: self.troopSelection("klove"))
        
        btn5 = Button(text ="Delete Troop",
                        color =(1, 0, .65, 1),
                        size = (100, 100),
                        pos = (300,0),
                    ) 
        btn5.bind(on_press = lambda x: self.troopSelection("del"))

        layout.add_widget(btn)
        layout.add_widget(btn2)
        layout.add_widget(btn3)
        layout.add_widget(btn4)
        layout.add_widget(btn5)
        self.add_widget(layout)
    
    def energyDisplay(self):
        global energy
        global energyDisplay
        energyDisplay = Label(text = "Energy: " + str(energy), pos = (100, 700),color= "FFFFFF",font_size = "50sp")
        self.add_widget(energyDisplay)
    
    def energyUpdate(self):
        energyDisplay.text = "Energy: " + str(energy)
    
    def court(self):
        courtImage = Image(source = "court.png",size = (1200, 500), pos = (0, 100))
        self.add_widget(courtImage)
        
    def troopSelection(self, troop):
        global selection
        selection = troop
    
    def on_touch_move(self, touch):
        global isSliding
        isSliding = True
    
    def makeTroop(self,troop,posCords):
        global energy
        go = False
        health = 0
        if troop == "newbron" and energy >= 200:
            energy -= 200
            go = True
            health = 10
        elif troop == "irving" and energy >= 100:
            energy -= 100
            go = True
            health = 10
        elif troop == "jraw" and energy >= 50:
            energy -= 50
            go = True
            health = 5
        elif troop == "klove" and energy >= 75:
            energy -= 75
            go = True
            health = 25
        if go == True:
            sourceImg = troop + ".png"
            troopImage = Image(source = sourceImg ,size = (100, 100), pos = posCords)
            global troops
            global troopHealth
            global troopCalls
            troops.append(troopImage)
            troopHealth.append(health)
            troopCalls.append(1)
            self.add_widget(troopImage)
    
    def on_touch_up(self, touch):
        global isSliding
        global selection
        global troops
        if isSliding == True and selection == "del" and myround(touch.pos)[1] >= 100 and myround(touch.pos)[1] <= 500 and myround(touch.pos)[0] >= 0 and myround(touch.pos)[0] <= 800:
            self.deleteTroop(myround(touch.pos))
            isSliding = False
            return
        for troop in troops:
            if troop.pos[0] == myround(touch.pos)[0] and troop.pos[1] == myround(touch.pos)[1]:
                isSliding = False
                return
        if isSliding == True and selection != "" and myround(touch.pos)[1] >= 100 and myround(touch.pos)[1] <= 500 and myround(touch.pos)[0] >= 0 and myround(touch.pos)[0] <= 800:
            self.makeTroop(selection,myround(touch.pos))
            selection = ""
            isSliding = False
    
    def spawnBullet(self, troop):
        troopImage = Image(source = "ball.png" ,size = (100, 100), pos = troop.pos)
        return(troopImage)
    
    def deleteTroop(self, pos):
        global troops
        global energy
        global troopHealth
        global troopCalls
        for troop in troops:
            if troop.pos[0] == pos[0] and troop.pos[1] == pos[1]:
                troopHealth.remove(troopHealth[troops.index(troop)])
                troopCalls.remove(troopCalls[troops.index(troop)])
                self.remove_widget(troop)
                troops.remove(troop)
                energy += 25
                return
    
    def inRow(self,pos):
        for enemy in enemies:
            if enemy.pos[1] == pos[1]:
                return(True)
    
    def shoot(self):
        global balls
        global troops
        global energy
        for troop in troops:
            if troop.source == "newbron.png" and troopCalls[troops.index(troop)] % 60 == 0 and self.inRow(troop.pos) == True:
                shoot = Animation(size = (125, 100), d = 0.25, t = 'out_elastic')
                shoot += Animation(size = (100, 100), d = 0.1)
                shoot.start(troop)
                troopCalls[troops.index(troop)] = 0
                ball = self.spawnBullet(troop)
                self.add_widget(ball)
                balls.append(ball)
            if troop.source == "irving.png" and troopCalls[troops.index(troop)] % 90 == 0 and self.inRow(troop.pos) == True:
                shoot = Animation(size = (125, 100), d = 0.25, t = 'out_elastic')
                shoot += Animation(size = (100, 100), d = 0.1)
                shoot.start(troop)
                troopCalls[troops.index(troop)] = 0
                ball = self.spawnBullet(troop)
                self.add_widget(ball)
                balls.append(ball)
            if troop.source == "jraw.png" and troopCalls[troops.index(troop)] % 1800 == 0:
                stretch = Animation(size = (100, 125), d = 0.5, t = 'out_elastic')
                stretch += Animation(size = (100, 100), d = 0.5)
                stretch.start(troop)
                troopCalls[troops.index(troop)] = 0
                energy += 50
    
    def roundStart(self):
        round = Label(text = "Round" + str(i+1), pos = (600, 400),color= "FFFFFF",font_size = "200")
        self.add_widget(round)
        stretch = Animation(pos = (round.pos[0],round.pos[1]-50), d = 2)
        stretch += Animation(pos = (round.pos[0],round.pos[1]+50), d = 1)
        stretch.start(round)
        Clock.schedule_once(partial(self.removeWidget, round), 4)
    
    def roundBar(self):
        global i
        global roundProgress
        roundProgress = ProgressBar(max = 100, value = 0, size = (400, 100), pos = (500, 700))
        self.add_widget(roundProgress)
    
    def addBar(self):
        global i
        global roundProgress
        roundProgress.value += 100/roundsF[i]
    
    def updateBar(self):
        roundProgress.value = 0
    
    def removeWidget(self,widget,*largs):
        self.remove_widget(widget)
    
    def moveBall(self):
        global balls
        for ball in balls:
            ball.pos = (ball.pos[0] + 10, ball.pos[1])
            self.didCollide(ball,False)
    
    def endOfMap(self):
        global enemies
        global mowers
        global mowersUsed
        for enemy in enemies:
            if enemy.pos[0] == 0:
                lat = enemy
                if mowersUsed == []:
                    ball = self.spawnBullet(lat)
                    self.add_widget(ball)
                    mowers.append(ball)
                    mowersUsed.append(ball.pos)
                    return
                for mower in mowersUsed:
                    if mower[1] == lat.pos[1]:
                        return(False)
                ball = self.spawnBullet(lat)
                self.add_widget(ball)
                mowers.append(ball)
                mowersUsed.append(ball.pos)
                return
            
    def moveMowers(self):
        global mowers
        for mower in mowers:
            mower.pos = (mower.pos[0] + 20, mower.pos[1])
            self.didCollide(mower,True)
            
    def moveEnemy(self):
        global enemies
        global troops
        global calls
        global troopCalls
        global enemyCalls
        cantMove = False
        for enemy in enemies:
            for troop in troops:
                if enemy.pos[0] - troop.pos[0] <= 50 and enemy.pos[0] - troop.pos[0] > 0 and enemy.pos[1] == troop.pos[1]:
                    cantMove = True
                    if enemyCalls[enemies.index(enemy)] % 60 == 0:
                        attack = Animation(size = (125, 100), d = 0.25, t = 'out_elastic')
                        attack += Animation(size = (100, 100), d = 0.1)
                        attack.start(enemy)
                        enemyCalls[enemies.index(enemy)] = 0
                        troopHealth[troops.index(troop)] -= 1
                        if troopHealth[troops.index(troop)] == 0:
                            troopHealth.remove(troopHealth[troops.index(troop)])
                            troopCalls.remove(troopCalls[troops.index(troop)])
                            self.remove_widget(troop)
                            troops.remove(troop)
                    continue
            if cantMove == True:
                cantMove = False
                continue
            if enemy.source == "klay.png":
                enemy.pos = (enemy.pos[0] - 0.5, enemy.pos[1])
            if enemy.source == "curry.png" or "draymond.png":
                enemy.pos = (enemy.pos[0] - 0.3, enemy.pos[1])
            
    def didCollide(self, ball,end):
        global enemies
        global balls
        global mowers
        global enemyCalls
        for enemy in enemies:
            if abs(ball.pos[0] - enemy.pos[0]) <= 25 and ball.pos[1] == enemy.pos[1]:
                if end == False:
                    enemyHealth[enemies.index(enemy)] -= 1
                    self.remove_widget(ball)
                    balls.remove(ball)
                elif end == True:
                    enemyHealth[enemies.index(enemy)] = 0
                if enemyHealth[enemies.index(enemy)] == 0:
                    enemyHealth.remove(enemyHealth[enemies.index(enemy)])
                    enemyCalls.remove(enemyCalls[enemies.index(enemy)])
                    self.remove_widget(enemy)
                    enemies.remove(enemy)
                    self.addBar()
                return
            if ball.pos[0] > 1200:
                self.remove_widget(ball)
                if end == False:
                    balls.remove(ball)
                if end == True:
                    mowers.remove(ball)
                return
            
                
    def makeEnemy(self,enemy):
        sourceImg = enemy + ".png"
        enemyImage = Image(source = sourceImg ,size = (100, 100), pos = (1200,random.randint(1,5)*100))
        global enemies
        global enemyHealth
        global enemyCalls
        enemies.append(enemyImage)
        enemyCalls.append(1)
        if enemy == "curry":
            enemyHealth.append(10)
        elif enemy == "draymond":
            enemyHealth.append(15)
        elif enemy == "klay":
            enemyHealth.append(8)
        self.add_widget(enemyImage)
    
    def spawnRounds(self):
        global sec
        global calls
        global rounds
        global roundsT
        global i
        global callsSpawn
        global timeRounds
        enemyList = ["curry","draymond","klay"]
        if callsSpawn % sec == 0 and callsSpawn != 0 and rounds[i] != 0 and roundsT[i] != 0:
            sec = random.randint(timeRounds[i][0],timeRounds[i][1])
            callsSpawn = 0
            choice = random.choice(enemyList)
            while rounds[i][enemyList.index(choice)] == 0:
                choice = random.choice(enemyList)
            self.makeEnemy(choice)
            rounds[i][enemyList.index(choice)] -= 1
            roundsT[i] -= 1
        
        
    def update(self,ndt):
        self.shoot()
        self.moveBall()
        self.moveEnemy()
        self.spawnRounds()
        self.moveMowers()
        if self.endOfMap() == False:
            print("Game Over")
        self.energyUpdate()
        global roundProgress
        global calls
        global i
        global callsSpawn
        global troopCalls
        global enemyCalls
        global enemies
        global troops
        calls += 1
        callsSpawn += 1
        for enemy in enemies:
            enemyCalls[enemies.index(enemy)] += 1 
        for troop in troops:
            troopCalls[troops.index(troop)] += 1
        
        if calls % 240 == 0:
            global energy
            energy += 25
        if calls == 10:
            self.roundStart()
        if roundProgress.value == roundProgress.max:
            self.updateBar()
            i += 1
            self.roundStart()
    
def myround(x, base=100):
    return (base * math.floor(x[0]/base),base * math.floor(x[1]/base))
root = PVZApp() 

root.run()