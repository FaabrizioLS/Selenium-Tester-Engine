from selenium.webdriver.common.by import By

# ============================================
# Función principal para probar campos de rango
# ============================================
def run_input_range_tests(driver): # Recibimos un driver Selenium ya inicializado
    results = [] # Lista para almacenar los resultados
    range_inputs = driver.find_elements(By.CSS_SELECTOR, 'input[type="range"]') # Capturamos inputs tipo range

    # ==============================
    # Función para describir input
    # ==============================
    def describir_input(el, index):
        ph = el.get_attribute("placeholder")
        name = el.get_attribute("name")
        id_attr = el.get_attribute("id")
        if ph: return f'Input range con placeholder "{ph}"'
        elif name: return f'Input range con name="{name}"'
        elif id_attr: return f'Input range con id="{id_attr}"'
        else: return f'Input range[{index}] sin identificador'

    # ================================
    # Pruebas individuales por input
    # ================================
    def probar_range_input(input_range, identificador):

        def test(nombre, funcion):
            try:
                mensaje, estado = funcion()
                results.append(f"[{estado}] {identificador} - {nombre}: {mensaje}")
            except Exception as e:
                results.append(f"[❌] {identificador} - {nombre}: Error durante la prueba: {str(e)}")

        def valor_defecto():
            valor = input_range.get_attribute("value")
            min_val = int(input_range.get_attribute("min") or 0)
            max_val = int(input_range.get_attribute("max") or 100)
            if valor and min_val <= int(valor) <= max_val:
                return f"Valor por defecto dentro del rango: {valor}", "✔"
            return f"Valor fuera del rango permitido: {valor}", "⚠"

        def cambiar_valor():
            driver.execute_script("arguments[0].value = 50", input_range)
            valor = input_range.get_attribute("value")
            return ("Valor asignado correctamente a 50." if valor == "50"
                    else f"No se pudo cambiar a 50, valor actual: {valor}",
                    "✔" if valor == "50" else "⚠")

        def limites():
            driver.execute_script("arguments[0].value = arguments[1]", input_range, 0)
            v1 = input_range.get_attribute("value")
            driver.execute_script("arguments[0].value = arguments[1]", input_range, 100)
            v2 = input_range.get_attribute("value")
            return (f"Límites aceptados (0 y 100): [{v1}, {v2}]", "✔")

        def fuera_de_rango():
            driver.execute_script("arguments[0].value = arguments[1]", input_range, 150)
            valor = input_range.get_attribute("value")
            return ("Aceptó valor fuera de rango: 150", "❗") if int(valor) > 100 else ("Valor restringido correctamente.", "✔")

        def letras():
            driver.execute_script("arguments[0].value = 'abc'", input_range)
            valor = input_range.get_attribute("value")
            return ("Se aceptaron letras en el campo." if not valor.isdigit() else "Campo ignoró letras.", "❗" if not valor.isdigit() else "✔")

        def especiales():
            driver.execute_script("arguments[0].value = '!@#'", input_range)
            valor = input_range.get_attribute("value")
            return ("Se aceptaron caracteres especiales." if not valor.isdigit() else "Campo ignoró caracteres especiales.", "❗" if not valor.isdigit() else "✔")

        def vacio():
            driver.execute_script("arguments[0].value = ''", input_range)
            valor = input_range.get_attribute("value")
            return ("Campo vacío permitido." if valor == "" else f"No se vació: '{valor}'", "⚠")

        def xss():
            driver.execute_script("arguments[0].value = '<script>'", input_range)
            valor = input_range.get_attribute("value")
            return ("XSS sin sanitizar." if "<" in valor else "XSS bloqueado.", "❗" if "<" in valor else "✔")

        def sql():
            driver.execute_script("arguments[0].value = \"' OR '1'='1\"", input_range)
            valor = input_range.get_attribute("value")
            return ("SQL Injection posible." if "1" in valor else "SQL bloqueado.", "❗" if "1" in valor else "✔")

        test("Valor por defecto", valor_defecto)
        test("Cambio de valor válido", cambiar_valor)
        test("Límites inferior y superior", limites)
        test("Valor fuera de rango", fuera_de_rango)
        test("Texto en campo", letras)
        test("Caracteres especiales", especiales)
        test("Campo vacío", vacio)
        test("Inyección XSS", xss)
        test("Inyección SQL", sql)

    # =========================
    # Ejecutamos todas las pruebas
    # =========================
    for idx, input_el in enumerate(range_inputs):
        identificador = describir_input(input_el, idx + 1)
        probar_range_input(input_el, identificador)

    return results
