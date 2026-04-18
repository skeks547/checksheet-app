from kivy.app import App
from kivy.uix.label import Label

class Step2_4App(App):
    def build(self):
        try:
            # pycryptodome 로드 시도
            from Crypto.Cipher import AES
            return Label(text='Step 2-4: pycryptodome Load Success')
        except Exception as e:
            return Label(text=f'Step 2-4 Error: {str(e)}')

if __name__ == '__main__':
    Step2_4App().run()
