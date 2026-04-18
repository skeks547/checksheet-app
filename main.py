from kivy.app import App
from kivy.uix.label import Label

class Step2_5App(App):
    def build(self):
        try:
            # android 패키지 로드 시도
            import android
            return Label(text='Step 2-5: android package Load Success')
        except Exception as e:
            return Label(text=f'Step 2-5 Error: {str(e)}')

if __name__ == '__main__':
    Step2_5App().run()
