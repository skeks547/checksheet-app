from kivy.app import App
from kivy.uix.label import Label
import os

class Step2_1App(App):
    def build(self):
        try:
            # pyjnius 로드 시도
            from jnius import autoclass
            return Label(text='Step 2-1: pyjnius Load Success')
        except Exception as e:
            return Label(text=f'Step 2-1 Error: {str(e)}')

if __name__ == '__main__':
    Step2_1App().run()
