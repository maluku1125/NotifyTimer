import pickle
import os
import json

APP_CONFIG_FILE = 'app_config.json'

def get_default_app_config():
    return {
        'save_path': os.getcwd(),
        'theme': 'dark',
        'refresh_mode': False
    }

def load_app_config():
    if os.path.exists(APP_CONFIG_FILE):
        try:
            with open(APP_CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return get_default_app_config()
    return get_default_app_config()

def save_app_config(config):
    try:
        with open(APP_CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"Failed to save app config: {e}")
        return False

def get_settings_file_path():
    app_config = load_app_config()
    save_path = app_config.get('save_path', os.getcwd())
    if not os.path.exists(save_path):
        try:
            os.makedirs(save_path)
        except OSError:
            save_path = os.getcwd() # fallback
    return os.path.join(save_path, 'timersettings.pkl')

def get_default_settings():
    return {
        'hotkeys': {i: f'ctrl+alt+{i+5}' for i in range(5)},
        'timers': [{'hours': '00', 'minutes': '00', 'seconds': '00', 'message': '輸入語音內容', 'notify_os': False, 'play_voice': True} for _ in range(5)]
    }

def migrate_old_settings(settings):
    for i in range(5):
         if 'hours' not in settings['timers'][i]:
              settings['timers'][i]['hours'] = '00'
         if 'notify_os' not in settings['timers'][i]:
              settings['timers'][i]['notify_os'] = False
         if 'play_voice' not in settings['timers'][i]:
              settings['timers'][i]['play_voice'] = True
    return settings

def load_settings():
    settings_file = get_settings_file_path()
    # 針對舊版資料夾根目錄遺留的檔案做相容載入
    old_file = 'timersettings.pkl'
    
    if os.path.exists(settings_file):
        try:
            with open(settings_file, 'rb') as f:
                settings = pickle.load(f)
                if 'hotkeys' not in settings or 'timers' not in settings:
                     return get_default_settings()
                return migrate_old_settings(settings)
        except Exception:
            pass
    elif os.path.exists(old_file) and settings_file != os.path.abspath(old_file):
        # 移轉
        try:
            with open(old_file, 'rb') as f:
                settings = pickle.load(f)
                if 'hotkeys' in settings and 'timers' in settings:
                    settings = migrate_old_settings(settings)
                    save_settings(settings)
                    return settings
        except Exception:
             pass

    return get_default_settings()

def save_settings(settings):
    settings_file = get_settings_file_path()
    try:
        with open(settings_file, 'wb') as f:
            pickle.dump(settings, f)
            return True
    except Exception as e:
        print(f"Failed to save settings: {e}")
        return False
