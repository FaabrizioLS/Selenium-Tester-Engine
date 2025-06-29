from selenium.webdriver.common.by import By
import os

# ============================================
# Función principal para probar input tipo file
# ============================================
def run_input_file_tests(driver):  # Recibimos el driver Selenium ya inicializado
    results = []  # Lista para almacenar los resultados
    inputs = driver.find_elements(By.CSS_SELECTOR, 'input[type="file"]')  # Buscamos todos los inputs tipo file

    # ============================
    # Función para describir input
    # ============================
    def describir_input(el, index):  # Generamos una descripción con placeholder, name o id
        ph = el.get_attribute("placeholder")
        name = el.get_attribute("name")
        id_attr = el.get_attribute("id")
        if ph: return f'Input file con placeholder "{ph}"'
        elif name: return f'Input file con name="{name}"'
        elif id_attr: return f'Input file con id="{id_attr}"'
        else: return f'Input file[{index}] sin identificador'

    # ================================
    # Ejecutamos pruebas sobre el input
    # ================================
    def probar_input(input_file, identificador):

        def test(nombre, funcion):  # Ejecutamos cada prueba y capturamos errores
            try:
                mensaje, estado = funcion()
                results.append(f"[{estado}] {identificador} - {nombre}: {mensaje}")
            except Exception as e:
                results.append(f"[❌] {identificador} - {nombre}: Error durante la prueba: {str(e)}")

        def archivo_valido():
            ruta = os.path.abspath("archivo_prueba.txt")
            with open(ruta, "w") as f:
                f.write("Contenido de prueba.")
            input_file.send_keys(ruta)
            valor = input_file.get_attribute("value")
            return ("Archivo cargado correctamente." if valor else "Archivo no se cargó.", "✔" if valor else "✘")

        def archivo_malicioso():
            ruta = os.path.abspath("malicioso<script>.jpg")
            with open(ruta, "w") as f:
                f.write("Simulación de archivo con nombre XSS.")
            input_file.clear()
            input_file.send_keys(ruta)
            valor = input_file.get_attribute("value")
            return ("Nombre potencialmente peligroso aceptado." if valor else "Archivo malicioso rechazado.", "⚠")

        def archivo_grande():
            ruta = os.path.abspath("archivo_grande.txt")
            with open(ruta, "wb") as f:
                f.write(b"0" * 5 * 1024 * 1024)  # 5MB
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

    # ===========================
    # Aplicamos pruebas a inputs
    # ===========================
    for idx, input_el in enumerate(inputs):
        identificador = describir_input(input_el, idx + 1)
        probar_input(input_el, identificador)

    return results
