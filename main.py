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

class PVZApp(App): 
    def build(self):
        game = TopBar()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game

rounds = [[8,2,0],[12,6,2]]
roundsF = [10,20]
roundsT = [10,20]
selection = ""
isSliding = False
troops = []
balls = []
calls = 0
energy = 100
enemies = []
enemyHealth = []
i = 0
roundProgress = ProgressBar(max = 100, value = 0, size = (100, 100), pos = (0, 0))
class TopBar(Widget):
    def __init__(self, **args):
        super(TopBar, self).__init__(**args)
        self.selectionBar()
        self.bar()
    
    def selectionBar(self):
        layout = GridLayout(cols = 4, rows = 1,size = (400, 100))

        btn = Button(text ="",
                        color =(1, 0, .65, 1),
                        size = (100, 100),
                        pos = (0,0),
                    )
        btn.bind(on_press = lambda x: self.troopSelection("JR"))
        
        btn2 = Button(text ="",
                        color =(1, 0, .65, 1),
                        size = (100, 100),
                        pos = (100,0),
                    ) 
        btn2.bind(on_press = lambda x: self.troopSelection("bron"))
        
        btn3 = Button(text ="",
                        color =(1, 0, .65, 1),
                        size = (100, 100),
                        pos = (200,0),
                    )
        btn3.bind(on_press = lambda x: self.troopSelection("KD"))
        
        btn4 = Button(text ="",
                        color =(1, 0, .65, 1),
                        size = (100, 100),
                        pos = (300,0),
                    ) 
        btn4.bind(on_press = lambda x: self.troopSelection("del"))

        layout.add_widget(btn)
        layout.add_widget(btn2)
        layout.add_widget(btn3)
        layout.add_widget(btn4)
        self.add_widget(layout)
        
    def court(self):
        courtImage = Image(source = "court.jpg",size = (1000, 800), pos = (0, 0))
        self.add_widget(courtImage)
        
    def troopSelection(self, troop):
        global selection
        selection = troop
        print(selection)
    
    def on_touch_move(self, touch):
        print(selection)
        print('The touch is at position', myround(touch.pos))
        global isSliding
        isSliding = True
    
    def makeTroop(self,troop,posCords):
        global energy
        go = False
        if troop == "bron" and energy >= 125:
            energy -= 125
            go = True
        elif troop == "KD" and energy >= 50:
            energy -= 50
            go = True
        elif troop == "JR" and energy >= 75:
            energy -= 75
            go = True
        if go == True:
            sourceImg = troop + ".png"
            troopImage = Image(source = sourceImg ,size = (100, 100), pos = posCords)
            global troops
            troops.append(troopImage)
            self.add_widget(troopImage)
    
    def on_touch_up(self, touch):
        global isSliding
        global selection
        if isSliding == True and selection == "del":
            self.deleteTroop(myround(touch.pos))
        elif isSliding == True and selection != "":
            self.makeTroop(selection,myround(touch.pos))
            selection = ""
        isSliding = False
    
    def spawnBullet(self, troop):
        troopImage = Image(source = "ball.png" ,size = (100, 100), pos = troop.pos)
        return(troopImage)
    
    def deleteTroop(self, pos):
        global troops
        global energy
        for troop in troops:
            if troop.pos[0] == pos[0] and troop.pos[1] == pos[1]:
                self.remove_widget(troop)
                troops.remove(troop)
                energy += 25
                return
    
    def shoot(self):
        global balls
        global troops
        global energy
        for troop in troops:
            if troop.source == "bron.png" and calls % 200 == 0:
                shoot = Animation(size = (125, 100), d = 0.25, t = 'out_elastic')
                shoot += Animation(size = (100, 100), d = 0.1)
                shoot.start(troop)
                ball = self.spawnBullet(troop)
                self.add_widget(ball)
                balls.append(ball)
            if troop.source == "KD.png" and calls % 350 == 0:
                shoot = Animation(size = (125, 100), d = 0.25, t = 'out_elastic')
                shoot += Animation(size = (100, 100), d = 0.1)
                shoot.start(troop)
                ball = self.spawnBullet(troop)
                self.add_widget(ball)
                balls.append(ball)
            if troop.source == "JR.png" and calls % 500 == 0:
                stretch = Animation(size = (100, 125), d = 0.5, t = 'out_elastic')
                stretch += Animation(size = (100, 100), d = 0.5)
                stretch.start(troop)
                energy += 50
    
    def roundStart(self):
        round = Label(text = "Round" + str(i+1), pos = (600, 400),color= "ff3333",size = (100, 100))
        self.add_widget(round)
        stretch = Animation(pos = (round.pos[0],round.pos[1]-50), d = 2)
        stretch += Animation(pos = (round.pos[0],round.pos[1]+50), d = 1)
        stretch.start(round)
        Clock.schedule_once(partial(self.removeWidget, round), 4)
    
    def bar(self):
        global i
        global roundProgress
        roundProgress = ProgressBar(max = 100, value = 0, size = (100, 100), pos = (0, 0))
        self.add_widget(roundProgress)
    def addBar(self):
        global i
        global roundProgress
        roundProgress.value += 100/roundsF[i]
        print(100/roundsF[i])
    def updateBar(self):
        roundProgress.value = 0
    
    def removeWidget(self,widget,*largs):
        self.remove_widget(widget)
    
    def moveBall(self):
        global balls
        for ball in balls:
            ball.pos = (ball.pos[0] + 10, ball.pos[1])
            self.didCollide(ball)
            
    def moveEnemy(self):
        global enemies
        for enemy in enemies:
            if enemy.source == "klay.png":
                enemy.pos = (enemy.pos[0] - 0.8, enemy.pos[1])
            if enemy.source == "curry.png" or "draymond.png":
                enemy.pos = (enemy.pos[0] - 0.5, enemy.pos[1])
            
    def didCollide(self, ball):
        global enemies
        global balls
        for enemy in enemies:
            if abs(ball.pos[0] - enemy.pos[0]) <= 25 and ball.pos[1] == enemy.pos[1]:
                enemyHealth[enemies.index(enemy)] -= 1
                self.remove_widget(ball)
                balls.remove(ball)
                if enemyHealth[enemies.index(enemy)] == 0:
                    enemyHealth.remove(enemyHealth[enemies.index(enemy)])
                    self.remove_widget(enemy)
                    enemies.remove(enemy)
                    self.addBar()
                return
            if ball.pos[0] > 1200:
                self.remove_widget(ball)
                balls.remove(ball)
                return
                
    def makeEnemy(self,enemy):
        sourceImg = enemy + ".png"
        enemyImage = Image(source = sourceImg ,size = (100, 100), pos = (1200,random.randint(1,6)*100))
        global enemies
        global enemyHealth
        enemies.append(enemyImage)
        if enemy == "curry":
            enemyHealth.append(3)
        elif enemy == "draymond":
            enemyHealth.append(5)
        elif enemy == "klay":
            enemyHealth.append(2)
        self.add_widget(enemyImage)
    
    def spawnRounds(self):
        sec = 150
        global calls
        global rounds
        global roundsT
        global i
        enemyList = ["curry","draymond","klay"]
        if calls % sec == 0 and calls != 0 and rounds[i] != 0 and roundsT[i] != 0:
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
        global roundProgress
        global calls
        global i
        print(i)
        calls += 1
        if calls % 500 == 0:
            global energy
            energy += 25
        if calls == 10:
            self.roundStart()
        if roundProgress.value == roundProgress.max:
            self.updateBar()
            i += 1
            self.roundStart()
            print("AFHSBIFBASJOFAJOSFNOJAF")
        print (energy)
    
def myround(x, base=100):
    return (base * math.floor(x[0]/base),base * math.floor(x[1]/base))
root = PVZApp() 

root.run()