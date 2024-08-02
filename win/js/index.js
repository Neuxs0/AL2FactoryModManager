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

function install_modloader() {
    pywebview.api.install_modloader().then((result) => {
        print(result[1]);
        if (!result[0]) {
            print("Failed to install one or more modloaders");
        }
    }).catch((error) => {
        print("Error during modloader installation:", error);
    });
}

function uninstall_modloader() {
    pywebview.api.uninstall_modloader().then(() => {}).catch((error) => {})
}

get_settings()