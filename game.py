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
from kivy.core.audio import SoundLoader

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
            self.game.label.text = "Score: " + str(self.game.score)   
             
        if self.game.score == -1:
            self.game.jumpscare()
            self.game.score = 0
            self.game.label.text = "Score: " + str(self.game.score)   
            
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
        if self.sound:
            self.sound.stop()  
            
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
        
        layout.add_widget(audiobtn)
        layout.add_widget(monsterbtn)
        layout.add_widget(backimgbtn)
        layout.add_widget(returnbtn)
        
        self.add_widget(layout)
        
    def returned(self, instance):
        self.manager.transition.direction = 'up'
        self.manager.current = 'main_menu'
        
        self.menu = App.get_running_app().root.get_screen('main_menu')
        if self.menu.sound:
            self.menu.sound.play()

    
    def modify_audio(self, instance):
        self.manager.transition.direction = 'up'
        self.manager.current = 'modify_volume'

class Modifying_Audio(Screen):
    def __init__(self, name='modify_volume'):
        super().__init__(name=name)
        
        label = Label(text='Volume:', size_hint=(.5, .3), pos_hint={'center_x': 0.5, 'center_y': 0.9})
        self.bagavolum = TextInput(hint_text="Introduceți volumul între 0 și 100", multiline=False, size_hint=(.5, .1), pos_hint={'center_x': 0.5, 'center_y': 0.75})
        backbtn = ScrButton(self, direction='right', goal='ScrOption', text='Back to Options', size_hint=(.4, .1), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        savebtn = ScrButton(self, direction='right', goal='', text='Save the presets', size_hint=(.4, .1), pos_hint={'center_x': 0.5, 'center_y': 0.25})

        backbtn.bind(on_press=self.back)
        savebtn.bind(on_press=self.handle_save)

        layout = FloatLayout()
        layout.add_widget(label)
        layout.add_widget(self.bagavolum)
        layout.add_widget(savebtn)
        layout.add_widget(backbtn)

        self.add_widget(layout)

    def back(self, instance):
        self.manager.transition.direction = 'down'
        self.manager.current = 'ScrOption'
        self.bagavolum.text = ''

    def baga_volum_la_sunet_ca_sa_nu_surzesti(self, instance):
        try:
            self.volume = float(self.bagavolum.text) / 100
            self.volume = max(0.0, min(1.0, self.volume))
            
            self.menu_audio = App.get_running_app().root.get_screen('main_menu')
            self.menu_joc = App.get_running_app().root.get_screen('ScrPlay')
            
            if self.menu_audio.sound:
                self.menu_audio.sound.volume = self.volume
            if self.menu_joc.manele:
                self.menu_joc.manele.volume = self.volume
        except:
            self.bagavolum.text = 'Put numbers between 0-100'
            Clock.schedule_once(self.back1, 2)

    def back1(self, dt):
        self.bagavolum.text = ''

    def handle_save(self, instance):
        self.baga_volum_la_sunet_ca_sa_nu_surzesti(instance)

        try:
            with open('info.json', 'r') as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}
          
        data["volum"] = self.volume

        with open('info.json', 'w') as file:
            json.dump(data, file, indent = 4)
            
class Jumpscare(Screen):
    def __init__(self, name = 'jumpscare_'):
        super().__init__(name = name)
        
        sperietura = Image(source = 'titlu.png', size_hint = (1, 1), size = (300, 300))
        bcbtn = ScrButton(self, direction = 'right', goal = '', text = 'Back to main menu', size_hint = (.4, .1), pos_hint = {'center_x':0.25, 'center_y': 0.9})
        
        bcbtn.bind(on_press = self.jumpscares)
        bcbtn.bind(on_press = self.manele_pe_sistem)
        layout = FloatLayout()
        
        layout.add_widget(sperietura)
        layout.add_widget(bcbtn)
        
        self.add_widget(layout)
        
    def jumpscares(self, instance):
        self.manager.transition.direction = 'left'
        self.manager.current = 'main_menu'
        
    def manele_pe_sistem(self, instance):
        self.menu = App.get_running_app().root.get_screen('main_menu')
        if self.menu.sound:
            self.menu.sound.play()
        
class Falling_Round_Things(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(FirstScreen())
        sm.add_widget(Play_Menu())
        sm.add_widget(Option_Menu())
        sm.add_widget(Jumpscare())
        sm.add_widget(Modifying_Audio())
        
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
