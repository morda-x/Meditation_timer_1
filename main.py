
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.clock import Clock

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from kivy.uix.image import Image # все управление ведем с помощью нажатия на картинки
from kivy.uix.behaviors import ButtonBehavior  # чтобы использовать кнопку картинку как кнопку
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.togglebutton import ToggleButton

from kivy.config import Config
Config.set('graphics', 'width', '350')
Config.set('graphics', 'height', '600')


class ScreenManagment(ScreenManager): pass


class MainScreen(Screen): pass


class KirtanScreen(Screen): pass


class MeditationScreen(Screen): pass


class SetupScreen(Screen): pass


class Contaner(BoxLayout): pass


class AddPractice(ButtonBehavior, Label): pass


class Play_Stop_Btn(ButtonBehavior, Image): pass


class Kirtan(ButtonBehavior, Label): pass


class KirtanSettings(ButtonBehavior, Label): pass


class MyButton(BoxLayout, ButtonBehavior): pass


class ImageBtn(ButtonBehavior, Image): pass


class LabelBtn(ButtonBehavior, Label): pass

class Practice(BoxLayout):
    def ChangeSettings(self, *args):
        self.p = Builder.load_file('change_settings.kv')
        self.p.ids.SaveBtn.bind(on_release=self.SaveSettings)
        self.p.ids.CloseBtn.bind(on_release=self.DelPractice)
        self.p.open()
        # два тика позволяют обновить виджеты !!!!!!!!!!!
        Clock.tick()
        Clock.tick()

        # нажмем на кнопку с временем нашего элемента
        for e in self.p.ids.scr.children[0].children:
            if e.text == self.time: e.state='down'
            else: e.state='normal'
        #вызовем принудительное обновление элементов
        # прокрутим скролл на центр
        # найдем выделенный элемент
        k = ToggleButton()
        for e in self.p.ids.scr.children[0].children:
            if e.state == 'down':
                k = e
                #print('e.pos', e.pos)
        x_pos_elem = k.pos[0]  # отступ элемента сетки от начала сетки слева
        a_elem = k.size[0]  # ширина одного элемента по х
        w_scroll_x = self.p.ids.scr.size[0]  # размер окна прокрутки по х
        n_elem = len(self.p.ids.scr.children[0].children)  # общее число элементов
        #print('x_pos_elem', x_pos_elem)
        #print('a_elem', a_elem)
        #print('w_scroll_x', w_scroll_x)
        #print('n_elem', n_elem)
        i = 0
        while i <= 1:
            # print(i)
            self.p.ids.scr.scroll_x = i
            if (x_pos_elem + a_elem / 2 - (a_elem * n_elem - w_scroll_x) * i) < (w_scroll_x / 2):
                #print('прокрутка завершена', i)
                break
            i += 0.01



    def SaveSettings(self, *args):
        if self.p.ids.kirt.is_pressed == 1: type = 'Киртан'
        if self.p.ids.med.is_pressed == 1: type = 'Медитация'
        time = ''

        for e in self.p.ids.scr.children[0].children:
            if e.state == 'down':
                time = e.text
        if time == '':
            # self.p.dismiss()
            # self.p.ids.SaveBtn.bc = (0,0,0,1)
            pass
        else:
            # print(type)
            # print(time)
            self.p.dismiss()
            #print(self)
            k = self
            k.type = type
            k.time = time
            if k.type == 'Киртан': k.contur_color = (255 / 255, 215 / 255, 0 / 255, 1)
            if k.type == 'Медитация': k.contur_color = (0 / 255, 255 / 255, 127 / 255, 1)

    def DelPractice(self, *args):

        self.p.dismiss()
        self.parent.remove_widget(self)

    def StartPractice(self):
        self.p = Builder.load_file('start_practice.kv')
        self.p.ids.ppbtn.bind(on_press=self.PlayPause)
        self.p.open()

    def PlayPause(self, *args):
        print('jjj')
        if self.p.ids.ppbtn.stat == 'play':
            self.p.ids.ppbtn.stat = 'pause'
            self.p.ids.ppbtn.source = 'image/play.png'
        if self.p.ids.ppbtn.stat == 'pause':
            self.p.ids.ppbtn.stat = 'play'
            self.p.ids.ppbtn.source = 'image/play_pressed.png'



class GorScroll(ScrollView):
    def __init__(self, **kwargs):
        super(GorScroll, self).__init__(**kwargs)
        sw=self
        sw.do_scroll_x = True
        sw.do_scroll_y = False

        g=GridLayout()

        g.rows=1
        g.size_hint=(None,1)
        g.bind(minimum_width=g.setter('width'))
        for i in range(1, 20):
            l = Builder.load_file('toggle_btn.kv')
            l.text = str(i * 5)
            if l.text=='15':
                l.state = 'down'
            g.add_widget(l)

        sw.add_widget(g)



class Place_for_practice(GridLayout):


    def ShowPopup(self):

        self.p = Builder.load_file('timer_settings.kv')
        self.p.ids.SaveBtn.bind(on_release=self.Create_practice)
        self.p.ids.CloseBtn.bind(on_release=self.p.dismiss)
        self.p.open()
        #print(p)


    def Create_practice(self, *args):
        if self.p.ids.kirt.is_pressed == 1: type='Киртан'
        if self.p.ids.med.is_pressed == 1: type = 'Медитация'
        time=''

        for e in self.p.ids.scr.children[0].children:
            if e.state == 'down':
                time=e.text
        if time=='':
            #self.p.dismiss()
            #self.p.ids.SaveBtn.bc = (0,0,0,1)
            pass
        else:
            #print(type)
            #print(time)
            self.p.dismiss()
            k = Builder.load_file('practice.kv')
            k.type=type
            k.time=time
            if k.type =='Киртан':k.contur_color = (255/255, 215/255, 0/255, 1)
            if k.type == 'Медитация': k.contur_color = (0/255, 255/255, 127/255, 1)
            self.add_widget(k)

class MyApp(App):
    def build(self):
        #print(self.root.children[0].ids.pfp.children)
        f= open("my_practices.txt", "r")
        lines = f.readlines()
        #print(lines)
        new_lines=[]
        for l in lines:
            new_lines.append(l.rstrip().split(','))
       # print(new_lines)
        for i in new_lines:

            p=Builder.load_file('practice.kv')
            if i[0] == 'Киртан': p.contur_color = (255 / 255, 215 / 255, 0 / 255, 1)
            if i[0] == 'Медитация': p.contur_color = (0 / 255, 255 / 255, 127 / 255, 1)
            p.type=i[0]
            p.time=i[1]
            self.root.children[0].ids.pfp.add_widget(p)



    def on_stop(self, *args):
        #print(self.root.children[0].ids.pfp.children)
        practices = self.root.children[0].ids.pfp.children
        f = open('my_practices.txt', 'w')
        for pr in reversed(practices):
            f.write(pr.type +','+ pr.time+'\n')
        f.close()

MyApp().run()

