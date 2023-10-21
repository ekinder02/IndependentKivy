from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.clock import Clock
import math

class PVZApp(App): 
    def build(self):
        game = TopBar()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        game.makeEnemy("curry")
        return game

selection = ""
isSliding = False
troops = []
balls = []
calls = 0
enemies = []
class TopBar(Widget):
    def __init__(self, **args):
        super(TopBar, self).__init__(**args)
        self.selectionBar()
        self.field()
    
    def selectionBar(self):
        layout = GridLayout(cols = 4, rows = 1)

        btn = Button(text ="",
                        color =(1, 0, .65, 1),
                        size = (100, 100),
                        pos = (0,0),
                    )
        btn.bind(on_press = lambda x: self.troopSelection("AD"))
        
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
        btn4.bind(on_press = lambda x: self.troopSelection("bron"))

        layout.add_widget(btn)
        layout.add_widget(btn2)
        layout.add_widget(btn3)
        layout.add_widget(btn4)
        self.add_widget(layout)
        
    def field(self):
        fieldImage = Image(source = "field.jpg",size = (400, 400), pos = (300, 100))
        self.add_widget(fieldImage)
        
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
        sourceImg = troop + ".png"
        troopImage = Image(source = sourceImg ,size = (100, 100), pos = posCords)
        global troops
        troops.append(troopImage)
        self.add_widget(troopImage)
    
    def on_touch_up(self, touch):
        global isSliding
        global selection
        if isSliding == True and selection != "":
            self.makeTroop(selection,myround(touch.pos))
            selection = ""
        isSliding = False
    
    def spawnBullet(self, troop):
        troopImage = Image(source = "ball.png" ,size = (100, 100), pos = troop.pos)
        return(troopImage)
    
    def shoot(self):
        global balls
        global troops
        for troop in troops:
            if troop.source == "bron.png" and calls % 60 == 0:
                ball = self.spawnBullet(troop)
                self.add_widget(ball)
                balls.append(ball)
            if troop.source == "KD.png" and calls % 120 == 0:
                ball = self.spawnBullet(troop)
                self.add_widget(ball)
                balls.append(ball)
    
    def moveBall(self):
        global balls
        for ball in balls:
            ball.pos = (ball.pos[0] + 10, ball.pos[1])
            self.didCollide(ball)
            
    def moveEnemy(self):
        global benemies
        for enemy in enemies:
            enemy.pos = (enemy.pos[0] - 1, enemy.pos[1])
            
    def didCollide(self, ball):
        global enemies
        global balls
        for enemy in enemies:
            if abs(ball.pos[0] - enemy.pos[0]) <= 25 and ball.pos[1] == enemy.pos[1]:
                self.remove_widget(ball)
                self.remove_widget(enemy)
                enemies.remove(enemy)
                balls.remove(ball)
            if ball.pos[0] > 900:
                self.remove_widget(ball)
                balls.remove(ball)
                
    def makeEnemy(self,enemy):
        sourceImg = enemy + ".png"
        enemyImage = Image(source = sourceImg ,size = (100, 100), pos = (1000,200))
        global enemies
        enemies.append(enemyImage)
        self.add_widget(enemyImage)
        
    def update(self,ndt):
        self.shoot()
        self.moveBall()
        self.moveEnemy()
        global calls
        calls += 1
    
def myround(x, base=100):
    return (base * math.floor(x[0]/base),base * math.floor(x[1]/base))
root = PVZApp() 

root.run()