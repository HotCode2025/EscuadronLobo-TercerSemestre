function seleccionarPersonajeJugador(){
    let inputZuko = document.getElementById("zuko")
    let inputKatara = document.getElementById("katara")
    let inputAang = document.getElementById("aang")
    let inputToph = document.getElementById("toph")

    if (inputZuko.checked) {
        alert("El personaje que elegiste fue: Zuko 🔥")
    } 
    
    else if (inputKatara.checked) {
        alert("El personaje que elegiste fue: Katara 💧")
    } 
    
    else if (inputAang.checked) {
        alert("El personaje que elegiste fue: Aang 🌪️")
    } 
    
    else if (inputToph.checked) {
        alert("El personaje que elegiste fue: Toph 🌱")
    } 
    
    else {
        alert("Debes seleccionar un personaje")
    }
}

let botonPersonajeJugador = document.getElementById("boton-personaje");
botonPersonajeJugador.addEventListener('click', seleccionarPersonajeJugador);


