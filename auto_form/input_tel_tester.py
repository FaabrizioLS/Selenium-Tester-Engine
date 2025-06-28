from selenium.webdriver.common.by import By

# ========================================
# Función principal para probar teléfonos
# ========================================
def run_input_tel_tests(driver):  # Recibe un driver Selenium ya inicializado
    results = []  # Lista para almacenar los resultados
    inputs = driver.find_elements(By.CSS_SELECTOR, 'input[type="tel"]')  # Seleccionamos todos los campos tipo teléfono

    # ========================
    # Identificación del campo
    # ========================
    def describir_input(el, index):  # Generamos una descripción legible del input
        ph = el.get_attribute("placeholder")
        name = el.get_attribute("name")
        id_attr = el.get_attribute("id")
        if ph: return f'Input con placeholder "{ph}"'
        elif name: return f'Input con name="{name}"'
        elif id_attr: return f'Input con id="{id_attr}"'
        else: return f'Input[{index}] sin identificador'

    # ======================
    # Pruebas por cada campo
    # ======================
    def probar_input(input_tel, identificador):

        def test(nombre, funcion):  # Ejecutamos una prueba y almacenamos el resultado
            try:
                mensaje, estado = funcion()
                results.append(f"[{estado}] {identificador} - {nombre}: {mensaje}")
            except Exception as e:
                results.append(f"[❌] {identificador} - {nombre}: Error durante la prueba: {str(e)}")

        # =====================================
        # Pruebas específicas para tipo teléfono
        # =====================================

        def numero_valido():
            input_tel.clear()
            input_tel.send_keys("+51 999 999 999")
            valor = input_tel.get_attribute("value")
            return ("Número aceptado correctamente." if "+51" in valor else f"No se aceptó correctamente: '{valor}'",
                    "✔" if "+51" in valor else "❌")

        def numero_local():
            input_tel.clear()
            input_tel.send_keys("999999999")
            valor = input_tel.get_attribute("value")
            return ("Número local aceptado.", "✔") if valor == "999999999" else (f"Valor incorrecto: '{valor}'", "❌")

        def letras_en_numero():
            input_tel.clear()
            input_tel.send_keys("999abc123")
            valor = input_tel.get_attribute("value")
            return ("Se aceptaron letras en el campo.", "❗") if any(c.isalpha() for c in valor) else ("Rechazó letras.", "✔")

        def caracteres_especiales():
            input_tel.clear()
            input_tel.send_keys("999@999#999")
            valor = input_tel.get_attribute("value")
            return ("Se aceptaron caracteres especiales.", "❗") if "@" in valor or "#" in valor else ("Especiales bloqueados.", "✔")

        def vacio():
            input_tel.clear()
            valor = input_tel.get_attribute("value")
            return ("Campo vacío permitido.", "⚠") if valor == "" else (f"No se vació correctamente: '{valor}'", "❌")

        def espacios():
            input_tel.clear()
            input_tel.send_keys("     ")
            valor = input_tel.get_attribute("value")
            return ("Campo acepta solo espacios.", "⚠") if valor.strip() == "" else (f"Valor tras limpiar: '{valor}'", "⚠")

        def xss():
            input_tel.clear()
            payload = '<script>alert(1)</script>'
            input_tel.send_keys(payload)
            valor = input_tel.get_attribute("value")
            return ("XSS sin sanitizar." if payload in valor else "XSS bloqueado o modificado.",
                    "❗" if payload in valor else "✔")

        def sql():
            input_tel.clear()
            payload = "' OR '1'='1"
            input_tel.send_keys(payload)
            valor = input_tel.get_attribute("value")
            return ("SQL Injection posible." if payload in valor else "SQL Injection bloqueado.",
                    "❗" if payload in valor else "✔")

        def largo():
            input_tel.clear()
            texto = "+51 " + "9" * 30
            input_tel.send_keys(texto)
            valor = input_tel.get_attribute("value")
            if len(valor) >= len(texto): return "Aceptó número muy largo.", "✔"
            elif 0 < len(valor) < len(texto): return f"Texto recortado. Largo final: {len(valor)}", "⚠"
            else: return "Texto largo rechazado.", "❌"

        test("Número válido", numero_valido)
        test("Número local", numero_local)
        test("Letras en número", letras_en_numero)
        test("Caracteres especiales", caracteres_especiales)
        test("Campo vacío", vacio)
        test("Solo espacios", espacios)
        test("Inyección XSS", xss)
        test("Inyección SQL", sql)
        test("Texto largo", largo)

    # ======================
    # Ejecutamos por input
    # ======================
    for idx, input_el in enumerate(inputs):
        identificador = describir_input(input_el, idx + 1)
        probar_input(input_el, identificador)

    return results
