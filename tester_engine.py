
from selenium import webdriver                          
from selenium.webdriver.firefox.options import Options  
from selenium.webdriver.firefox.service import Service  
from auto_form.input_text_tester import run_input_text_tests
from auto_form.input_email_tester import run_input_email_tests
from datetime import datetime                           
import time                                             

# ======================
# Función principal
# ======================
def run_tests(url):  # Recibe la URL del HTML a probar
    results = []  # Lista para acumular los resultados
    options = Options()
    options.add_argument("--headless")  # Para que no se abra la ventana del navegador
    service = Service(executable_path="C:/WebDriver/geckodriver.exe")  # Ruta a geckodriver
    driver = webdriver.Firefox(service=service, options=options)  # Inicia el navegador

    try:
        driver.get(url)  # Abre la página
        time.sleep(1)  # Esperamos que el DOM cargue
        results.append("[✔] Página cargada correctamente")  # Confirmación visual

        results.extend(run_input_text_tests(driver))   # Ejecutamos pruebas de texto
        results.extend(run_input_email_tests(driver))  # Ejecutamos pruebas de email

    except Exception as e:
        results.append(f"[✘] Error general: {e}")  # Capturamos cualquier error grave

    finally:
        driver.quit()  # Cerramos el navegador
        return generate_report(results)  # Generamos y retornamos el reporte

# ======================
# Generador de reporte
# ======================
def generate_report(results):
    categories = {
        "✅ FUNCIONAL": [],
        "❌ FALLA DETECTADA": [],
        "⚠️ POSIBLE VULNERABILIDAD": []
    }

    for res in results:
        if res.startswith("[✔]"):
            categories["✅ FUNCIONAL"].append(res[4:])
        elif res.startswith("[✘]"):
            if any(p in res.lower() for p in ["<script", "sql", "1=1", "xss", "inyección", "or 1=1"]):
                categories["⚠️ POSIBLE VULNERABILIDAD"].append(res[4:])
            else:
                categories["❌ FALLA DETECTADA"].append(res[4:])
        elif res.startswith("[❗]"):
            categories["⚠️ POSIBLE VULNERABILIDAD"].append(res[4:])

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report = [f"🧪 INFORME AUTOMÁTICO DE PRUEBAS – {now}", "-" * 60]

    for titulo, items in categories.items():
        report.append(f"\n{titulo}:")
        if items:
            report.extend([f"  - {i}" for i in items])
        else:
            report.append("  (Ninguno)")

    report.append("\nResumen total:")
    report.append(f"  Funcional: {len(categories['✅ FUNCIONAL'])}")
    report.append(f"  Fallas: {len(categories['❌ FALLA DETECTADA'])}")
    report.append(f"  Vulnerabilidades: {len(categories['⚠️ POSIBLE VULNERABILIDAD'])}")
    return "\n".join(report)

# ======================
# Modo prueba directa
# ======================
if __name__ == "__main__":
    url_prueba = "file:///C:/Users/Windows/Desktop/formulario.html"  # Cambia por tu ruta local
    print(run_tests(url_prueba))
