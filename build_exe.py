"""
NotifyTimer 打包腳本
執行此腳本即可將程式打包為單一 .exe（無小黑窗）。
用法：python build_exe.py
"""

import subprocess
import sys
import shutil
import os

APP_NAME = "NotifyTimer"
ENTRY = "main.py"
SPEC_FILE = f"{APP_NAME}.spec"
DIST_DIR = "dist"


def check_pyinstaller():
    """檢查 PyInstaller 是否已安裝，未安裝則自動安裝。"""
    try:
        import PyInstaller
        print(f"[OK] PyInstaller {PyInstaller.__version__} 已安裝")
    except ImportError:
        print("[INFO] 正在安裝 PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("[OK] PyInstaller 安裝完成")


def clean_build():
    """清除舊的 build / dist 資料夾。"""
    for folder in ["build", DIST_DIR]:
        if os.path.exists(folder):
            print(f"[CLEAN] 刪除 {folder}/")
            shutil.rmtree(folder)


def build():
    """使用 .spec 檔執行打包。"""
    print(f"\n{'='*50}")
    print(f"  開始打包 {APP_NAME}")
    print(f"{'='*50}\n")

    cmd = [sys.executable, "-m", "PyInstaller", SPEC_FILE, "--clean", "--noconfirm"]
    print(f"[CMD] {' '.join(cmd)}\n")
    result = subprocess.run(cmd)

    if result.returncode != 0:
        print("\n[ERROR] 打包失敗！請檢查上方錯誤訊息。")
        sys.exit(1)

    exe_path = os.path.join(DIST_DIR, f"{APP_NAME}.exe")
    if os.path.exists(exe_path):
        size_mb = os.path.getsize(exe_path) / (1024 * 1024)
        print(f"\n[OK] 打包成功！")
        print(f"     輸出：{os.path.abspath(exe_path)}")
        print(f"     大小：{size_mb:.1f} MB")
    else:
        print("\n[ERROR] 找不到輸出的 exe 檔案。")
        sys.exit(1)


if __name__ == "__main__":
    # 切到腳本所在目錄，確保路徑正確
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    check_pyinstaller()
    clean_build()
    build()

    print("\n完成！按 Enter 關閉...")
    input()
