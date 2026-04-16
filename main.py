import os
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import platform
from kivy.clock import Clock

class PDFTestApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        self.btn = Button(text="Open PDF (4000500638.pdf)", size_hint_y=0.2)
        self.btn.bind(on_release=self.open_native_pdf)
        self.status = Label(text="Click button to test PDF viewer")
        
        self.layout.add_widget(self.status)
        self.layout.add_widget(self.btn)
        return self.layout

    def on_start(self):
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])

    def open_native_pdf(self, instance):
        # 테스트용 PDF 경로 (저장소에 실존하는 파일)
        pdf_path = os.path.join(os.path.dirname(__file__), "pdfss", "4000500638.pdf")
        
        if not os.path.exists(pdf_path):
            self.status.text = f"File not found: {pdf_path}"
            return

        if platform == 'android':
            try:
                from jnius import autoclass
                from android.runnable import run_on_main_thread

                @run_on_main_thread
                def _show():
                    try:
                        mActivity = autoclass('org.kivy.android.PythonActivity').mActivity
                        File = autoclass('java.io.File')
                        # 대소문자 주의: com.github.barteksc.pdfviewer.PDFView
                        PDFView = autoclass('com.github.barteksc.pdfviewer.PDFView')
                        
                        pdf_view = PDFView(mActivity, None)
                        mActivity.addContentView(pdf_view, 
                            autoclass('android.view.ViewGroup$LayoutParams')(-1, -1))
                        
                        file = File(pdf_path)
                        pdf_view.fromFile(file).load()
                        self.status.text = "PDF Viewer loaded successfully"
                    except Exception as e:
                        self.status.text = f"Native Error: {str(e)}"
                _show()
            except Exception as e:
                self.status.text = f"Pyjnius Error: {str(e)}"
        else:
            self.status.text = "Native PDF viewer only works on Android"

if __name__ == '__main__':
    PDFTestApp().run()
