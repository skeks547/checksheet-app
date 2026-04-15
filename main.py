import os
import json
import traceback
import subprocess
import socket
from openpyxl import load_workbook

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.recycleview import RecycleView
from kivy.properties import StringProperty, BooleanProperty, NumericProperty, DictProperty, ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.core.text import LabelBase
from kivy.utils import platform
from kivy.clock import Clock
from kivy.metrics import dp

# 안드로이드 키보드 설정
if platform == 'android':
    Window.softinput_mode = 'below_target'

# SMB 라이브러리
SMB_AVAILABLE = False
try:
    from smb.SMBConnection import SMBConnection
    SMB_AVAILABLE = True
except: pass

# 한글 폰트
try:
    FONT_NAME = "font.ttf"
    if os.path.exists(FONT_NAME):
        LabelBase.register(name="Roboto", fn_regular=FONT_NAME)
except: pass

SETTINGS_FILE = 'settings.json'
LOCAL_BASE = "/sdcard/Download/CheckSheet" if platform == 'android' else os.path.join(os.getcwd(), "CheckSheet_Data")
if not os.path.exists(LOCAL_BASE): os.makedirs(LOCAL_BASE)

class ListScreen(Screen):
    pass

class ViewerScreen(Screen):
    pass

class RowWidget(BoxLayout):
    no = StringProperty('')
    item_code = StringProperty('')
    quantity = StringProperty('')
    complete = BooleanProperty(False)
    shortage = BooleanProperty(False)
    rework = BooleanProperty(False)
    real_index = NumericProperty(0)

    def on_checkbox_active(self, checkbox_type):
        App.get_running_app().update_item_status(self.item_code, self.no, checkbox_type)

    def open_pdf(self):
        app = App.get_running_app()
        for i, d in enumerate(app.root.get_screen('list').ids.rv.data):
            if d['item_code'] == self.item_code and d['no'] == self.no:
                app.open_pdf_viewer(i)
                break

class CheckSheetRV(RecycleView):
    pass

class CheckSheetApp(App):
    excel_path = StringProperty('')
    pdf_folder_path = StringProperty('')
    pdf_source = StringProperty('local')
    excel_source = StringProperty('local')
    smb_config = DictProperty({'ip': '', 'user': '', 'pass': ''})
    
    # 뷰어 관련
    current_view_idx = NumericProperty(-1)
    touch_start_x = NumericProperty(0)
    
    # 정렬 지시자 (KV에서 바인딩용)
    sort_indicator_no = StringProperty('')
    sort_indicator_code = StringProperty('')
    sort_indicator_qty = StringProperty('')
    sort_indicator_comp = StringProperty('')
    sort_indicator_short = StringProperty('')
    sort_indicator_rew = StringProperty('')
    
    sort_states = {}

    def build(self):
        self.load_settings()
        sm = ScreenManager()
        sm.add_widget(ListScreen(name='list'))
        sm.add_widget(ViewerScreen(name='viewer'))
        return sm

    def on_start(self):
        if platform == 'android':
            Clock.schedule_once(self.ask_permissions, 1)
        if self.excel_path and os.path.exists(self.excel_path):
            self.load_excel_data(self.excel_path)

    def ask_permissions(self, dt):
        if platform == 'android':
            try:
                from android.permissions import request_permissions, Permission
                from jnius import autoclass
                request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE, Permission.INTERNET, Permission.ACCESS_NETWORK_STATE])
                Env = autoclass('android.os.Environment')
                if not Env.isExternalStorageManager():
                    Context = autoclass('org.kivy.android.PythonActivity').mActivity
                    Intent = autoclass('android.content.Intent'); Settings = autoclass('android.provider.Settings'); Uri = autoclass('android.net.Uri')
                    intent = Intent(Settings.ACTION_MANAGE_APP_ALL_FILES_ACCESS_PERMISSION)
                    uri = Uri.fromParts("package", Context.getPackageName(), None); intent.setData(uri)
                    Context.startActivity(intent)
            except: pass

    # --- 정렬 기능 ---
    def sort_by(self, column):
        rv = self.root.get_screen('list').ids.rv
        if not rv.data: return
        
        current = self.sort_states.get(column, None)
        new_state = 'desc' if current == 'asc' else 'asc'
        self.sort_states = {column: new_state} # 하나만 정렬 유지
        
        # 지시자 업데이트
        self.sort_indicator_no = " ▲" if column=='no' and new_state=='asc' else (" ▼" if column=='no' and new_state=='desc' else "")
        self.sort_indicator_code = " ▲" if column=='item_code' and new_state=='asc' else (" ▼" if column=='item_code' and new_state=='desc' else "")
        self.sort_indicator_qty = " ▲" if column=='quantity' and new_state=='asc' else (" ▼" if column=='quantity' and new_state=='desc' else "")
        self.sort_indicator_comp = " ▲" if column=='complete' and new_state=='asc' else (" ▼" if column=='complete' and new_state=='desc' else "")
        self.sort_indicator_short = " ▲" if column=='shortage' and new_state=='asc' else (" ▼" if column=='shortage' and new_state=='desc' else "")
        self.sort_indicator_rew = " ▲" if column=='rework' and new_state=='asc' else (" ▼" if column=='rework' and new_state=='desc' else "")

        def get_val(x):
            v = x.get(column, '')
            if column == 'quantity':
                try: return float(v)
                except: return 0
            return str(v).lower()

        rv.data = sorted(rv.data, key=get_val, reverse=(new_state == 'desc'))
        rv.refresh_from_data()

    # --- 상태 동기화 ---
    def update_item_status(self, item_code, no, status_type):
        rv = self.root.get_screen('list').ids.rv
        target_idx = -1
        for i, d in enumerate(rv.data):
            if d['item_code'] == item_code and d['no'] == no:
                target_idx = i; break
        
        if target_idx != -1:
            d = rv.data[target_idx]
            if status_type == 'complete':
                d['complete'] = not d['complete']
                if d['complete']: d['shortage'] = d['rework'] = False
            elif status_type == 'shortage':
                d['shortage'] = not d['shortage']
                if d['shortage']: d['complete'] = d['rework'] = False
            elif status_type == 'rework':
                d['rework'] = not d['rework']
                if d['rework']: d['complete'] = d['shortage'] = False
            
            rv.refresh_from_data()
            if self.root.current == 'viewer':
                self.update_viewer_buttons()

    def update_viewer_buttons(self):
        if self.current_view_idx < 0: return
        item = self.root.get_screen('list').ids.rv.data[self.current_view_idx]
        vs = self.root.get_screen('viewer')
        vs.ids.btn_comp.background_color = (0, 1, 0, 1) if item['complete'] else (0.3, 0.3, 0.3, 1)
        vs.ids.btn_short.background_color = (1, 1, 0, 1) if item['shortage'] else (0.3, 0.3, 0.3, 1)
        vs.ids.btn_rew.background_color = (1, 0, 0, 1) if item['rework'] else (0.3, 0.3, 0.3, 1)

    # --- PDF 뷰어 ---
    def open_pdf_viewer(self, index):
        self.current_view_idx = index
        self.root.current = 'viewer'
        self.load_viewer_pdf()

    def close_viewer(self):
        self.root.current = 'list'

    def load_viewer_pdf(self):
        if self.current_view_idx < 0: return
        rv_data = self.root.get_screen('list').ids.rv.data
        item = rv_data[self.current_view_idx]
        item_code = item['item_code']
        vs = self.root.get_screen('viewer')
        vs.ids.viewer_title.text = item_code
        self.update_viewer_buttons()
        
        local_path = os.path.join(LOCAL_BASE, f"{item_code}.pdf")
        if not os.path.exists(local_path) and self.pdf_source == 'smb':
            self.download_pdf_silently(item_code)
            return

        if platform == 'android':
            self.render_pdf_to_widget(local_path)
        else:
            if os.path.exists(local_path):
                if os.name == 'nt': os.startfile(local_path)
                else: subprocess.run(['xdg-open', local_path])

    def render_pdf_to_widget(self, path):
        try:
            from jnius import autoclass
            File = autoclass('java.io.File'); PFD = autoclass('android.os.ParcelFileDescriptor')
            PR = autoclass('android.graphics.pdf.PdfRenderer'); Bitmap = autoclass('android.graphics.Bitmap')
            f = File(path)
            if not f.exists(): 
                self.root.get_screen('viewer').ids.pdf_img.source = ""; return
            pfd = PFD.open(f, PFD.MODE_READ_ONLY); renderer = PR(pfd); page = renderer.openPage(0)
            w, h = page.getWidth() * 2, page.getHeight() * 2
            bitmap = Bitmap.createBitmap(w, h, Bitmap.Config.ARGB_8888)
            page.render(bitmap, None, None, page.RENDER_MODE_FOR_DISPLAY)
            tmp_img = os.path.join(LOCAL_BASE, "temp_view.png")
            out = autoclass('java.io.FileOutputStream')(tmp_img)
            bitmap.compress(Bitmap.CompressFormat.PNG, 100, out); out.close(); page.close(); renderer.close()
            img_widget = self.root.get_screen('viewer').ids.pdf_img
            img_widget.source = ""; img_widget.source = tmp_img; img_widget.reload()
        except: pass

    def download_pdf_silently(self, item_code):
        if not self.pdf_folder_path: return
        parts = self.pdf_folder_path.split("/", 1)
        share = parts[0]; sub = parts[1] if len(parts) > 1 else ""
        remote = os.path.join("/", sub, f"{item_code}.pdf").replace("\\", "/")
        local = os.path.join(LOCAL_BASE, f"{item_code}.pdf")
        def do_download(dt):
            try:
                conn = self.get_smb_conn_only()
                if conn:
                    with open(local, 'wb') as f: conn.retrieveFile(share, remote, f)
                    conn.close()
                    Clock.schedule_once(lambda x: self.load_viewer_pdf(), 0.1)
            except: pass
        Clock.schedule_once(do_download, 0.1)

    def get_smb_conn_only(self):
        try:
            ip = self.smb_config['ip']
            conn = SMBConnection(self.smb_config['user'], self.smb_config['pass'], "App", ip, use_ntlm_v2=True, is_direct_tcp=True)
            if conn.connect(ip, 445, timeout=3): return conn
        except: pass
        return None

    def on_viewer_swipe(self, direction):
        rv_data = self.root.get_screen('list').ids.rv.data
        if direction == 'right' and self.current_view_idx > 0:
            self.current_view_idx -= 1; self.load_viewer_pdf()
        elif direction == 'left' and self.current_view_idx < len(rv_data) - 1:
            self.current_view_idx += 1; self.load_viewer_pdf()

    def on_viewer_touch_down(self, touch):
        self.touch_start_x = touch.x

    def on_viewer_touch_up(self, touch):
        dx = touch.x - self.touch_start_x
        if abs(dx) > dp(100):
            self.on_viewer_swipe('right' if dx > 0 else 'left')

    # --- 공통 유틸리티 ---
    def load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                    d = json.load(f); self.excel_path = d.get('excel_path', ''); self.pdf_folder_path = d.get('pdf_folder_path', '')
                    self.pdf_source = d.get('pdf_source', 'local'); self.excel_source = d.get('excel_source', 'local')
                    self.smb_config = d.get('smb_config', {'ip':'','user':'','pass':''})
            except: pass

    def save_settings(self):
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump({'excel_path': self.excel_path, 'pdf_folder_path': self.pdf_folder_path, 'pdf_source': self.pdf_source, 'excel_source': self.excel_source, 'smb_config': self.smb_config}, f, ensure_ascii=False)

    def load_excel_data(self, path):
        try:
            wb = load_workbook(path, data_only=True); ws = wb.active; rows = list(ws.rows)
            headers = [str(cell.value).strip().lower() for cell in rows[0]]
            idx_no, idx_code, idx_qty = headers.index('no'), headers.index('품목코드'), headers.index('수량')
            rv_data = []
            for i, row in enumerate(rows[1:]):
                rv_data.append({
                    'no': str(row[idx_no].value or ''), 'item_code': str(row[idx_code].value or ''), 'quantity': str(row[idx_qty].value or ''),
                    'complete': str(ws.cell(row=i+2, column=headers.index('완료')+1).value or '').upper() == 'V' if '완료' in headers else False,
                    'shortage': str(ws.cell(row=i+2, column=headers.index('수량부족')+1).value or '').upper() == 'V' if '수량부족' in headers else False,
                    'rework': str(ws.cell(row=i+2, column=headers.index('재작업')+1).value or '').upper() == 'V' if '재작업' in headers else False,
                    'real_index': i
                })
            self.root.get_screen('list').ids.rv.data = rv_data
        except: pass

    def save_to_excel(self):
        if not self.excel_path: return
        try:
            wb = load_workbook(self.excel_path); ws = wb.active; headers = [str(cell.value).strip().lower() for cell in ws[1]]
            cols = {'완료':-1,'수량부족':-1,'재작업':-1}
            for k in cols: 
                if k in headers: cols[k] = headers.index(k)+1
            for d in self.root.get_screen('list').ids.rv.data:
                row_idx = d['real_index']+2
                if cols['완료']>0: ws.cell(row=row_idx, column=cols['완료']).value = 'V' if d['complete'] else ''
                if cols['수량부족']>0: ws.cell(row=row_idx, column=cols['수량부족']).value = 'V' if d['shortage'] else ''
                if cols['재작업']>0: ws.cell(row=row_idx, column=cols['재작업']).value = 'V' if d['rework'] else ''
            wb.save(self.excel_path); self.show_error_popup("저장 완료")
        except: pass

    def show_error_popup(self, msg):
        Popup(title="알림", content=Label(text=msg, halign='center'), size_hint=(0.8, 0.4)).open()

    def select_source(self, mode):
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))
        popup = Popup(title="파일 출처 선택", content=content, size_hint=(0.85, 0.5))
        def on_choice(choice):
            popup.dismiss()
            if choice == 'local': self.open_local_browser(mode)
            else: self.open_smb_shares_browser(mode)
        content.add_widget(Button(text="폰 저장소", on_release=lambda x: on_choice('local')))
        content.add_widget(Button(text="PC 공유폴더", on_release=lambda x: on_choice('smb')))
        popup.open()

    def open_smb_shares_browser(self, mode):
        conn = self.get_smb_conn_only()
        if not conn: self.show_error_popup("SMB 접속 실패"); return
        content = BoxLayout(orientation='vertical'); scroll = ScrollView(); list_box = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(5))
        list_box.bind(minimum_height=list_box.setter('height')); scroll.add_widget(list_box)
        popup = Popup(title="공유폴더 선택", content=content, size_hint=(0.95, 0.95))
        try:
            for s in conn.listShares():
                if s.isSpecial or s.name.endswith('$'): continue
                btn = Button(text=f"📁 {s.name}", size_hint_y=None, height=dp(90))
                btn.bind(on_release=lambda b, s=s: self.open_smb_files_browser(conn, s.name, "/", mode, popup))
                list_box.add_widget(btn)
        except: pass
        content.add_widget(scroll); content.add_widget(Button(text="취소", size_hint_y=None, height=dp(80), on_release=lambda x: (conn.close(), popup.dismiss())))
        popup.open()

    def open_smb_files_browser(self, conn, share, path, mode, parent):
        content = BoxLayout(orientation='vertical'); scroll = ScrollView(); list_box = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(2))
        list_box.bind(minimum_height=list_box.setter('height')); scroll.add_widget(list_box)
        popup = Popup(title=f"SMB: {share}{path}", content=content, size_hint=(0.95, 0.95))
        def refresh(cp):
            list_box.clear_widgets()
            if cp != "/":
                btn = Button(text=".. 상위폴더", size_hint_y=None, height=dp(80))
                btn.bind(on_release=lambda x: refresh(os.path.dirname(cp.rstrip("/")) or "/")); list_box.add_widget(btn)
            for f in conn.listPath(share, cp):
                if f.filename in ['.', '..']: continue
                btn = Button(text=f"{'📁' if f.isDirectory else '📄'} {f.filename}", size_hint_y=None, height=dp(90))
                btn.bind(on_release=lambda b, f=f: on_click(cp, f)); list_box.add_widget(btn)
        def on_click(cp, f):
            new_p = os.path.join(cp, f.filename).replace("\\", "/")
            if f.isDirectory:
                if mode == 'dir': self.pdf_folder_path = f"{share}{new_p}"; self.pdf_source='smb'; self.save_settings(); popup.dismiss(); parent.dismiss(); conn.close()
                else: refresh(new_p)
            else:
                if mode == 'file':
                    local = os.path.join(LOCAL_BASE, f.filename)
                    with open(local, 'wb') as lf: conn.retrieveFile(share, new_p, lf)
                    self.excel_path = local; self.excel_source='smb'; self.load_excel_data(local); self.save_settings(); popup.dismiss(); parent.dismiss(); conn.close()
        refresh(path); content.add_widget(scroll); content.add_widget(Button(text="닫기", size_hint_y=None, height=dp(80), on_release=lambda x: popup.dismiss()))
        popup.open()

    def open_local_browser(self, mode):
        start_p = "/sdcard" if platform == 'android' else os.getcwd()
        content = BoxLayout(orientation='vertical'); fc = FileChooserListView(path=start_p)
        if mode == 'dir': fc.dirselect = True
        popup = Popup(title="파일 선택", content=content, size_hint=(0.95, 0.95))
        def on_select(instance):
            if fc.selection:
                path = fc.selection[0]
                if mode == 'file': self.excel_path = path; self.excel_source='local'; self.load_excel_data(path)
                else: self.pdf_folder_path = path; self.pdf_source='local'
                self.save_settings(); popup.dismiss()
        content.add_widget(fc); content.add_widget(Button(text="선택 완료", size_hint_y=None, height=dp(70), on_release=on_select))
        popup.open()

    def open_smb_settings(self):
        scroll = ScrollView(size_hint=(1, 1)); content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20), size_hint_y=None)
        content.bind(minimum_height=content.setter('height')); inputs = {}
        fields = [('ip', 'IP 주소'), ('user', 'ID (계정)'), ('pass', 'PW (비번)')]
        for key, hint in fields:
            content.add_widget(Label(text=hint, size_hint_y=None, height=dp(40), halign='left', text_size=(Window.width*0.85, None)))
            ti = TextInput(text=self.smb_config.get(key, ''), multiline=False, size_hint_y=None, height=dp(100), font_size='22sp')
            if key == 'pass': ti.password = True
            content.add_widget(ti); inputs[key] = ti
        popup = Popup(title="SMB 설정", content=scroll, size_hint=(0.95, 0.9)); scroll.add_widget(content)
        def save(instance):
            self.smb_config = {k: v.text.strip() for k, v in inputs.items()}; self.save_settings(); popup.dismiss()
        content.add_widget(Button(text="저장", size_hint_y=None, height=dp(90), on_release=save, background_color=(0, 0.6, 0.8, 1)))
        popup.open()

if __name__ == '__main__':
    CheckSheetApp().run()
