from kivy.app import App
from kivy.uix.button import Button
from kivy.utils import platform
from kivy.clock import Clock
import os

class PDFTestApp(App):
    def build(self):
        # 화면 전체를 버튼으로 구성
        return Button(
            text="[PDF TEST]\n1. Put 'test.pdf' in Download folder\n2. Click this button",
            halign="center",
            font_size="20sp",
            on_release=self.open_pdf
        )

    def on_start(self):
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            # 기본 권한 요청
            request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])

    def open_pdf(self, instance):
        if platform != 'android':
            instance.text = "This test only works on Android"; return
        
        try:
            from jnius import autoclass
            from android.runnable import run_on_main_thread

            # 필수 클래스 로드
            PDFView = autoclass('com.github.barteksc.pdfviewer.PDFView')
            File = autoclass('java.io.File')
            LayoutParams = autoclass('android.view.ViewGroup$LayoutParams')
            mActivity = autoclass('org.kivy.android.PythonActivity').mActivity

            @run_on_main_thread
            def _show():
                try:
                    # 뷰어 생성 및 전체 화면 배치
                    pdf_view = PDFView(mActivity, None)
                    mActivity.addContentView(pdf_view, LayoutParams(-1, -1))
                    
                    # 휴대폰의 다운로드 폴더에 있는 test.pdf 파일을 대상으로 함
                    pdf_path = "/sdcard/Download/test.pdf"
                    if not os.path.exists(pdf_path):
                        # 표준 경로로 한번 더 시도
                        pdf_path = "/storage/emulated/0/Download/test.pdf"
                    
                    if os.path.exists(pdf_path):
                        file_obj = File(pdf_path)
                        pdf_view.fromFile(file_obj).enableSwipe(True).load()
                        instance.text = f"SUCCESS!\nOpening: {pdf_path}"
                    else:
                        instance.text = f"FILE NOT FOUND:\n{pdf_path}\nPlease put 'test.pdf' in Download folder."
                except Exception as e:
                    instance.text = f"NATIVE ERROR:\n{str(e)}"
            _show()
        except Exception as e:
            instance.text = f"PYJNIUS ERROR:\n{str(e)}"

if __name__ == '__main__':
    PDFTestApp().run()
