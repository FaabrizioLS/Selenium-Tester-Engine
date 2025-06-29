from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# ====================================
# Función principal para probar checkboxes
# ====================================
def run_input_checkbox_tests(driver): # Recibimos un driver Selenium ya inicializado
    results = [] # Lista para almacenar resultados
    checkboxes = driver.find_elements(By.CSS_SELECTOR, 'input[type="checkbox"]') # Obtenemos todos los checkbox

    # ==========================
    # Función para describir input
    # ==========================
    def describir_input(el, index):
        label = driver.execute_script("return arguments[0].nextSibling?.textContent", el)
        name = el.get_attribute("name")
        id_attr = el.get_attribute("id")
        if label and label.strip(): return f'Checkbox con texto "{label.strip()}"'
        elif name: return f'Checkbox con name="{name}"'
        elif id_attr: return f'Checkbox con id="{id_attr}"'
        else: return f'Checkbox[{index}] sin identificador'

    # ======================
    # Pruebas sobre un input
    # ======================
    def probar_checkbox(input_cb, identificador):

        def test(nombre, funcion):
            try:
                mensaje, estado = funcion()
                results.append(f"[{estado}] {identificador} - {nombre}: {mensaje}")
            except Exception as e:
                results.append(f"[❌] {identificador} - {nombre}: Error durante la prueba: {str(e)}")

        def estado_por_defecto():
            estado = input_cb.is_selected()
            return ("No está marcado por defecto.", "✔") if not estado else ("Marcado por defecto.", "⚠")

        def marcar_y_verificar():
            if not input_cb.is_selected(): input_cb.click()
            return ("Checkbox marcado correctamente.", "✔") if input_cb.is_selected() else ("No se pudo marcar.", "❌")

        def desmarcar_y_verificar():
            if input_cb.is_selected(): input_cb.click()
            return ("Checkbox desmarcado correctamente.", "✔") if not input_cb.is_selected() else ("No se pudo desmarcar.", "❌")

        def accesibilidad_tab():
            input_cb.send_keys(Keys.TAB)
            return ("Campo accesible por teclado (TAB).", "✔")

        def manipulacion_js():
            driver.execute_script("arguments[0].setAttribute('checked', 'true')", input_cb)
            estado = input_cb.is_selected()
            return ("Checkbox fue manipulado por JS.", "⚠") if estado else ("Protegido ante manipulación JS.", "✔")

        test("Estado por defecto", estado_por_defecto)
        test("Marcar checkbox", marcar_y_verificar)
        test("Desmarcar checkbox", desmarcar_y_verificar)
        test("Accesibilidad (TAB)", accesibilidad_tab)
        test("Manipulación por JavaScript", manipulacion_js)

    # ======================
    # Ejecutamos las pruebas
    # ======================
    for idx, input_el in enumerate(checkboxes):
        identificador = describir_input(input_el, idx + 1)
        probar_checkbox(input_el, identificador)

    return results
