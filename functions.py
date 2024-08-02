import requests
import zipfile
import json
import os
import io
import platform
import subprocess
import shutil

def load_json(file):
    with open(file, 'r') as f:
        return json.load(f)

def open_settings():
    return load_json(".\\settings.json")

def open_folder(path):
    if path is None:
        print(f"Error: Attempted to open a folder with a None path: {path}")
        return
    
    if not os.path.exists(path):
        print(f"Error: The specified path does not exist: {path}")
        return

    if platform.system() == "Windows":
        os.startfile(str(path))
    elif platform.system() == "Darwin":
        subprocess.run(["open", str(path)])
    else:
        subprocess.run(["xdg-open", str(path)])

def download_and_extract(url, extract_to):
    response = requests.get(url)
    if response.status_code == 200:
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
            zip_ref.extractall(extract_to)
        print(f"Extracted {url} to {extract_to}")
        return True
    else:
        print(f"Failed to download {url}")
        return False

def get_latest_bepinex_url():
    try:
        response = requests.get("https://api.github.com/repos/BepInEx/BepInEx/releases/latest")
        response.raise_for_status()
        release_info = response.json()
        assets = release_info.get('assets', [])
        
        user_os = platform.system().lower()
        if user_os == "windows":
            user_os = "win"
        elif user_os == "darwin":
            user_os = "macos"
        else:
            user_os = "linux"

        for asset in assets:
            if f"{user_os}_x64" in asset['name'] and asset['name'].endswith('.zip'):
                return asset['browser_download_url']
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch release info from https://api.github.com/repos/BepInEx/BepInEx/releases/latest: {e}")
    return None

class bind_func:
    settings = open_settings()
    game_directory = settings["gameDir"]

    @staticmethod
    def print(txt):
        print(txt)
    
    @staticmethod
    def open_folder(dir):
        open_folder(dir)
    
    @staticmethod
    def open_game_folder():
        if not bind_func.game_directory:
            return False, "Game directory is not set"
        if not os.path.exists(bind_func.game_directory):
            return False, f"Game directory does not exist: {bind_func.game_directory}"
        open_folder(bind_func.game_directory)
        return True, f"Opened game folder: {bind_func.game_directory}"
    
    @staticmethod
    def open_bepinex_folder():
        dir = f"{bind_func.game_directory}\\BepInEx"
        if not dir:
            return False, "BepInEx directory is not set"
        if not os.path.exists(dir):
            return False, f"BepInEx directory does not exist: {dir}"
        open_folder(dir)
        return True, f"Opened BepInEx folder: {dir}"
    
    @staticmethod
    def open_settings():
        return open_settings()
    
    @staticmethod
    def get_os():
        return platform.system()

    @staticmethod
    def set_game_directory(dir):
        bind_func.game_directory = dir
        return True
    
    @staticmethod
    def install_bepinex():
        success = True
        messages = []

        # Install BepInEx
        bepinex_url = get_latest_bepinex_url()
        if bepinex_url:
            if download_and_extract(bepinex_url, bind_func.game_directory):
                messages.append("BepInEx installed successfully")
            else:
                success = False
                messages.append("Failed to install BepInEx")
        else:
            success = False
            messages.append("Failed to get the latest BepInEx download URL")

    @staticmethod
    def uninstall_bepinex():
        shutil.rmtree(f"{bind_func.game_directory}\\BepInEx")

        files = [
            f"{bind_func.game_directory}\\.doorstop_version",
            f"{bind_func.game_directory}\\changelog.txt",
            f"{bind_func.game_directory}\\doorstop_config.ini",
            f"{bind_func.game_directory}\\winhttp.dll"
        ]

        for file in files:
            os.remove(file)