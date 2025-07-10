# Selenium-Tester-Engine
Herramienta en Python que automatiza pruebas funcionales y de seguridad sobre formularios HTML5 utilizando Selenium WebDriver.

Antes de ejecutar el proyecto, asegúrate de tener instalado lo siguiente:

---

## ✅ Requisitos

### 1. Python 3.8 o superior
- Descargar desde: https://www.python.org/downloads/

### 2. Uno o más navegadores compatibles:
- [Firefox](https://www.mozilla.org/firefox/new/)
- [Google Chrome](https://www.google.com/chrome/)
- [Microsoft Edge](https://www.microsoft.com/edge)
- [Brave Browser](https://brave.com/download/)
- [Vivaldi](https://vivaldi.com/download/)

### 3. WebDriver correspondiente en `C:/WebDriver/`:
| Navegador  | Driver            | Enlace de descarga                                         |
|------------|-------------------|-------------------------------------------------------------|
| Firefox    | `geckodriver.exe` | https://github.com/mozilla/geckodriver/releases            |
| Chrome     | `chromedriver.exe`| https://sites.google.com/chromium.org/driver/              |
| Edge       | `msedgedriver.exe`| https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/ |
| Brave      | `chromedriver.exe`| Usa el mismo que Chrome.                                  |
| Vivaldi    | `chromedriver.exe`| Usa el mismo que Chrome.                                  |

> Crea la carpeta `C:/WebDriver/` si no existe, y coloca los `.exe` allí.

### 4. Instalar Selenium

```bash
pip install selenium
