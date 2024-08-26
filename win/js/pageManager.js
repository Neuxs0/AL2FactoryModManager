function navigate(page) {
    var pages = [
        "home", "mods", "game-controls", "settings"
    ]

    if (page != null && pages.includes(page)) {
        document.getElementById(page).style.display = "block"
    }

    pages.forEach(element => {
        if (element != page) {
            document.getElementById(element).style.display = "none"
        }
    });
}

navigate("home")