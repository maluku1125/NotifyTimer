# NotifyTimer ⏰

倒計時提醒工具，支援多組計時器、語音播報、Windows 系統通知與全域快捷鍵。

## 功能

- **5 組獨立計時器** — 可同時運行，各自設定時/分/秒
- **語音播報** — 計時結束後透過 Google TTS 語音唸出自訂提醒內容
- **Windows 通知** — 計時結束後發送系統推播通知
- **全域快捷鍵** — 自訂鍵盤快捷鍵快速啟動各計時器
- **深色/淺色主題** — 可在系統設定中切換
- **迷你模式** — 一鍵收合為精簡視窗
- **設定持久化** — 計時器與快捷鍵設定自動儲存

## 安裝

```bash
pip install -r requirements.txt
```

### 相依套件

| 套件 | 用途 |
|------|------|
| `sv-ttk` | Sun Valley ttk 主題 |
| `keyboard` | 全域快捷鍵監聽 |
| `Pillow` | 圖標載入 |
| `pygame` | 音效播放 |
| `gTTS` | Google 文字轉語音 |
| `winotify` | Windows 推播通知 |

## 使用方式

```bash
python main.py
```

## 打包為 EXE

```bash
python build_exe.py
```

打包完成後，執行檔位於 `dist/NotifyTimer.exe`。

## 專案結構

```
NotifyTimer/
├── main.py            # 程式入口
├── build_exe.py       # PyInstaller 打包腳本
├── assets/            # 靜態素材
│   ├── bug.ico        # 應用程式圖標
│   └── ding.wav       # 提示音效
└── core/              # 功能模組
    ├── __init__.py
    ├── ui.py           # UI 介面 (TimerApp, TimerRow)
    ├── audio.py        # 音效與語音播報
    ├── config.py       # 設定檔管理
    ├── notifier.py     # Windows 系統通知
    └── timer_core.py   # 計時邏輯核心
```

## 作者

諭諭
