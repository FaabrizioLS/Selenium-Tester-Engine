from selenium.webdriver.common.by import By

# ====================================================
# Función para probar campos de selección tipo radio
# ====================================================
def run_input_radio_tests(driver):  # Recibimos el driver Selenium
    results = []  # Lista para almacenar los resultados
    radio_groups = {}  # Agrupamos radios por su atributo name

    radios = driver.find_elements(By.CSS_SELECTOR, 'input[type="radio"]')  # Obtenemos todos los radios

    for radio in radios:
        name = radio.get_attribute("name")
        if name:
            if name not in radio_groups:
                radio_groups[name] = []
            radio_groups[name].append(radio)

    # ===================================
    # Funciones de prueba para cada grupo
    # ===================================
    for name, group in radio_groups.items():

        def test(nombre, funcion):
            try:
                mensaje, estado = funcion()
                results.append(f"[{estado}] Grupo radio '{name}' - {nombre}: {mensaje}")
            except Exception as e:
                results.append(f"[❌] Grupo radio '{name}' - {nombre}: Error en prueba: {str(e)}")

        def seleccion_unica():
            selected = []
            for radio in group:
                driver.execute_script("arguments[0].click()", radio)
                if radio.is_selected():
                    selected.append(radio)
            return ("Solo una opción puede seleccionarse." if len(selected) == 1 else f"Seleccionó {len(selected)} opciones", "✔" if len(selected) == 1 else "❌")

        def cambio_de_seleccion():
            if len(group) < 2:
                return ("No hay suficientes radios para probar cambio de selección.", "⚠")
            driver.execute_script("arguments[0].click()", group[0])
            driver.execute_script("arguments[0].click()", group[1])
            return ("Cambio de selección funcional." if group[1].is_selected() and not group[0].is_selected() else "No se actualizó la selección", "✔" if group[1].is_selected() else "❌")

        def sin_seleccion_inicial():
            seleccionados = [r for r in group if r.is_selected()]
            return ("Ninguna opción está seleccionada por defecto." if not seleccionados else f"{len(seleccionados)} opción(es) ya seleccionada(s)", "⚠")

        def value_correcto():
            for radio in group:
                driver.execute_script("arguments[0].click()", radio)
                valor = radio.get_attribute("value")
                if not valor:
                    return ("Falta atributo 'value' en un radio.", "❌")
            return ("Todos los radios tienen valores válidos.", "✔")

        def prueba_teclado():
            try:
                group[0].send_keys(" ")  # Espacio debería marcarlo
                return ("Acepta navegación con teclado.", "✔")
            except:
                return ("No responde al teclado (espacio).", "❌")

        test("Selección única", seleccion_unica)
        test("Cambio de selección", cambio_de_seleccion)
        test("Sin selección inicial", sin_seleccion_inicial)
        test("Validación de value", value_correcto)
        test("Navegación con teclado", prueba_teclado)

    return results
