from selenium.webdriver.common.by import By

# ========================================
# Función principal para probar teléfonos
# ========================================
def run_input_tel_tests(driver):
    results = []
    inputs = driver.find_elements(By.CSS_SELECTOR, 'input[type="tel"]')

    def describir_input(el, index):
        ph = el.get_attribute("placeholder")
        name = el.get_attribute("name")
        id_attr = el.get_attribute("id")
        if ph: return f'Input con placeholder "{ph}"'
        elif name: return f'Input con name="{name}"'
        elif id_attr: return f'Input con id="{id_attr}"'
        else: return f'Input[{index}] sin identificador'

    def probar_input(input_tel, identificador):

        def test(nombre, funcion):
            try:
                mensaje, estado = funcion()
                results.append(f"[{estado}] {identificador} - {nombre}: {mensaje}")
            except Exception as e:
                results.append(f"[❌] {identificador} - {nombre}: Error durante la prueba: {str(e)}")

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

        def visibilidad_y_foco():
            visible = input_tel.is_displayed()
            enabled = input_tel.is_enabled()
            input_tel.click()
            activo = driver.switch_to.active_element == input_tel
            return f"Visible: {visible}, Enabled: {enabled}, Focus: {activo}", "✔" if visible and enabled and activo else "⚠"

        def atributos():
            info = {
                "autocomplete": input_tel.get_attribute("autocomplete"),
                "maxlength": input_tel.get_attribute("maxlength"),
                "pattern": input_tel.get_attribute("pattern"),
                "required": input_tel.get_attribute("required"),
                "inputmode": input_tel.get_attribute("inputmode"),
                "aria-label": input_tel.get_attribute("aria-label"),
                "aria-required": input_tel.get_attribute("aria-required"),
            }
            return f"Atributos detectados: {info}", "✔"

        def shadow_dom():
            try:
                shadow = driver.execute_script("return arguments[0].shadowRoot", input_tel)
                return ("Presente" if shadow else "No está en Shadow DOM", "⚠" if shadow else "✔")
            except:
                return "No accesible como Shadow DOM", "✔"

        def eventos_input_change():
            input_tel.clear()
            input_tel.send_keys("999999999")
            driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }))", input_tel)
            driver.execute_script("arguments[0].dispatchEvent(new Event('change', { bubbles: true }))", input_tel)
            return "Eventos input y change disparados.", "✔"

        test("Número válido", numero_valido)
        test("Número local", numero_local)
        test("Letras en número", letras_en_numero)
        test("Caracteres especiales", caracteres_especiales)
        test("Campo vacío", vacio)
        test("Solo espacios", espacios)
        test("Inyección XSS", xss)
        test("Inyección SQL", sql)
        test("Texto largo", largo)
        test("Visibilidad y foco", visibilidad_y_foco)
        test("Atributos relevantes", atributos)
        test("Shadow DOM", shadow_dom)
        test("Eventos input/change", eventos_input_change)

    for idx, input_el in enumerate(inputs):
        identificador = describir_input(input_el, idx + 1)
        probar_input(input_el, identificador)

    print("\n=== RESULTADOS DE PRUEBA DE CAMPOS <input type='tel'> ===\n")
    for r in results:
        print(r)

    return results
