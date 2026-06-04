let ataqueJugador
let ataqueEnemigo

function iniciarJuego(){
    let botonPersonajeJugador = document.getElementById("boton-personaje")
    botonPersonajeJugador.addEventListener('click', seleccionarPersonajeJugador)
    
    let botonPunio = document.getElementById('boton-punio') //ahora creamos un escuchador de evento
    botonPunio.addEventListener('click', ataquePunio)
    let botonPatada = document.getElementById('boton-patada')
    botonPatada.addEventListener('click', ataquePatada)
    let botonBarrida = document.getElementById('boton-barrida')
    botonBarrida.addEventListener('click', ataqueBarrida)
}

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

function ataquePunio(){ //Modificamos la variable global ataqueJugador
    ataqueJugador = 'Punio'
    ataqueAleatorioEnemigo()
}

function ataquePatada(){ //Modificamos la variable global ataqueJugador
    ataqueJugador = 'Patada'
    ataqueAleatorioEnemigo()
}

function ataqueBarrida(){ //Modificamos la variable global ataqueJugador
    ataqueJugador = 'Barrida'
    ataqueAleatorioEnemigo()
}

function ataqueAleatorioEnemigo(){
    let ataqueAleatorio = Math.floor(Math.random() * 3) + 1
    if(ataqueAleatorio == 1){
        ataqueEnemigo = 'Punio'
    } else if(ataqueAleatorio == 2){
        ataqueEnemigo = 'Patada'
    } else {
        ataqueEnemigo = 'Barrida'
    }
    combate()
}

function combate(){
    //COMBATE
    if(ataqueEnemigo == ataqueJugador){ //EMPATE
        crearMensaje("EMPATE")
    } else if(ataqueEnemigo == 'Punio' && ataqueJugador == 'Barrida') { //GANASTE
        crearMensaje("GANASTE")
    } else if(ataqueEnemigo == 'Patada' && ataqueJugador == 'Punio') { //GANASTE
        crearMensaje("GANASTE")
    } else if(ataqueEnemigo == 'Barrida' && ataqueJugador == 'Patada') { //GANASTE
        crearMensaje("GANASTE")
    } else { //PERDISTE
        crearMensaje("PERDISTE")
    }
}

function crearMensaje(resultado){
    let sectionMensaje = document.getElementById('mensajes') //creamos la variable de la seccion a modificar
    let parrafo = document.createElement('p') //creamos la variable que va a contener el mensaje

    parrafo.innerHTML = 'Tu personaje atacó con ' + ataqueJugador + ', el personaje del enemigo atacó con ' + ataqueEnemigo + ' ' + resultado
    sectionMensaje.appendChild(parrafo) //mostramos los ataques en el DOM
}

window.addEventListener('load', iniciarJuego)