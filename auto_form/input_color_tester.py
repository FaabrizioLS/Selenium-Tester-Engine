from selenium.webdriver.common.by import By

# ==============================================
# Función principal para probar inputs de colores
# ==============================================
def run_input_color_tests(driver): # Recibimos un driver Selenium ya inicializado
    results = [] # Lista para almacenar los resultados
    inputs = driver.find_elements(By.CSS_SELECTOR, 'input[type="color"]') # Seleccionamos todos los campos tipo color

    # ================================
    # Función para describir un input
    # ================================
    def describir_input(el, index):
        ph = el.get_attribute("placeholder")
        name = el.get_attribute("name")
        id_attr = el.get_attribute("id")
        if ph: return f'Input color con placeholder "{ph}"'
        elif name: return f'Input color con name="{name}"'
        elif id_attr: return f'Input color con id="{id_attr}"'
        else: return f'Input color[{index}] sin identificador'

    # ================================
    # Ejecutamos pruebas sobre input
    # ================================
    def probar_input(input_color, identificador):

        def test(nombre, funcion):
            try:
                mensaje, estado = funcion()
                results.append(f"[{estado}] {identificador} - {nombre}: {mensaje}")
            except Exception as e:
                results.append(f"[❌] {identificador} - {nombre}: Error durante la prueba: {str(e)}")

        def color_por_defecto():
            valor = input_color.get_attribute("value")
            return (f"Valor inicial: '{valor}'", "✔" if valor.startswith("#") and len(valor) == 7 else "⚠")

        def color_valido():
            driver.execute_script("arguments[0].value = '#00FF00'; arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", input_color)
            valor = input_color.get_attribute("value")
            return ("Color aceptado correctamente." if valor.upper() == "#00FF00" else f"No aceptado: '{valor}'", "✔")

        def color_invalido():
            driver.execute_script("arguments[0].value = '123456'; arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", input_color)
            valor = input_color.get_attribute("value")
            return ("Formato inválido rechazado." if not valor.startswith("123456") else "Aceptó formato inválido.", "⚠")

        def vacio():
            driver.execute_script("arguments[0].value = ''; arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", input_color)
            valor = input_color.get_attribute("value")
            return ("Campo vacío permitido." if valor == "" else f"No se vació: '{valor}'", "⚠")

        def xss():
            driver.execute_script("arguments[0].value = '<script>alert(1)</script>'; arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", input_color)
            valor = input_color.get_attribute("value")
            return ("XSS sin sanitizar." if '<' in valor else "XSS bloqueado.", "❗" if '<' in valor else "✔")

        def sql():
            driver.execute_script("arguments[0].value = \"'#ff0000' OR '1'='1\"; arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", input_color)
            valor = input_color.get_attribute("value")
            return ("SQL Injection posible." if '1' in valor else "SQL bloqueado.", "❗" if '1' in valor else "✔")

        test("Valor por defecto", color_por_defecto)
        test("Color válido", color_valido)
        test("Color inválido", color_invalido)
        test("Campo vacío", vacio)
        test("Inyección XSS", xss)
        test("Inyección SQL", sql)

    # ============================
    # Ejecutamos pruebas por input
    # ============================
    for idx, input_el in enumerate(inputs):
        identificador = describir_input(input_el, idx + 1)
        probar_input(input_el, identificador)

    return results
