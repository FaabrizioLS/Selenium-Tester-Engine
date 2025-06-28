from selenium.webdriver.common.by import By

# ============================================
# Función principal para probar campos de fecha y hora
# ============================================
def run_input_datetime_tests(driver): # Recibimos un driver Selenium ya inicializado
    results = [] # Lista para almacenar los resultados
    date_inputs = driver.find_elements(By.CSS_SELECTOR, 'input[type="date"]') # Capturamos inputs tipo date
    time_inputs = driver.find_elements(By.CSS_SELECTOR, 'input[type="time"]') # Capturamos inputs tipo time
    month_inputs = driver.find_elements(By.CSS_SELECTOR, 'input[type="month"]') # Capturamos inputs tipo month
    week_inputs = driver.find_elements(By.CSS_SELECTOR, 'input[type="week"]') # Capturamos inputs tipo week
    datetime_inputs = driver.find_elements(By.CSS_SELECTOR, 'input[type="datetime-local"]') # Capturamos inputs tipo datetime-local

    # ==========================
    # Función para describir input
    # ==========================
    def describir_input(el, index, tipo):
        ph = el.get_attribute("placeholder")
        name = el.get_attribute("name")
        id_attr = el.get_attribute("id")
        if ph: return f'Input {tipo} con placeholder "{ph}"'
        elif name: return f'Input {tipo} con name="{name}"'
        elif id_attr: return f'Input {tipo} con id="{id_attr}"'
        else: return f'Input {tipo}[{index}] sin identificador'

    def probar_input(input_el, identificador, tipo, valor_correcto):
        def test(nombre, funcion):
            try:
                mensaje, estado = funcion()
                results.append(f"[{estado}] {identificador} - {nombre}: {mensaje}")
            except Exception as e:
                results.append(f"[❌] {identificador} - {nombre}: Error durante la prueba: {str(e)}")

        def valor_valido():
            input_el.clear()
            input_el.send_keys(valor_correcto)
            valor = input_el.get_attribute("value")
            return ("Valor aceptado correctamente." if valor == valor_correcto else f"No aceptado: '{valor}'", "✔")

        def formato_invalido():
            input_el.clear()
            input_el.send_keys("invalido")
            valor = input_el.get_attribute("value")
            return ("Formato no aceptado." if valor == "" else f"Aceptó formato inválido: '{valor}'", "⚠")

        def vacio():
            input_el.clear()
            valor = input_el.get_attribute("value")
            return ("Campo vacío permitido." if valor == "" else f"No se vació: '{valor}'", "⚠")

        def especiales():
            input_el.clear()
            input_el.send_keys("@#!")
            valor = input_el.get_attribute("value")
            return ("Caracteres especiales rechazados." if valor == "" else f"Valor actual: '{valor}'", "⚠")

        def xss():
            input_el.clear()
            input_el.send_keys("<script>alert(1)</script>")
            valor = input_el.get_attribute("value")
            return ("XSS sin sanitizar." if '<' in valor else "XSS bloqueado.", "❗" if '<' in valor else "✔")

        def sql():
            input_el.clear()
            input_el.send_keys("' OR '1'='1")
            valor = input_el.get_attribute("value")
            return ("SQL Injection posible." if '1' in valor else "SQL bloqueado.", "❗" if '1' in valor else "✔")

        test("Valor válido", valor_valido)
        test("Formato incorrecto", formato_invalido)
        test("Campo vacío", vacio)
        test("Caracteres especiales", especiales)
        test("Inyección XSS", xss)
        test("Inyección SQL", sql)

    # ============================
    # Ejecutamos pruebas para cada tipo
    # ============================
    for idx, el in enumerate(date_inputs):
        probar_input(el, describir_input(el, idx + 1, "date"), "date", "2025-06-28")

    for idx, el in enumerate(time_inputs):
        probar_input(el, describir_input(el, idx + 1, "time"), "time", "13:30")

    for idx, el in enumerate(month_inputs):
        probar_input(el, describir_input(el, idx + 1, "month"), "month", "2025-06")

    for idx, el in enumerate(week_inputs):
        probar_input(el, describir_input(el, idx + 1, "week"), "week", "2025-W26")

    for idx, el in enumerate(datetime_inputs):
        probar_input(el, describir_input(el, idx + 1, "datetime-local"), "datetime-local", "2025-06-28T13:30")

    return results
