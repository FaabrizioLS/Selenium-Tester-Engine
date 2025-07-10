from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import tempfile

def run_input_file_tests(driver, timeout=10):
    results = []
    wait = WebDriverWait(driver, timeout)

    # Buscamos inputs tipo file (soporta WebViews si están cargados)
    try:
        inputs = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'input[type="file"]')))
    except:
        results.append("[⚠] No se encontraron inputs tipo file.")
        return results

    def describir_input(el, index):
        ph = el.get_attribute("placeholder")
        name = el.get_attribute("name")
        id_attr = el.get_attribute("id")
        if ph: return f'Input file con placeholder "{ph}"'
        elif name: return f'Input file con name="{name}"'
        elif id_attr: return f'Input file con id="{id_attr}"'
        else: return f'Input file[{index}] sin identificador'

    def probar_input(input_file, identificador):

        def test(nombre, funcion):
            try:
                mensaje, estado = funcion()
                results.append(f"[{estado}] {identificador} - {nombre}: {mensaje}")
            except Exception as e:
                results.append(f"[❌] {identificador} - {nombre}: Error durante la prueba: {str(e)}")

        def archivo_valido():
            with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w") as f:
                f.write("Contenido de prueba.")
                ruta = f.name
            input_file.clear()
            input_file.send_keys(ruta)
            valor = input_file.get_attribute("value")
            return ("Archivo cargado correctamente." if valor else "Archivo no se cargó.", "✔" if valor else "❌")

        def archivo_malicioso():
            ruta = os.path.abspath("malicioso<script>.jpg")
            with open(ruta, "w", encoding="utf-8") as f:
                f.write("Simulación de archivo con nombre XSS.")
            input_file.clear()
            input_file.send_keys(ruta)
            valor = input_file.get_attribute("value")
            return ("Nombre potencialmente peligroso aceptado." if valor else "Archivo malicioso rechazado.", "⚠")

        def archivo_grande():
            with tempfile.NamedTemporaryFile(delete=False, suffix=".bin") as f:
                f.write(b"A" * 10 * 1024 * 1024)  # 10MB
                ruta = f.name
            input_file.clear()
            input_file.send_keys(ruta)
            valor = input_file.get_attribute("value")
            return ("Archivo grande cargado." if valor else "No se cargó archivo grande.", "✔" if valor else "⚠")

        def vacio():
            input_file.clear()
            valor = input_file.get_attribute("value")
            return ("Campo vacío permitido." if valor == "" else f"No se vació: '{valor}'", "⚠")

        test("Archivo válido", archivo_valido)
        test("Nombre malicioso", archivo_malicioso)
        test("Archivo grande", archivo_grande)
        test("Campo vacío", vacio)

    # Ejecutar pruebas por cada input encontrado
    for idx, input_el in enumerate(inputs):
        identificador = describir_input(input_el, idx + 1)
        probar_input(input_el, identificador)

    return results
