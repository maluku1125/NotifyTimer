import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import keyboard
import threading
import sv_ttk
import webbrowser
import sys
import os

import config
from timer_core import TimerCore
from audio import play_text_to_speech, play_ding_sound
from notifier import send_windows_notification

class TimerRow:
    def __init__(self, parent_tab, index, settings, app):
        self.index = index
        self.app = app
        self.core = TimerCore(index)
        
        self.hour_var = tk.StringVar(value=settings.get('hours', '00'))
        self.minute_var = tk.StringVar(value=settings.get('minutes', '00'))
        self.second_var = tk.StringVar(value=settings.get('seconds', '00'))
        self.message_var = tk.StringVar(value=settings.get('message', '輸入語音內容'))
        self.notify_os_var = tk.BooleanVar(value=settings.get('notify_os', False))
        self.play_voice_var = tk.BooleanVar(value=settings.get('play_voice', True))
        
        self.frame = ttk.Frame(parent_tab)
        self.frame.pack(fill='x', pady=12)
        
        self.center_frame = ttk.Frame(self.frame)
        self.center_frame.pack(anchor='center')
        
        ttk.Label(self.center_frame, text=f"計時器 {index+1}", font=app.font_bold, foreground="#56b6c2").pack(side='left', padx=(0, 10))
        
        self.entry_hour = ttk.Entry(self.center_frame, width=3, textvariable=self.hour_var, justify='center', font=app.font)
        self.entry_hour.pack(side='left')
        ttk.Label(self.center_frame, text="時", font=app.font).pack(side='left', padx=3)
        
        self.entry_minute = ttk.Entry(self.center_frame, width=3, textvariable=self.minute_var, justify='center', font=app.font)
        self.entry_minute.pack(side='left')
        ttk.Label(self.center_frame, text="分", font=app.font).pack(side='left', padx=3)
        
        self.entry_second = ttk.Entry(self.center_frame, width=3, textvariable=self.second_var, justify='center', font=app.font)
        self.entry_second.pack(side='left')
        ttk.Label(self.center_frame, text="秒", font=app.font).pack(side='left', padx=(3, 10))
        
        ttk.Label(self.center_frame, text="提醒內容:", font=app.font, foreground="#9da5b4").pack(side='left', padx=(0, 5))
        # 限制提醒內容最多 20 個字元
        vcmd = (app.root.register(lambda text: len(text) <= 20), '%P')
        self.entry_message = ttk.Entry(self.center_frame, width=15, textvariable=self.message_var, font=app.font, validate='key', validatecommand=vcmd)
        self.entry_message.pack(side='left', padx=2)
        
        self.check_voice = ttk.Checkbutton(self.center_frame, text="語音", variable=self.play_voice_var, style="Toggle.TButton")
        self.check_voice.pack(side='left', padx=(15, 5))
        
        self.check_notify = ttk.Checkbutton(self.center_frame, text="通知", variable=self.notify_os_var, style="Toggle.TButton")
        self.check_notify.pack(side='left', padx=(0, 15))
        
        self.start_button = ttk.Button(self.center_frame, text='▶ 開始', command=self.start, width=8, style="Accent.TButton")
        self.start_button.pack(side='left', padx=5)
        
        self.stop_button = ttk.Button(self.center_frame, text='■ 停止', command=self.stop, width=8)
        self.stop_button.pack(side='left', padx=5)
        
        self.update_ui_state()

    def start(self):
        if self.core.running:
            return
            
        h = self.hour_var.get()
        m = self.minute_var.get()
        s = self.second_var.get()
        msg = self.message_var.get()
        
        if self.core.start(h, m, s, msg):
            self.update_ui_state()
            self.app.save_current_settings()
            
    def stop(self):
        self.core.stop()
        self.hour_var.set(self.core.original_hours)
        self.minute_var.set(self.core.original_minutes)
        self.second_var.set(self.core.original_seconds)
        self.update_ui_state()
        
    def tick(self):
        if not self.core.running:
            return
            
        remaining = self.core.get_remaining_time()
        
        if remaining <= 0:
            self.core.stop()
            self.hour_var.set(self.core.original_hours)
            self.minute_var.set(self.core.original_minutes)
            self.second_var.set(self.core.original_seconds)
            self.update_ui_state()
            
            msg = self.core.message
            do_notify = self.notify_os_var.get()
            do_voice = self.play_voice_var.get()
            
            threading.Thread(target=self.play_alarm, args=(msg, do_notify, do_voice), daemon=True).start()
        else:
            hrs_str, mins_str, secs_str = self.core.get_remaining_time_formatted()
            self.hour_var.set(hrs_str)
            self.minute_var.set(mins_str)
            self.second_var.set(secs_str)
            
    def play_alarm(self, message, do_notify, do_voice):
        if do_notify:
            send_windows_notification("倒數計時結束！", message)
            
        if do_voice:
            if not message or not message.strip():
                play_ding_sound()
            else:
                play_text_to_speech(message)

    def update_ui_state(self):
        if self.core.running:
            self.entry_hour.state(['disabled'])
            self.entry_minute.state(['disabled'])
            self.entry_second.state(['disabled'])
            self.entry_message.state(['disabled'])
            self.check_voice.state(['disabled'])
            self.check_notify.state(['disabled'])
            self.start_button.state(['disabled'])
        else:
            self.entry_hour.state(['!disabled'])
            self.entry_minute.state(['!disabled'])
            self.entry_second.state(['!disabled'])
            self.entry_message.state(['!disabled'])
            self.check_voice.state(['!disabled'])
            self.check_notify.state(['!disabled'])
            self.start_button.state(['!disabled'])
            
    def get_settings(self):
        return {
            'hours': self.core.original_hours if self.core.running else self.hour_var.get(),
            'minutes': self.core.original_minutes if self.core.running else self.minute_var.get(),
            'seconds': self.core.original_seconds if self.core.running else self.second_var.get(),
            'message': self.core.message if self.core.running else self.message_var.get(),
            'notify_os': self.notify_os_var.get(),
            'play_voice': self.play_voice_var.get()
        }


class TimerApp:
    @staticmethod
    def _resource_path(relative_path):
        """取得資源的絕對路徑（支援 PyInstaller 打包後的環境）。"""
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)

    def __init__(self, root):
        self.root = root
        self.root.title("NotifyTimer - 倒計時提醒 V2.1.0")
        self.root.geometry("920x450")
        self.root.resizable(False, False)
        
        # 設定視窗圖標（標題列 + 工作列）
        icon_path = self._resource_path('bug.ico')
        if os.path.exists(icon_path):
            self.root.iconbitmap(icon_path)
            # 用 wm_iconphoto 確保工作列圖標也顯示正確
            img = Image.open(icon_path)
            photo = ImageTk.PhotoImage(img)
            self.root.wm_iconphoto(True, photo)
        
        self.font = ("Microsoft JhengHei", 12)
        self.font_bold = ("Microsoft JhengHei", 12, "bold")
        self.font_title = ("Microsoft JhengHei", 16, "bold")

        self.app_config = config.load_app_config()
        sv_ttk.set_theme(self.app_config.get('theme', 'dark'))
        
        self.apply_custom_styles()
        
        self.settings = config.load_settings()
        self.timers = []
        self.hotkey_vars = []
        
        self.setup_ui()
        self.setup_hotkeys()
        self.start_tick_loop()

    def apply_custom_styles(self):
        # Override sv-ttk defaults to enforce Microsoft JhengHei 
        style = ttk.Style()
        style.configure('.', font=self.font)
        style.configure('TButton', font=self.font)
        style.configure('TLabel', font=self.font)
        style.configure('TEntry', font=self.font)
        style.configure('TCheckbutton', font=self.font)
        style.configure('TRadiobutton', font=self.font)
        style.configure('TNotebook.Tab', font=self.font_bold, padding=[10, 5])

    def setup_ui(self):
        header = ttk.Frame(self.root, padding=(20, 15))
        header.pack(fill='x')
        ttk.Label(header, text="NotifyTimer", font=self.font_title).pack(side='left')
    
        main_container = ttk.Frame(self.root, padding=(20, 0))
        main_container.pack(fill='both', expand=True)
        
        notebook = ttk.Notebook(main_container)
        
        # --- TAB: Timers ---
        self.timer_tab = ttk.Frame(notebook, padding=15)
        notebook.add(self.timer_tab, text=' 計時設定 ')
        for i in range(5):
            row = TimerRow(self.timer_tab, i, self.settings['timers'][i], self)
            self.timers.append(row)
            
        # --- TAB: Hotkeys ---
        self.hotkey_tab = ttk.Frame(notebook, padding=25)
        notebook.add(self.hotkey_tab, text=' 快捷鍵管理 ')
        hotkey_inner = ttk.Frame(self.hotkey_tab)
        hotkey_inner.pack(anchor='center', expand=True)
        
        self.hotkey_entries = []
        self.hotkey_record_buttons = []
        self._recording_index = None
        self._recording_hook = None
        self._recorded_keys = set()
        self._last_recorded_text = ''

        for i in range(5):
             ttk.Label(hotkey_inner, text=f"快捷鍵 {i+1}:", font=self.font_bold, foreground="#56b6c2").grid(row=i, column=0, pady=10, padx=(0, 20), sticky="e")
             var = tk.StringVar(value=self.settings['hotkeys'][i])
             self.hotkey_vars.append(var)
             entry = ttk.Entry(hotkey_inner, textvariable=var, font=self.font, width=20, justify='center')
             entry.grid(row=i, column=1, pady=10, padx=10)
             entry.configure(state='readonly')
             self.hotkey_entries.append(entry)
             rec_btn = ttk.Button(hotkey_inner, text='錄製', command=lambda idx=i: self.start_hotkey_recording(idx))
             rec_btn.grid(row=i, column=2, pady=10, padx=5)
             self.hotkey_record_buttons.append(rec_btn)
             ttk.Button(hotkey_inner, text='儲存', command=lambda idx=i: self.update_hotkey(idx)).grid(row=i, column=3, pady=10, padx=5)
             
        # --- TAB: Settings ---
        self.setting_tab = ttk.Frame(notebook, padding=25)
        notebook.add(self.setting_tab, text=' 系統設定 ')
        self.setup_setting_tab()
             
        # --- TAB: About/Notes ---
        self.note_tab = ttk.Frame(notebook, padding=25)
        notebook.add(self.note_tab, text=' 說明文件 ')
        self.setup_note_tab()
             
        notebook.pack(expand=True, fill='both')

    def setup_setting_tab(self):
        setting_inner = ttk.Frame(self.setting_tab)
        setting_inner.pack(anchor='center', expand=True)
        
        # Save Path
        ttk.Label(setting_inner, text="設定檔存檔路徑:", font=self.font_bold, foreground="#56b6c2").grid(row=0, column=0, pady=15, padx=(0, 20), sticky="e")
        self.save_path_var = tk.StringVar(value=self.app_config.get('save_path', ''))
        path_entry = ttk.Entry(setting_inner, textvariable=self.save_path_var, width=35, state='readonly', font=self.font)
        path_entry.grid(row=0, column=1, pady=15, padx=10)
        ttk.Button(setting_inner, text='瀏覽', command=self.browse_save_path).grid(row=0, column=2, pady=15, padx=10)
        
        # Theme
        ttk.Label(setting_inner, text="介面主題配色:", font=self.font_bold, foreground="#56b6c2").grid(row=1, column=0, pady=15, padx=(0, 20), sticky="e")
        theme_frame = ttk.Frame(setting_inner)
        theme_frame.grid(row=1, column=1, pady=15, padx=10, sticky="w")
        self.theme_var = tk.StringVar(value=self.app_config.get('theme', 'dark'))
        ttk.Radiobutton(theme_frame, text="深色 (Dark)", variable=self.theme_var, value="dark").pack(side='left', padx=(0, 15))
        ttk.Radiobutton(theme_frame, text="淺色 (Light)", variable=self.theme_var, value="light").pack(side='left')
        
        # Apply button
        btn_frame = ttk.Frame(setting_inner)
        btn_frame.grid(row=2, column=0, columnspan=3, pady=(30, 0))
        ttk.Button(btn_frame, text="儲存並套用設定", style="Accent.TButton", command=self.apply_settings, width=15).pack()

    def browse_save_path(self):
        directory = filedialog.askdirectory(initialdir=self.save_path_var.get(), title="選擇設定檔儲存資料夾")
        if directory:
            self.save_path_var.set(directory)

    def apply_settings(self):
        new_theme = self.theme_var.get()
        new_path = self.save_path_var.get()
        
        # Apply theme immediately
        sv_ttk.set_theme(new_theme)
        self.apply_custom_styles()
        
        # Save config
        self.app_config['theme'] = new_theme
        self.app_config['save_path'] = new_path
        if config.save_app_config(self.app_config):
            self.save_current_settings()
            messagebox.showinfo("成功", "系統設定已儲存並套用！\n若更改了儲存資料夾，設定也已在新資料夾同步。")
        else:
            messagebox.showerror("錯誤", "儲存系統設定失敗。")

    def setup_note_tab(self):
        note_inner = ttk.Frame(self.note_tab)
        note_inner.pack(anchor='center', expand=True)
        
        instructions = [
            ("快速鍵用法", "倒數結束後，根據選取狀況會播放語音或發送通知。"),
            ("設定儲存位置", "您可以在「系統設定」標籤頁中自訂設定檔的儲存資料夾。"),
            ("原作者", "諭諭"),
            ("Discord", "歡迎加入TMS新楓之谷 Discord 群!")
        ]
        
        for i in range(4):
             ttk.Label(note_inner, text=f"{instructions[i][0]}", font=self.font_bold, foreground="#56b6c2").grid(row=i, column=0, sticky='e', pady=12, padx=(0,15))
             ttk.Label(note_inner, text=instructions[i][1], font=self.font).grid(row=i, column=1, sticky='w', pady=12)
             
        # Hyperlink properly
        ttk.Label(note_inner, text="邀請連結", font=self.font_bold, foreground="#56b6c2").grid(row=4, column=0, sticky='e', pady=12, padx=(0,15))
        link_label = ttk.Label(note_inner, text="https://discord.gg/maplestory-tw", font=self.font, foreground="#5294e2", cursor="hand2")
        link_label.grid(row=4, column=1, sticky='w', pady=12)
        link_label.bind("<Button-1>", lambda e: webbrowser.open_new("https://discord.gg/maplestory-tw"))

    def setup_hotkeys(self):
        for i in range(5):
            self.register_hotkey(i, self.settings['hotkeys'][i])

    def register_hotkey(self, index, hotkey):
        def on_hotkey():
            self.root.after(0, self.timers[index].start)
            
        try:
             keyboard.add_hotkey(hotkey, on_hotkey)
        except Exception as e:
             print(f"Error binding hotkey {hotkey}: {e}")

    def start_hotkey_recording(self, index):
        """開始錄製快捷鍵：監聽鍵盤事件並即時顯示組合鍵"""
        # 如果已在錄製中，先停止
        if self._recording_index is not None:
            self.stop_hotkey_recording()

        self._recording_index = index
        self._recorded_keys = set()
        self._last_recorded_text = ''

        # 更新 UI 狀態
        self.hotkey_entries[index].configure(state='normal')
        self.hotkey_vars[index].set('請按下快捷鍵...')
        self.hotkey_entries[index].configure(state='readonly')
        self.hotkey_record_buttons[index].configure(text='錄製中', state='disabled')

        # 暫時移除所有已註冊的全域快捷鍵，避免衝突
        keyboard.unhook_all_hotkeys()

        # 使用 keyboard hook 監聽所有按鍵事件
        self._recording_hook = keyboard.hook(self._on_record_key_event)

    def _on_record_key_event(self, event):
        """處理錄製期間的鍵盤事件"""
        if self._recording_index is None:
            return

        MODIFIER_MAP = {
            'left shift': 'shift', 'right shift': 'shift',
            'left ctrl': 'ctrl', 'right ctrl': 'ctrl',
            'left alt': 'alt', 'right alt': 'alt',
            'left windows': 'win', 'right windows': 'win',
        }

        key_name = event.name.lower() if event.name else ''
        normalized = MODIFIER_MAP.get(key_name, key_name)

        if event.event_type == keyboard.KEY_DOWN:
            self._recorded_keys.add(normalized)
            self._update_recording_display()
        elif event.event_type == keyboard.KEY_UP:
            # 當有修飾鍵+普通鍵的組合，且普通鍵已被按下後放開任何鍵時完成錄製
            modifiers = {'shift', 'ctrl', 'alt', 'win'}
            has_modifier = bool(self._recorded_keys & modifiers)
            has_normal = bool(self._recorded_keys - modifiers)
            if has_modifier and has_normal:
                self.root.after(0, self.stop_hotkey_recording)
            elif not has_modifier and normalized in self._recorded_keys:
                # 單一按鍵也允許（例如 F1~F12）
                self.root.after(0, self.stop_hotkey_recording)

    def _update_recording_display(self):
        """即時更新錄製中顯示的快捷鍵文字"""
        modifiers_order = ['ctrl', 'alt', 'shift', 'win']
        modifiers = {'shift', 'ctrl', 'alt', 'win'}
        parts = []
        for mod in modifiers_order:
            if mod in self._recorded_keys:
                parts.append(mod)
        for key in sorted(self._recorded_keys - modifiers):
            parts.append(key)
        text = '+'.join(parts)
        if text != self._last_recorded_text:
            self._last_recorded_text = text
            self.root.after(0, lambda: self._set_recording_text(text))

    def _set_recording_text(self, text):
        """在主執行緒更新 Entry 文字"""
        if self._recording_index is not None:
            idx = self._recording_index
            self.hotkey_entries[idx].configure(state='normal')
            self.hotkey_vars[idx].set(text)
            self.hotkey_entries[idx].configure(state='readonly')

    def stop_hotkey_recording(self):
        """停止錄製並套用結果"""
        if self._recording_hook is not None:
            keyboard.unhook(self._recording_hook)
            self._recording_hook = None

        idx = self._recording_index
        if idx is None:
            return

        # 組合最終快捷鍵字串
        modifiers_order = ['ctrl', 'alt', 'shift', 'win']
        modifiers = {'shift', 'ctrl', 'alt', 'win'}
        parts = []
        for mod in modifiers_order:
            if mod in self._recorded_keys:
                parts.append(mod)
        for key in sorted(self._recorded_keys - modifiers):
            parts.append(key)
        result = '+'.join(parts)

        # 更新 Entry
        self.hotkey_entries[idx].configure(state='normal')
        if result:
            self.hotkey_vars[idx].set(result)
        else:
            self.hotkey_vars[idx].set(self.settings['hotkeys'][idx])
        self.hotkey_entries[idx].configure(state='readonly')

        # 還原按鈕狀態
        self.hotkey_record_buttons[idx].configure(text='錄製', state='normal')

        self._recording_index = None
        self._recorded_keys = set()

        # 重新註冊所有快捷鍵
        self.setup_hotkeys()

    def update_hotkey(self, index):
        new_hotkey = self.hotkey_vars[index].get()
        old_hotkey = self.settings['hotkeys'][index]
        
        if old_hotkey in keyboard._hotkeys:
            try:
                keyboard.remove_hotkey(old_hotkey)
            except Exception:
                pass
                
        self.settings['hotkeys'][index] = new_hotkey
        self.register_hotkey(index, new_hotkey)
        self.save_current_settings()

    def save_current_settings(self):
        for i in range(5):
            self.settings['timers'][i] = self.timers[i].get_settings()
        config.save_settings(self.settings)

    def start_tick_loop(self):
        for timer in self.timers:
            timer.tick()
        self.root.after(100, self.start_tick_loop)
