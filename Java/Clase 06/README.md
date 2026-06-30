# 🐳 Clase 6 - Instalación de Docker en Windows

## 📖 Introducción

En esta clase se aprendió qué es Docker, cuáles son los requisitos para instalar Docker Desktop en Windows y cómo verificar que la instalación fue realizada correctamente.

---

# 🎯 Objetivos

- Comprender qué es Docker.
- Instalar Docker Desktop en Windows.
- Configurar WSL 2.
- Verificar el funcionamiento de Docker mediante comandos básicos.

---

# 🐳 ¿Qué es Docker?

Docker es una plataforma de virtualización basada en contenedores que permite desarrollar, ejecutar y distribuir aplicaciones de forma aislada, asegurando que funcionen de la misma manera en cualquier entorno.

A diferencia de una máquina virtual, los contenedores comparten el núcleo del sistema operativo, lo que los hace más livianos y rápidos.

---

# ✅ Requisitos previos

Antes de instalar Docker Desktop es necesario contar con:

- Windows 10 u 11 de 64 bits.
- Virtualización habilitada en BIOS.
- WSL 2 instalado.
- Conexión a Internet.

---

# 📥 Instalación de Docker Desktop

## Paso 1. Instalar WSL 2

Abrir PowerShell como administrador y ejecutar:

```powershell
wsl --install
```

Si WSL ya está instalado, verificarlo con:

```powershell
wsl --status
```

---

## Paso 2. Descargar Docker Desktop

Descargar Docker Desktop desde el sitio oficial:

https://www.docker.com/products/docker-desktop/

---

## Paso 3. Ejecutar el instalador

Durante la instalación dejar seleccionada la opción:

- Use WSL 2 instead of Hyper-V

Esperar a que finalice la instalación.

---

## Paso 4. Reiniciar Windows

Reiniciar el equipo para completar la configuración.

---

## Paso 5. Abrir Docker Desktop

Esperar hasta que Docker indique que está funcionando correctamente.

---

# ✔ Verificación de la instalación

Ejecutar:

```bash
docker --version
```

Luego:

```bash
docker run hello-world
```

Si aparece el mensaje **Hello from Docker!**, la instalación fue exitosa.

---

# 💻 Comandos utilizados

```bash
docker --version
```

Muestra la versión instalada.

```bash
docker run hello-world
```

Ejecuta un contenedor de prueba.

```bash
docker info
```

Muestra información sobre Docker.

---

# 📌 Conclusión

La instalación de Docker Desktop permite comenzar a trabajar con contenedores de forma sencilla. Una vez configurado, es posible crear, ejecutar y administrar aplicaciones aisladas del sistema operativo, facilitando el desarrollo y la portabilidad entre distintos entornos.