from selenium.webdriver.common.by import By

# ===============================
# Función principal para probar URLs
# ===============================
def run_input_url_tests(driver):
    results = []
    inputs = driver.find_elements(By.CSS_SELECTOR, 'input[type="url"]')

    def describir_input(el, index):
        ph = el.get_attribute("placeholder")
        name = el.get_attribute("name")
        id_attr = el.get_attribute("id")
        if ph: return f'Input con placeholder "{ph}"'
        elif name: return f'Input con name="{name}"'
        elif id_attr: return f'Input con id="{id_attr}"'
        else: return f'Input[{index}] sin identificador'

    def probar_input(input_url, identificador):

        def test(nombre, funcion):
            try:
                mensaje, estado = funcion()
                results.append(f"[{estado}] {identificador} - {nombre}: {mensaje}")
            except Exception as e:
                results.append(f"[❌] {identificador} - {nombre}: Error durante la prueba: {str(e)}")

        def url_valida():
            input_url.clear()
            input_url.send_keys("https://google.com")
            valor = input_url.get_attribute("value")
            return ("URL aceptada correctamente." if valor == "https://google.com"
                    else f"URL no aceptada. Valor: '{valor}'",
                    "✔" if valor == "https://google.com" else "❌")

        def sin_protocolo():
            input_url.clear()
            input_url.send_keys("www.ejemplo.com")
            valor = input_url.get_attribute("value")
            return ("Falta protocolo. Valor no válido.", "❌") if not valor.startswith("http") else ("Aceptó sin protocolo", "❗")

        def incompleta():
            input_url.clear()
            input_url.send_keys("https://")
            valor = input_url.get_attribute("value")
            return ("URL incompleta detectada.", "❌") if valor == "https://" else ("Navegador modificó la entrada.", "❗")

        def caracteres_invalidos():
            input_url.clear()
            input_url.send_keys("https://<script>.com")
            valor = input_url.get_attribute("value")
            return ("Contiene caracteres inválidos." if "<" in valor or ">" in valor else "No sanitizó caracteres.",
                    "❗" if "<" in valor or ">" in valor else "✔")

        def vacio():
            input_url.clear()
            valor = input_url.get_attribute("value")
            return ("Campo vacío permitido.", "⚠") if valor == "" else (f"No se vació correctamente: '{valor}'", "❌")

        def espacios():
            input_url.clear()
            input_url.send_keys("     ")
            valor = input_url.get_attribute("value")
            return ("Campo acepta solo espacios.", "⚠") if valor.strip() == "" else (f"Valor tras limpiar: '{valor}'", "⚠")

        def xss():
            input_url.clear()
            payload = '<script>alert(1)</script>'
            input_url.send_keys(payload)
            valor = input_url.get_attribute("value")
            return ("XSS sin sanitizar." if payload in valor else "XSS bloqueado o modificado.",
                    "❗" if payload in valor else "✔")

        def sql():
            input_url.clear()
            payload = "https://malicioso.com/' OR '1'='1"
            input_url.send_keys(payload)
            valor = input_url.get_attribute("value")
            return ("SQL Injection posible." if payload in valor else "SQL Injection bloqueado.",
                    "❗" if payload in valor else "✔")

        def largo():
            input_url.clear()
            texto = "https://" + "a" * 2000 + ".com"
            input_url.send_keys(texto)
            valor = input_url.get_attribute("value")
            if len(valor) >= len(texto): return "Aceptó URL muy larga.", "✔"
            elif 0 < len(valor) < len(texto): return f"Texto recortado. Largo final: {len(valor)}", "⚠"
            else: return "URL larga rechazada.", "❌"

        def especiales():
            input_url.clear()
            input_url.send_keys("https://$&*(@!#).com")
            valor = input_url.get_attribute("value")
            return f"Caracteres especiales aceptados: '{valor}'", "✔"

        def comillas():
            input_url.clear()
            input_url.send_keys('"https://test.com"')
            valor = input_url.get_attribute("value")
            return f"Comillas aceptadas: '{valor}'", "✔"

        def emojis():
            input_url.clear()
            input_url.send_keys("https://🐱‍💻.com")
            valor = input_url.get_attribute("value")
            return f"Emojis aceptados: '{valor}'", "✔"

        def visibilidad_y_foco():
            visible = input_url.is_displayed()
            enabled = input_url.is_enabled()
            input_url.click()
            activo = driver.switch_to.active_element == input_url
            return f"Visible: {visible}, Enabled: {enabled}, Focus: {activo}", "✔" if visible and enabled and activo else "⚠"

        def atributos():
            datos = {
                "autocomplete": input_url.get_attribute("autocomplete"),
                "maxlength": input_url.get_attribute("maxlength"),
                "required": input_url.get_attribute("required"),
                "aria-label": input_url.get_attribute("aria-label"),
                "aria-required": input_url.get_attribute("aria-required"),
            }
            return f"Atributos detectados: {datos}", "✔"

        def shadow_dom():
            try:
                shadow = driver.execute_script("return arguments[0].shadowRoot", input_url)
                return ("Presente" if shadow else "No está en Shadow DOM", "⚠" if shadow else "✔")
            except:
                return "No accesible como Shadow DOM", "✔"

        def eventos_input_change():
            input_url.clear()
            input_url.send_keys("https://evento.com")
            driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }))", input_url)
            driver.execute_script("arguments[0].dispatchEvent(new Event('change', { bubbles: true }))", input_url)
            return "Eventos input y change disparados.", "✔"

        # Ejecutamos todas las pruebas
        test("URL válida", url_valida)
        test("Sin protocolo", sin_protocolo)
        test("Incompleta", incompleta)
        test("Caracteres inválidos", caracteres_invalidos)
        test("Campo vacío", vacio)
        test("Solo espacios", espacios)
        test("Inyección XSS", xss)
        test("Inyección SQL", sql)
        test("Texto largo", largo)
        test("Caracteres especiales", especiales)
        test("Uso de comillas", comillas)
        test("Emojis y Unicode", emojis)
        test("Visibilidad y foco", visibilidad_y_foco)
        test("Atributos comunes", atributos)
        test("Shadow DOM", shadow_dom)
        test("Eventos input/change", eventos_input_change)

    for idx, input_el in enumerate(inputs):
        identificador = describir_input(input_el, idx + 1)
        probar_input(input_el, identificador)

    print("\n=== RESULTADOS DE PRUEBA DE CAMPOS <input type='url'> ===\n")
    for r in results:
        print(r)

    return results
