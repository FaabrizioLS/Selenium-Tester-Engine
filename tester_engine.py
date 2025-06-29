from selenium import webdriver                           
from selenium.webdriver.firefox.options import Options   
from selenium.webdriver.firefox.service import Service   
from datetime import datetime                            
import time                                              

# =============================
# Módulos de pruebas automáticas
# =============================
from auto_form.input_text_tester import run_input_text_tests
from auto_form.input_email_tester import run_input_email_tests
from auto_form.input_password_tester import run_input_password_tests
from auto_form.input_number_tester import run_input_number_tests
from auto_form.input_tel_tester import run_input_tel_tests
from auto_form.input_url_tester import run_input_url_tests
from auto_form.input_search_tester import run_input_search_tests
from auto_form.input_range_tester import run_input_range_tests
from auto_form.input_checkbox_tester import run_input_checkbox_tests
from auto_form.input_radio_tester import run_input_radio_tests
from auto_form.input_file_tester import run_input_file_tests
from auto_form.input_select_tester import run_input_select_tests
from auto_form.input_textarea_tester import run_input_textarea_tests
from auto_form.input_color_tester import run_input_color_tests
from auto_form.input_datetime_tester import run_input_datetime_tests
from auto_form.input_button_tester import run_button_tests
# ======================
# Función principal
# ======================
def run_tests(url):  # Recibe la URL del HTML a probar
    results = []  # Lista para acumular los resultados
    options = Options()
    options.add_argument("--headless")  # Ejecutamos sin abrir ventana
    service = Service(executable_path="C:/WebDriver/geckodriver.exe")  # Ruta al ejecutable de GeckoDriver
    driver = webdriver.Firefox(service=service, options=options)  # Creamos el navegador

    try:
        driver.get(url)  # Abrimos la página
        time.sleep(1)  # Esperamos que cargue correctamente
        results.append("[✔] Página cargada correctamente")  # Confirmación de carga

        # ================================
        # Ejecutamos todas las pruebas
        # ================================
        results.extend(run_input_text_tests(driver))
        results.extend(run_input_email_tests(driver))
        results.extend(run_input_password_tests(driver))
        results.extend(run_input_number_tests(driver))
        results.extend(run_input_tel_tests(driver))
        results.extend(run_input_url_tests(driver))
        results.extend(run_input_search_tests(driver))
        results.extend(run_input_range_tests(driver))
        results.extend(run_input_checkbox_tests(driver))
        results.extend(run_input_radio_tests(driver))
        results.extend(run_input_file_tests(driver))
        results.extend(run_input_select_tests(driver))
        results.extend(run_input_textarea_tests(driver))
        results.extend(run_input_color_tests(driver))
        results.extend(run_input_datetime_tests(driver))
        results.extend(run_button_tests(driver))


    except Exception as e:
        results.append(f"[✘] Error general: {e}")  # Capturamos cualquier fallo grave

    finally:
        driver.quit()  # Cerramos navegador al final
        return generate_report(results)  # Procesamos resultados

# ==========================
# Generador de reporte final
# ==========================
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

# =======================
# Prueba directa opcional
# =======================
if __name__ == "__main__":
    url_prueba = "file:///C:/Users/Windows/Desktop/formulario.html"  # Ruta local para test
    print(run_tests(url_prueba))
