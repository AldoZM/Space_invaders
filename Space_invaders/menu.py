from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout

class LoginScreen(GridLayout):
    
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 1
        self.add_widget(Lable(text='Hola!'))
        self.texto = TextInput(multiline= False)    
        self.add_widget(self.texto)

class MyApp(App):

    def build(self):
        return Menu()

if __name__ == '__menu__':
    Correr().run()















#clase.clear()
