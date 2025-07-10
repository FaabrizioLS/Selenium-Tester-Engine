from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotInteractableException

# =============================================
# Función principal para probar botones (toggle)
# =============================================
def run_button_tests(driver):  # Recibimos un driver Selenium ya inicializado
    results = []  # Lista de resultados
    buttons = driver.find_elements(By.CSS_SELECTOR, 'button, [role="button"], input[type="button"], input[type="submit"], input[type="reset"]')  # Obtenemos todos los botones

    # ===========================
    # Función para describir el botón
    # ===========================
    def describir_boton(el, index):
        texto = el.text.strip()
        id_attr = el.get_attribute("id")
        name = el.get_attribute("name")
        aria_label = el.get_attribute("aria-label")
        value = el.get_attribute("value")

        if texto:
            return f'Botón con texto "{texto}"'
        elif id_attr:
            return f'Botón con id="{id_attr}"'
        elif name:
            return f'Botón con name="{name}"'
        elif aria_label:
            return f'Botón con aria-label="{aria_label}"'
        elif value:
            return f'Botón con value="{value}"'
        else:
            return f'Botón[{index}] sin identificador'

    # =======================
    # Funciones de prueba
    # =======================
    def probar_boton(boton, identificador):

        def test(nombre, funcion):
            try:
                mensaje, estado = funcion()
                results.append(f"[{estado}] {identificador} - {nombre}: {mensaje}")
            except ElementNotInteractableException:
                results.append(f"[⚠] {identificador} - {nombre}: No interactuable.")
            except Exception as e:
                results.append(f"[❌] {identificador} - {nombre}: Error: {str(e)}")

        def click_funciona():
            estado_inicial = driver.execute_script("return document.body.className")
            boton.click()
            estado_despues = driver.execute_script("return document.body.className")
            if estado_inicial != estado_despues:
                return "Click cambió el estado de la página.", "✔"
            else:
                return "Click no produjo cambios visibles en la clase del body.", "⚠"

        def doble_click():
            boton.click()
            boton.click()
            estado_final = driver.execute_script("return document.body.className")
            return f"Estado tras doble clic: '{estado_final}'", "✔"

        def foco_teclado():
            boton.send_keys(Keys.ENTER)
            return "Botón responde a Enter (teclado).", "✔"

        def visible():
            visible = boton.is_displayed()
            return ("Botón visible correctamente." if visible else "Botón no es visible."), "✔" if visible else "⚠"

        test("Click funcional", click_funciona)
        test("Doble click funcional", doble_click)
        test("Teclado (Enter)", foco_teclado)
        test("Visibilidad", visible)

    # ================================
    # Ejecutamos pruebas en cada botón
    # ================================
    for idx, boton in enumerate(buttons):
        identificador = describir_boton(boton, idx + 1)
        probar_boton(boton, identificador)

    return results
