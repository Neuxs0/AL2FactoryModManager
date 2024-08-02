var settings = ""

function print(txt) {
    pywebview.api.print(txt).then(() => {}).catch((error) => {})
}

function get_settings() {
    pywebview.api.open_settings().then((settingsFile) => {
        settings = settingsFile
    }).catch((error) => {})
}

function open_folder(dir) {
    pywebview.api.open_folder(dir).then(() => {}).catch((error) => {})
}

function open_game_folder() {
    pywebview.api.open_game_folder().then(() => {}).catch((error) => {})
}

function open_bepinex_folder() {
    pywebview.api.open_bepinex_folder().then(() => {}).catch((error) => {})
}

function install_bepinex() {
    pywebview.api.install_bepinex().then((result) => {
        print(result[1]);
        if (!result[0]) {
            print("Failed to install bepinex");
        }
    }).catch((error) => {
        print("Error during bepinex installation:", error);
    });
}

function uninstall_bepinex() {
    pywebview.api.uninstall_bepinex().then(() => {}).catch((error) => {})
}

get_settings()