from selenium.webdriver.common.by import By

# ==============================================
# Función principal para probar campos <textarea>
# ==============================================
def run_input_textarea_tests(driver):
    results = []
    textareas = driver.find_elements(By.TAG_NAME, "textarea")

    def describir_textarea(el, index):
        ph = el.get_attribute("placeholder")
        name = el.get_attribute("name")
        id_attr = el.get_attribute("id")
        if ph: return f'Textarea con placeholder "{ph}"'
        elif name: return f'Textarea con name="{name}"'
        elif id_attr: return f'Textarea con id="{id_attr}"'
        else: return f'Textarea[{index}] sin identificador'

    def probar_textarea(textarea, identificador):

        def test(nombre, funcion):
            try:
                mensaje, estado = funcion()
                results.append(f"[{estado}] {identificador} - {nombre}: {mensaje}")
            except Exception as e:
                results.append(f"[❌] {identificador} - {nombre}: Error durante la prueba: {str(e)}")

        def texto_valido():
            textarea.clear()
            textarea.send_keys("Este es un comentario válido.")
            valor = textarea.get_attribute("value")
            return ("Texto aceptado correctamente." if valor == "Este es un comentario válido."
                    else f"Texto no aceptado. Valor: '{valor}'", "✔")

        def vacio():
            textarea.clear()
            valor = textarea.get_attribute("value")
            return ("Campo vacío permitido." if valor == "" else f"No se vació correctamente: '{valor}'", "⚠")

        def solo_espacios():
            textarea.clear()
            textarea.send_keys("    ")
            valor = textarea.get_attribute("value")
            return ("Campo acepta solo espacios." if valor.strip() == "" else f"Contiene: '{valor}'", "⚠")

        def texto_largo():
            texto = "a" * 1500
            textarea.clear()
            textarea.send_keys(texto)
            valor = textarea.get_attribute("value")
            if len(valor) >= 1500:
                return "Campo aceptó texto largo.", "✔"
            elif 0 < len(valor) < 1500:
                return f"Texto recortado. Largo final: {len(valor)}", "⚠"
            else:
                return "Texto largo rechazado.", "❌"

        def salto_linea():
            texto = "Primera línea\nSegunda línea"
            textarea.clear()
            textarea.send_keys(texto)
            valor = textarea.get_attribute("value")
            return ("Saltos de línea aceptados." if "\n" in valor else "Saltos omitidos.", "✔")

        def xss():
            payload = "<script>alert(1)</script>"
            textarea.clear()
            textarea.send_keys(payload)
            valor = textarea.get_attribute("value")
            return ("XSS sin sanitizar." if payload in valor else "XSS bloqueado o modificado.",
                    "❗" if payload in valor else "✔")

        def sql():
            payload = "' OR '1'='1"
            textarea.clear()
            textarea.send_keys(payload)
            valor = textarea.get_attribute("value")
            return ("SQL Injection posible." if payload in valor else "SQL Injection bloqueado.",
                    "❗" if payload in valor else "✔")

        def especiales():
            textarea.clear()
            textarea.send_keys("!@#$%^&*()")
            valor = textarea.get_attribute("value")
            return f"Especiales aceptados: '{valor}'", "✔"

        def comillas():
            textarea.clear()
            textarea.send_keys('"comillas" \'dobles\'')
            valor = textarea.get_attribute("value")
            return f"Comillas aceptadas: '{valor}'", "✔"

        def emojis():
            textarea.clear()
            textarea.send_keys("Comentario 😊👍 con emojis 🚀")
            valor = textarea.get_attribute("value")
            return f"Emojis aceptados: '{valor}'", "✔"

        def visibilidad_y_foco():
            visible = textarea.is_displayed()
            enabled = textarea.is_enabled()
            textarea.click()
            activo = driver.switch_to.active_element == textarea
            return f"Visible: {visible}, Enabled: {enabled}, Focus: {activo}", "✔" if visible and enabled and activo else "⚠"

        def atributos():
            datos = {
                "autocomplete": textarea.get_attribute("autocomplete"),
                "maxlength": textarea.get_attribute("maxlength"),
                "required": textarea.get_attribute("required"),
                "aria-label": textarea.get_attribute("aria-label"),
                "aria-required": textarea.get_attribute("aria-required"),
            }
            return f"Atributos detectados: {datos}", "✔"

        def shadow_dom():
            try:
                shadow = driver.execute_script("return arguments[0].shadowRoot", textarea)
                return ("Presente" if shadow else "No está en Shadow DOM", "⚠" if shadow else "✔")
            except:
                return "No accesible como Shadow DOM", "✔"

        def eventos_input_change():
            textarea.clear()
            textarea.send_keys("evento")
            driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }))", textarea)
            driver.execute_script("arguments[0].dispatchEvent(new Event('change', { bubbles: true }))", textarea)
            return "Eventos input y change disparados.", "✔"

        test("Texto válido", texto_valido)
        test("Campo vacío", vacio)
        test("Solo espacios", solo_espacios)
        test("Texto largo", texto_largo)
        test("Saltos de línea", salto_linea)
        test("Inyección XSS", xss)
        test("Inyección SQL", sql)
        test("Caracteres especiales", especiales)
        test("Uso de comillas", comillas)
        test("Emojis y Unicode", emojis)
        test("Visibilidad y foco", visibilidad_y_foco)
        test("Atributos comunes", atributos)
        test("Shadow DOM", shadow_dom)
        test("Eventos input/change", eventos_input_change)

    for idx, textarea in enumerate(textareas):
        identificador = describir_textarea(textarea, idx + 1)
        probar_textarea(textarea, identificador)

    print("\n=== RESULTADOS DE PRUEBA DE CAMPOS <textarea> ===\n")
    for r in results:
        print(r)

    return results
