from kivy.app import App
from kivy.uix.label import Label
from kivy.utils import platform
from kivy.clock import Clock
import os

class TestApp(App):
    def build(self):
        return Label(text="PDF Viewer Test Loading...")

    def on_start(self):
        if platform == 'android':
            # 권한 요청 후 1초 뒤 실행
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
            Clock.schedule_once(self.open_pdf, 1)

    def open_pdf(self, dt):
        try:
            from jnius import autoclass
            from android.runnable import run_on_main_thread

            @run_on_main_thread
            def run():
                try:
                    mActivity = autoclass('org.kivy.android.PythonActivity').mActivity
                    PDFView = autoclass('com.github.barteksc.pdfviewer.PDFView')
                    File = autoclass('java.io.File')
                    LayoutParams = autoclass('android.view.ViewGroup$LayoutParams')

                    pdfView = PDFView(mActivity, None)
                    mActivity.addContentView(pdfView, LayoutParams(-1, -1))

                    # 프로젝트 내부의 실제 파일 경로 사용
                    pdf_path = os.path.join(os.path.dirname(__file__), "pdf", "4000500638.pdf")
                    
                    if os.path.exists(pdf_path):
                        file = File(pdf_path)
                        pdfView.fromFile(file).enableSwipe(True).load()
                    else:
                        print(f"DEBUG: File not found at {pdf_path}")
                except Exception as e:
                    print(f"DEBUG: Native Error: {e}")
            run()
        except Exception as e:
            print(f"DEBUG: Pyjnius Error: {e}")

if __name__ == '__main__':
    TestApp().run()
