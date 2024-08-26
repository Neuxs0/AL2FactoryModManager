import webview
import os
import sys
import ctypes
import json
import inspect
import platform

def start_window(type, error=""):
    import functions
    if type == "normal":
        window = webview.create_window(title='AL2 Factory Mod Manager', url='win/index.html', resizable=False, width=800, height=600)
        for name, method in inspect.getmembers(functions.bind_func, predicate=inspect.isfunction):
            window.expose(method)
        webview.start()
    elif type == "error":
        ctypes.windll.user32.MessageBoxW(0, error, "AL2 Factory Mod Manager - Error", 0)
        sys.exit(1)

def check_program_files():
    programFiles = {
        ".\\win\\": False,
        ".\\settings.json": False
    }

    if not os.path.exists(".\\win\\") or not os.listdir(".\\win\\"):
        return programFiles, "Error: Missing essential files in 'win' directory! Please reinstall the application."

    for item in programFiles:
        if not os.path.exists(item):
            try:
                if item == ".\\settings.json":
                    with open(item, 'w') as f:
                        gameDir = ""
                        if platform.system() == "Windows":
                            gameDir = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Assembly Line 2"
                        elif platform.system() == "Darwin":
                            gameDir = "/Applications/Assembly Line 2"
                        else:
                            gameDir = "/home/user/.local/share/Steam/steamapps/common/Assembly Line 2/"
                        json.dump({"theme": "dark", "gameDir": f"{gameDir}"}, f, indent=4)
                elif "." in os.path.basename(item):
                    with open(item, 'w') as f:
                        pass
                else:
                    os.mkdir(item)
                programFiles[item] = True
            except Exception as e:
                return programFiles, f"Error creating '{item}': {str(e)}"
        else:
            programFiles[item] = True
    return programFiles, ""

if __name__ == '__main__':
    program_status, error_msg = check_program_files()

    if error_msg:
        print(error_msg, file=sys.stderr)
        start_window("error", error_msg)
    elif all(program_status.values()):
        start_window("normal")
    else:
        print("Error: Unknown error occurred during initialization.", file=sys.stderr)
        start_window("error", "Unknown error occurred during initialization.")