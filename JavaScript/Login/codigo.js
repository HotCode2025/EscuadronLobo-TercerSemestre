// =============================================
//  LOGIN FORM - Funcionalidad JavaScript
//  Web Viva - Final 3
// =============================================

// Usuarios registrados (simulando una base de datos)
const USUARIOS = {
  'admin': 'admin123',
  'cecy': 'mendoza2024',
  'usuario': 'pass123'
};

// ---- Referencias al DOM ----
const loginBtn    = document.getElementById('loginBtn');
const usernameInput = document.getElementById('username');
const passwordInput = document.getElementById('password');
const mensajeDiv  = document.getElementById('mensaje');
const strengthBar = document.getElementById('strengthBar');
const forgotLink  = document.getElementById('forgotLink');
const signupLink  = document.getElementById('signupLink');

// ---- Función: mostrar mensaje ----
function mostrarMensaje(texto, tipo) {
  mensajeDiv.textContent = texto;
  mensajeDiv.className = 'mensaje ' + tipo;
}

// ---- Función: calcular fortaleza de contraseña ----
function calcularFortaleza(pw) {
  if (!pw) return 0;
  let nivel = 0;
  if (pw.length >= 6)             nivel++;  // longitud mínima
  if (/[A-Z]/.test(pw))           nivel++;  // tiene mayúscula
  if (/[0-9]/.test(pw))           nivel++;  // tiene número
  if (/[^a-zA-Z0-9]/.test(pw))    nivel++;  // tiene símbolo
  return nivel;
}

// ---- Evento: barra de fortaleza en tiempo real ----
passwordInput.addEventListener('input', function () {
  const nivel = calcularFortaleza(this.value);
  const anchos  = ['0%', '25%', '50%', '75%', '100%'];
  const colores = ['transparent', '#ff6b6b', '#ffd23f', '#a3e635', '#2cb67d'];
  strengthBar.style.width      = anchos[nivel];
  strengthBar.style.background = colores[nivel];
});

// ---- Evento: login al presionar Enter desde password ----
passwordInput.addEventListener('keydown', function (e) {
  if (e.key === 'Enter') loginBtn.click();
});

// ---- Evento: click en botón Login ----
loginBtn.addEventListener('click', function (e) {
  e.preventDefault();

  const user = usernameInput.value.trim();
  const pass = passwordInput.value;

  // Resetear mensaje
  mensajeDiv.className = 'mensaje';
  mensajeDiv.style.display = 'none';

  // Validar campos vacíos
  if (!user || !pass) {
    mostrarMensaje('Por favor completá usuario y contraseña.', 'error');
    return;
  }

  // Validar credenciales
  if (USUARIOS[user] && USUARIOS[user] === pass) {
    mostrarMensaje('¡Bienvenido, ' + user + '! Acceso concedido.', 'success');
  } else {
    mostrarMensaje('Usuario o contraseña incorrectos.', 'error');
    passwordInput.value = '';
    strengthBar.style.width = '0';
  }
});

// ---- Evento: olvidé mi contraseña ----
forgotLink.addEventListener('click', function (e) {
  e.preventDefault();
  mostrarMensaje('Funcionalidad de recupero próximamente.', 'error');
});

// ---- Evento: registrarse ----
signupLink.addEventListener('click', function (e) {
  e.preventDefault();
  mostrarMensaje('Registro próximamente disponible.', 'error');
});
