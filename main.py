from kivy.app import App
from kivy.uix.label import Label

class Step2_2App(App):
    def build(self):
        try:
            # openpyxl 로드 시도
            import openpyxl
            return Label(text='Step 2-2: openpyxl Load Success')
        except Exception as e:
            return Label(text=f'Step 2-2 Error: {str(e)}')

if __name__ == '__main__':
    Step2_2App().run()
