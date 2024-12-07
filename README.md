# FileGuardian

[![Version: 1.0](https://img.shields.io/badge/Version-1.0-blue.svg)](./README.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

## Resumen

**FileGuardian** es una herramienta profesional para la organización y gestión de archivos en tiempo real. Detecta duplicados, aplica reglas de organización configurables y permite monitorear carpetas automáticamente mediante una interfaz gráfica sencilla y eficiente.

---

## Características

- **Organización Inteligente**: Clasifica automáticamente los archivos en carpetas según reglas configurables.
- **Detección de Duplicados**: Encuentra y gestiona archivos duplicados basados en hashes.
- **Monitoreo en Tiempo Real**: Usa Watchdog para detectar y organizar archivos nuevos al instante.
- **Interfaz Amigable**: GUI intuitiva desarrollada con `tkinter`.

---

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/mier48/file-guardian
   cd file-guardian
   ```

2. Crea y activa un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/MacOS
   venv\Scripts\activate     # Windows
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

---

## Uso

1. Ejecuta la aplicación principal:
   ```bash
   python src/gui.py
   ```

2. Configura reglas de organización desde la interfaz.
3. Usa las herramientas adicionales para detección de duplicados y logs.

---

## Tests

Ejecuta las pruebas unitarias:
```bash
pytest tests/
```

---

## Licencia

Este proyecto está bajo la licencia [MIT](LICENSE).

---

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Por favor, abre un issue o envía un pull request.

---

## ✨ Créditos

Desarrollado por Alberto Mier. Si tienes dudas, contacta en [info@albertomier.com].
