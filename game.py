from kivy.app import App 
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.core.window import Window
from random import randint
from kivy.uix.widget import Widget
from kivy.uix.slider import Slider
from kivy.core.audio import SoundLoader
from kivy.uix.video import Video

import json 

    
class ScrButton(Button):
    def __init__(self, screen, direction='right', goal='', text='', **kwargs):
        super().__init__(text=text, **kwargs)
        self.screen = screen
        self.direction = direction
        self.goal = goal

class FallingSprite(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  
        self.size_hint = (None, None)   
        self.size = (64, 64)
        self.source = 'pngtree-cute-or-creepy-cartoon-ghost-for-halloween-costume-fantasy-no-background-png-image_10462460.png' 
        self.pos = (randint(0, Window.width - 64), randint(Window.height - 64, Window.height))
        self.speed = 200  
        
    def update(self, dt):
        self.game = App.get_running_app().root.get_screen('ScrPlay')
        x, y = self.pos
        if self.game.manager.current == 'ScrPlay':
            y -= self.speed * dt
        if y + self.height > 0:
            self.pos = (x, y)
        else:
            self.reset()
            self.game.score -= 1
            self.game.label.text = "Score: " + str(self.game.score) + "\n" + "Boost at 50 points!\nIt is a mystery." 
             
        if self.game.score == -1:
            self.game.jumpscare()
            self.game.score = 0
            self.game.label.text = "Score: " + str(self.game.score) 

            if self.game.score >= 50:
                self.game.score -= 4
            if self.game.score >= 200:
                self.game.score -= 20
            if self.game.score >= 500:
                self.game.score -= 75
             
        if self.game.score == -1:
            self.game.jumpscare()
            self.game.score = 0
            self.game.label.text = "Score: " + str(self.game.score)  
            
        if self.game.score >= 50:
            self.speed = 250
            self.n = 5
            self.game.label.text = "Score: " + str(self.game.score) + "\n" + "Bonus at 200 points!\n It is a mystery."
            
        if self.game.score >= 200:
            self.speed = 300
            self.n = 25
            self.game.label.text = "Score: " + str(self.game.score) + "\n" + "At 500, you will face death!!"
            
        if self.game.score >= 500:
            self.game.label.text = "Score: " + str(self.game.score) + "\n" + "You can't make it to 1000 points!"
            self.speed = 350
            
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.game = App.get_running_app().root.get_screen('ScrPlay')
            self.game.score += 1
            self.game.label.text = "Score: " + str(self.game.score)
            self.parent.remove_widget(self)
            self.game.sprites.remove(self)
            return True
        return super().on_touch_down(touch)
    
    def reset(self):
        self.pos = (randint(0, Window.width - 64), randint(Window.height - 64, Window.height))
        
class FirstScreen(Screen):
    def __init__(self, name='main_menu'):
        super().__init__(name=name)
    
        self.image = Image(source = 'sit.png', size_hint = (.6, .6), pos_hint = {'center_x':0.5, 'center_y':0.75})
        
        play_button = ScrButton(self, direction = 'right', goal = 'ScrPlay', text = 'Play', size_hint = (.5, .1), pos_hint = {'center_x':0.5, 'center_y':0.4})
        option_button = ScrButton(self, direction =  'right', goal = 'ScrOption', text = 'Options', size_hint = (.5, .1), pos_hint = {'center_x':0.5, 'center_y':0.25})     
        quit_button = ScrButton(self, direction = 'right', goal = '', text = 'Leave', size_hint = (.5, .1), pos_hint = {'center_x':0.5, 'center_y':0.1})   
             
        layout = FloatLayout()
        
        play_button.bind(on_press = self.next)
        option_button.bind(on_press = self.next1)
        quit_button.bind(on_press = self.left)
        
        layout.add_widget(self.image)
        layout.add_widget(play_button)
        layout.add_widget(option_button)
        layout.add_widget(quit_button)
        
        self.add_widget(layout)

        self.sound = SoundLoader.load('Wii Music - Gaming Background Music (HD).mp3')
        if self.sound:
            self.sound.play()
            
    def next(self, instance):
        self.manager.transition.direction = 'left'
        self.manager.current  = 'ScrPlay'
        if self.sound:
            self.sound.stop()  
            
    def next1(self, instance):
        self.manager.transition.direction = 'down'
        self.manager.current = 'ScrOption'
            
    def left(self, instance):
        App.get_running_app().stop()
            
class Play_Menu(Screen):
    def __init__(self, name = 'ScrPlay', **kwargs):
        super().__init__(**kwargs, name = name)
        self.sprites = []
        self.layout = FloatLayout()  
        self.score = 0
        self.background = Image(source = 'focfocfoc.jpg')
        
        self.manele = SoundLoader.load("jojo.mp3")    
        
        Clock.schedule_interval(self.update, 1/60)  
        
        self.label = Label(text = "Score:" + str(0), size_hint = (.5, .1), pos_hint = {'center_x':0.5, 'center_y': 0.9})
        self.pause_menu = Label(text = 'Pause', size_hint = (.1, .1), pos_hint = {'center_x': 0.25, 'center_y': 0.9})
        
        self.add_widget(self.pause_menu)
        self.layout.add_widget(self.background)
        self.layout.add_widget(self.label)

        self.add_widget(self.layout)
        
    def update(self, dt):
        for sprite in self.sprites:
            sprite.update(dt)
        if len(self.sprites) == 0:
            for i in range(5): 
                sprite = FallingSprite()
                self.layout.add_widget(sprite)
                self.sprites.append(sprite)

    def jumpscare(self):
        Clock.unschedule(self.update)
        self.manager.transition.direction = 'down'
        self.manager.current = 'jumpscare_'
        for sprite in self.sprites:
            self.layout.remove_widget(sprite)
        self.sprites.clear()
        
    def on_enter(self, *args):
        if self.manele:
            self.manele.loop = True 
            self.manele.play()
        Clock.schedule_interval(self.update, 1/60)

    def on_leave(self, *args):
        Clock.unschedule(self.update)
        for sprite in self.sprites:
            self.layout.remove_widget(sprite)
        self.sprites.clear()        
        if self.manele:
            self.manele.stop()

    def on_touch_down(self, touch):
        if self.pause_menu.collide_point(*touch.pos):
            Clock.unschedule(self.update)
            self.manager.transition.direction = 'down'
            self.manager.current = 'pause_menu'
            return True
        return super().on_touch_down(touch)
        
class Option_Menu(Screen):
    def __init__(self, name = 'ScrOption'):
        super().__init__(name = name)
        
        audiobtn = ScrButton(self, direction = 'right', goal = '', text = 'Volume', size_hint = (.4, .1), pos_hint = {'center_x':0.5, 'center_y': 0.9})
        monsterbtn = ScrButton(self, direction = 'right', goal = '', text = 'Round thing design', size_hint = (.4, .1), pos_hint = {'center_x':0.5, 'center_y':0.75})        
        backimgbtn = ScrButton(self, direction= 'right', goal = '', text = 'Location background', size_hint = (.4, .1), pos_hint = {'center_x': 0.5, 'center_y': 0.6})
        returnbtn = ScrButton(self, direction= 'right', goal = '', text = 'Back to main menu', size_hint = (.4, .1), pos_hint = {'center_x':0.5, 'center_y':0.2})

        layout = FloatLayout()
        
        returnbtn.bind(on_press = self.returned)
        
        audiobtn.bind(on_press = self.modify_audio)
        
        monsterbtn.bind(on_press = self.troll1)
        
        backimgbtn.bind(on_press = self.troll2)
        
        layout.add_widget(audiobtn)
        layout.add_widget(monsterbtn)
        layout.add_widget(backimgbtn)
        layout.add_widget(returnbtn)
        
        self.add_widget(layout)
        
    def returned(self, instance):
        self.manager.transition.direction = 'up'
        self.manager.current = 'main_menu'
    
    def modify_audio(self, instance):
        self.manager.transition.direction = 'up'
        self.manager.current = 'modify_volume'
        
    def troll1(self, instance):
        self.manager.transition.direction = 'up'
        self.manager.current = 'haha1'
        
    def troll2(self, instance):
        self.manager.transition.direction = 'up'
        self.manager.current = 'haha2'

class Modifying_Audio(Screen):
    def __init__(self, name='modify_volume'):
        super().__init__(name=name)

        self.layout = FloatLayout()

        self.label = Label(
            text='Volume: 100%',
            size_hint=(.5, .1),
            pos_hint={'center_x': 0.5, 'center_y': 0.85},
            font_size='20sp'
        )

        self.slider = Slider(
            min=0,
            max=100,
            value=100,
            step=1,
            size_hint=(.8, .1),
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )
        self.slider.bind(value=self.on_slider_value_change)
        
        savebtn = ScrButton(self, direction='right', goal='', text='Save the presets',
                            size_hint=(.4, .1), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        savebtn.bind(on_press=self.handle_save)

        self.layout.add_widget(self.label)
        self.layout.add_widget(self.slider)
        self.layout.add_widget(savebtn)

        self.add_widget(self.layout)

    def on_enter(self):
        try:
            with open('info.json', 'r') as file:
                data = json.load(file)
                vol = data.get("volum", 1.0)
                self.slider.value = int(vol * 100)
        except:
            self.slider.value = 100 

    def on_slider_value_change(self, instance, value):
        self.label.text = f'Volume: {int(value)}%'
        self.volume = max(0.0, min(1.0, float(value) / 100))

        try:
            self.menu_audio = App.get_running_app().root.get_screen('main_menu')
            self.menu_joc = App.get_running_app().root.get_screen('ScrPlay')

            if self.menu_audio.sound:
                self.menu_audio.sound.volume = self.volume
            if self.menu_joc.manele:
                self.menu_joc.manele.volume = self.volume
        except:
            pass  

    def back(self, instance):
        self.manager.transition.direction = 'down'
        self.manager.current = 'ScrOption'

    def handle_save(self, instance):
        if not hasattr(self, 'volume'):
            return
        try:
            with open('info.json', 'r') as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        data["volum"] = self.volume

        with open('info.json', 'w') as file:
            json.dump(data, file, indent=4)
            
        self.manager.transition.direction = 'down'
        self.manager.current = 'ScrOption'
            
class Jumpscare(Screen):
    def __init__(self, name='jumpscare_'):
        super().__init__(name=name)

        label = Label(text = 'Game over!', pos_hint = {'center_x':0.5, 'center_y':0.9})
        
        self.sperietura = Video(source='scream.mp4', state='stop', options={'eos': 'loop'})

        self.add_widget(label)
        self.add_widget(self.sperietura)

    def on_enter(self):    
               
        self.sperietura.state = 'play'

        Clock.schedule_once(self.jumpscares, 7)
        Clock.schedule_once(self.jumpscares, 7)

    def jumpscares(self, instance):
        
        self.sperietura.state = 'stop'
        
        self.manager.transition.direction = 'left'
        self.manager.current = 'main_menu'
        
        menu_screen = self.manager.get_screen('main_menu')
        if hasattr(menu_screen, 'sound') and menu_screen.sound:
            menu_screen.sound.play()
        
class Happy1(Screen):
    def __init__(self, name='haha1'):
        super().__init__(name=name)
        
        label = Label(
            text="HAHA, YOU CAN'T CHANGE THE GAME'S MASCOT :)",
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            font_size='20sp'
        )
        self.add_widget(label)
    
    def on_enter(self):
        Clock.schedule_once(self.return_to_options, 3)
        
    def return_to_options(self, dt):
        self.manager.transition.direction = 'down'
        self.manager.current = 'ScrOption'

class Happy2(Screen):
    def __init__(self, name='haha2'):
        super().__init__(name=name)
        
        label = Label(
            text="HAHA, YOU CAN'T CHANGE THE GAME'S BACKGROUND :)",
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            font_size='20sp'
        )
        
        self.add_widget(label)
        
    def on_enter(self):
        Clock.schedule_once(self.return_to_options, 3)
        
    def return_to_options(self, dt):
        self.manager.transition.direction = 'down'
        self.manager.current = 'ScrOption'
        
class PauseMenu(Screen):
    def __init__(self, name='pause_menu'):
        super().__init__(name=name)
        
        layout = FloatLayout()
        
        return_menu_btn = ScrButton(self, direction='right', goal='', text='Back to main menu', size_hint=(.4, .1), pos_hint={'center_x': 0.5, 'center_y': 0.75})
        return_game_btn = ScrButton(self, direction='right', goal='', text='Back to play menu', size_hint=(.4, .1), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        
        return_menu_btn.bind(on_press=self.inapoi)
        return_game_btn.bind(on_press=self.game)
        
        layout.add_widget(return_menu_btn)
        layout.add_widget(return_game_btn)
        
        self.add_widget(layout)

    def inapoi(self, instance):
        self.manager.transition.direction = 'up'
        self.manager.current = 'main_menu'
        
        r_play = App.get_running_app().root.get_screen('ScrPlay')
        r_play.score = 0
        
    def game(self, instance):
        self.manager.transition.direction = 'up'
        self.manager.current = 'ScrPlay'

        scr_play = App.get_running_app().root.get_screen('ScrPlay')
        Clock.schedule_interval(scr_play.update, 1/60)
            
class Falling_Round_Things(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(FirstScreen())
        sm.add_widget(Play_Menu())
        sm.add_widget(Option_Menu())
        sm.add_widget(Jumpscare())
        sm.add_widget(Modifying_Audio())
        sm.add_widget(Happy1())
        sm.add_widget(Happy2())
        sm.add_widget(PauseMenu())
        volum = self.load_volume()

        main_menu = sm.get_screen('main_menu')
        play_menu = sm.get_screen('ScrPlay')

        if main_menu.sound:
            main_menu.sound.volume = volum
        if play_menu.manele:
            play_menu.manele.volume = volum
            
        return sm
    
    def load_volume(self):
        try:
            with open('info.json', 'r') as file:
                data = json.load(file)
                volum = data.get("volum", 1.0)
                return max(0.0, min(1.0, volum))
        except (FileNotFoundError, json.JSONDecodeError):
            return 1.0

Falling_Round_Things().run()
