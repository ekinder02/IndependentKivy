from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
import math

class PVZApp(App): 
    def build(self):
        return TopBar()

selection = ""
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
        btn.bind(on_press = lambda x: self.troopSelection("bow"))
        
        btn2 = Button(text ="",
                        color =(1, 0, .65, 1),
                        size = (100, 100),
                        pos = (100,0),
                    ) 
        btn2.bind(on_press = lambda x: self.troopSelection("sword"))
        
        btn3 = Button(text ="",
                        color =(1, 0, .65, 1),
                        size = (100, 100),
                        pos = (200,0),
                    )
        btn3.bind(on_press = lambda x: self.troopSelection("spear"))
        
        btn4 = Button(text ="",
                        color =(1, 0, .65, 1),
                        size = (100, 100),
                        pos = (300,0),
                    ) 
        btn4.bind(on_press = lambda x: self.troopSelection("stick"))

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
    
    def on_touch_up(self, touch):
        global selection
        selection = ""
def myround(x, base=50):
    return (base * math.ceil(x[0]/base),base * math.ceil(x[1]/base))
root = PVZApp() 

root.run()