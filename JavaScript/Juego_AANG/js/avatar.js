function seleccionarPersonajeJugador(){
    let inputZuko = document.getElementById("zuko")
    let inputKatara = document.getElementById("katara")
    let inputAang = document.getElementById("aang")
    let inputToph = document.getElementById("toph")
    let spanpersonajejugador = document.getElementById("personaje-jugador")
    let spanPersonajeEnemigo = document.getElementById("personaje-enemigo")
    let personajes = ["Zuko", "Katara", "Aang", "Toph"] //lista de personajes
    let personajeJugador = "" //declaramos las variables de personaje jugador y enemigo
    let personajeEnemigo = ""

    numeroRandom = Math.floor(Math.random() * 4) + 1;
    console.log(numeroRandom)

    if (inputZuko.checked) {
        spanpersonajejugador.innerHTML = "Zuko"
        personajeJugador = "Zuko" //asignamos el personaje que eligió el jugador para comparar con el del enemigo
    } 
    
    else if (inputKatara.checked) {
        spanpersonajejugador.innerHTML = "Katara"
        personajeJugador = "Katara"
    } 
    
    else if (inputAang.checked) {
        spanpersonajejugador.innerHTML = "Aang"
        personajeJugador = "Aang"
    } 
    
    else if (inputToph.checked) {
        spanpersonajejugador.innerHTML = "Toph"
        personajeJugador = "Toph"
    } 
    
    else {
        alert("Debes seleccionar un personaje")
    }

    while (personajeEnemigo == "" || personajeEnemigo == personajeJugador) { //asignamos un numero random para elegir un nombre de la lista y lo comparamos con el que eligió el jugador
        let numeroRandom = Math.floor(Math.random() * 4)                    // si es igual vuelve a elegir otro numero aleatorio. todo esto hasta que los personajes sean diferentes
        personajeEnemigo = personajes[numeroRandom]
    }
    
    spanPersonajeEnemigo.innerHTML = personajeEnemigo //mostramos el nombre del personaje que eligió la máquina


}

let botonPersonajeJugador = document.getElementById("boton-personaje")
botonPersonajeJugador.addEventListener('click', seleccionarPersonajeJugador)