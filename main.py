import os
import shutil
import traceback
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.utils import platform
from kivy.clock import Clock

class PDFTestApp(App):
    def build(self):
        self.root_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        self.status_label = Label(
            text="[Graphics Stabilized Version]\n1. Grant Permission (if not done)\n2. Select PDF to test WebView", 
            size_hint_y=None, 
            height=300,
            halign='center'
        )
        self.root_layout.add_widget(self.status_label)
        
        self.perm_btn = Button(text="1. Grant Permission Screen", size_hint_y=None, height=120)
        self.perm_btn.bind(on_release=self.open_permission_settings)
        self.root_layout.add_widget(self.perm_btn)
        
        self.select_btn = Button(text="2. Select PDF and Show", size_hint_y=None, height=120)
        self.select_btn.bind(on_release=self.open_file_chooser)
        self.root_layout.add_widget(self.select_btn)
        
        self.webview = None
        return self.root_layout

    def open_permission_settings(self, instance):
        if platform != 'android': return
        try:
            from jnius import autoclass
            mActivity = autoclass('org.kivy.android.PythonActivity').mActivity
            Intent = autoclass('android.content.Intent')
            Settings = autoclass('android.provider.Settings')
            Uri = autoclass('android.net.Uri')
            uri = Uri.fromParts("package", mActivity.getPackageName(), None)
            intent = Intent(Settings.ACTION_MANAGE_APP_ALL_FILES_ACCESS_PERMISSION)
            intent.setData(uri)
            mActivity.startActivity(intent)
            self.status_label.text = "Permission requested.\nPlease allow and return."
        except Exception as e:
            self.status_label.text = f"Perm Err: {e}"

    def open_file_chooser(self, instance):
        path = "/storage/emulated/0" if platform == 'android' else os.getcwd()
        fc = FileChooserListView(path=path, filters=['*.pdf'])
        content = BoxLayout(orientation='vertical')
        content.add_widget(fc)
        select_btn = Button(text="Open Selected", size_hint_y=None, height=120)
        content.add_widget(select_btn)
        popup = Popup(title="Select PDF", content=content, size_hint=(0.9, 0.9))
        
        def on_select(btn):
            if fc.selection:
                popup.dismiss()
                self.start_pdf_process(fc.selection[0])
        select_btn.bind(on_release=on_select)
        popup.open()

    def start_pdf_process(self, file_path):
        self.status_label.text = f"File selected.\nPreparing internal engine..."
        Clock.schedule_once(lambda dt: self.copy_and_show(file_path), 0.5)

    def copy_and_show(self, src_path):
        try:
            from jnius import autoclass
            mActivity = autoclass('org.kivy.android.PythonActivity').mActivity
            internal_dir = mActivity.getFilesDir().getAbsolutePath()
            
            # File copy
            dest_path = os.path.join(internal_dir, "temp.pdf")
            if os.path.exists(dest_path): os.remove(dest_path)
            shutil.copy2(src_path, dest_path)
            
            # Engine copy
            dest_pdfjs = os.path.join(internal_dir, "pdfjs")
            src_pdfjs = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pdfjs")
            if not os.path.exists(dest_pdfjs) and os.path.exists(src_pdfjs):
                shutil.copytree(src_pdfjs, dest_pdfjs)

            self.status_label.text = "Initializing Isolated WebView..."
            Clock.schedule_once(lambda dt: self.init_webview(dest_path), 1.0)
        except Exception as e:
            self.status_label.text = f"Error: {e}"

    def init_webview(self, pdf_path):
        from android.runnable import run_on_main_thread
        @run_on_main_thread
        def _setup():
            try:
                from jnius import autoclass
                mActivity = autoclass('org.kivy.android.PythonActivity').mActivity
                
                if not self.webview:
                    # 1. Create WebView
                    self.webview = autoclass('android.webkit.WebView')(mActivity)
                    
                    # 2. Critical Fix: Force Software Layer BEFORE adding to view
                    # This prevents GPU/OpenGL conflict with Kivy
                    self.webview.setLayerType(1, None) # 1 = View.LAYER_TYPE_SOFTWARE
                    
                    # 3. Configure Settings
                    s = self.webview.getSettings()
                    s.setJavaScriptEnabled(True)
                    s.setAllowFileAccess(True)
                    s.setDomStorageEnabled(True)
                    
                    # 4. Add to Activity using addContentView (Standard Overlay)
                    params = autoclass('android.view.ViewGroup$LayoutParams')(-1, -1)
                    mActivity.addContentView(self.webview, params)
                
                # 5. Bring to front and load
                self.webview.setVisibility(0)
                self.webview.bringToFront()
                
                internal = mActivity.getFilesDir().getAbsolutePath()
                url = f"file://{internal}/pdfjs/web/viewer.html?file=file://{pdf_path}"
                self.webview.loadUrl(url)
                self.status_label.text = "Success! WebView Running."
            except Exception as e:
                self.status_label.text = f"WebView Err: {e}"
        _setup()

if __name__ == '__main__':
    PDFTestApp().run()
