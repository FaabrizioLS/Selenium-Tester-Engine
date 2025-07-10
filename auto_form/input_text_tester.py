from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# ===================================
# Función principal para probar texto
# ===================================
def run_input_text_tests(driver):
    results = []
    inputs = driver.find_elements(By.CSS_SELECTOR, 'input[type="text"]')

    def describir_input(el, index):
        ph = el.get_attribute("placeholder")
        name = el.get_attribute("name")
        id_attr = el.get_attribute("id")
        if ph: return f'Input con placeholder "{ph}"'
        elif name: return f'Input con name="{name}"'
        elif id_attr: return f'Input con id="{id_attr}"'
        else: return f'Input[{index}] sin identificador'

    def probar_input(input_text, identificador):

        def test(nombre, funcion):
            try:
                mensaje, estado = funcion()
                results.append(f"[{estado}] {identificador} - {nombre}: {mensaje}")
            except Exception as e:
                results.append(f"[❌] {identificador} - {nombre}: Error durante la prueba: {str(e)}")

        def texto_valido():
            input_text.clear()
            input_text.send_keys("Texto válido")
            valor = input_text.get_attribute("value")
            return ("Texto aceptado correctamente.", "✔") if valor == "Texto válido" else (f"Texto no aceptado. Valor: '{valor}'", "✘")

        def vacio():
            input_text.clear()
            valor = input_text.get_attribute("value")
            requerido = input_text.get_attribute("required")
            if valor == "" and requerido: return "Campo requerido pero se permitió vacío.", "✘"
            elif valor == "": return "Campo vacío permitido.", "⚠"
            else: return f"No se vació correctamente: '{valor}'", "✘"

        def espacios():
            input_text.clear()
            input_text.send_keys("     ")
            valor = input_text.get_attribute("value")
            return ("Campo acepta solo espacios. Validamos limpieza.", "⚠") if valor.strip() == "" else (f"Contiene caracteres tras limpiar espacios: '{valor}'", "⚠")

        def especiales():
            input_text.clear()
            input_text.send_keys("@#$%^&*()")
            valor = input_text.get_attribute("value")
            return f"Especiales aceptados: '{valor}'", "✔"

        def xss():
            input_text.clear()
            payload = '<script>alert(1)</script>'
            input_text.send_keys(payload)
            valor = input_text.get_attribute("value")
            return ("XSS sin sanitizar.", "❗") if payload in valor else ("XSS bloqueado o modificado.", "✔")

        def sql():
            input_text.clear()
            payload = "' OR '1'='1"
            input_text.send_keys(payload)
            valor = input_text.get_attribute("value")
            return ("SQL Injection posible.", "❗") if payload in valor else ("SQL Injection bloqueado.", "✔")

        def largo():
            input_text.clear()
            texto = "A" * 1000
            input_text.send_keys(texto)
            valor = input_text.get_attribute("value")
            maxlength = input_text.get_attribute("maxlength")
            if maxlength and len(valor) > int(maxlength): return f"Texto excede maxlength ({maxlength}).", "✘"
            if len(valor) >= 1000: return "Campo aceptó texto largo.", "✔"
            elif 0 < len(valor) < 1000: return f"Texto recortado. Largo final: {len(valor)}", "⚠"
            else: return "Texto largo rechazado.", "✘"

        def comillas():
            input_text.clear()
            input_text.send_keys('"comillas simples" \'y dobles\'')
            valor = input_text.get_attribute("value")
            return f"Comillas aceptadas: '{valor}'", "✔"

        def emojis():
            input_text.clear()
            input_text.send_keys("😄🚀✨ texto con emoji ❤️")
            valor = input_text.get_attribute("value")
            return f"Emojis y Unicode aceptados: '{valor}'", "✔"

        def visibilidad_y_foco():
            visible = input_text.is_displayed()
            enabled = input_text.is_enabled()
            input_text.click()
            activo = driver.switch_to.active_element == input_text
            return f"Visible: {visible}, Enabled: {enabled}, Focus: {activo}", "✔" if visible and enabled and activo else "⚠"

        def atributos():
            datos = {
                "autocomplete": input_text.get_attribute("autocomplete"),
                "maxlength": input_text.get_attribute("maxlength"),
                "pattern": input_text.get_attribute("pattern"),
                "required": input_text.get_attribute("required"),
                "inputmode": input_text.get_attribute("inputmode"),
                "aria-label": input_text.get_attribute("aria-label"),
                "aria-required": input_text.get_attribute("aria-required"),
            }
            return f"Atributos detectados: {datos}", "✔"

        def shadow_dom():
            try:
                shadow = driver.execute_script("return arguments[0].shadowRoot", input_text)
                return ("Presente" if shadow else "No está en Shadow DOM", "⚠" if shadow else "✔")
            except:
                return "No accesible como Shadow DOM", "✔"

        def eventos_input_change():
            input_text.clear()
            input_text.send_keys("evento")
            driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }))", input_text)
            driver.execute_script("arguments[0].dispatchEvent(new Event('change', { bubbles: true }))", input_text)
            return "Eventos input y change disparados.", "✔"

        test("Texto válido", texto_valido)
        test("Campo vacío", vacio)
        test("Solo espacios", espacios)
        test("Caracteres especiales", especiales)
        test("Inyección XSS", xss)
        test("Inyección SQL", sql)
        test("Texto largo", largo)
        test("Uso de comillas", comillas)
        test("Emojis y Unicode", emojis)
        test("Visibilidad y foco", visibilidad_y_foco)
        test("Atributos comunes", atributos)
        test("Shadow DOM", shadow_dom)
        test("Eventos input/change", eventos_input_change)

    for idx, input_el in enumerate(inputs):
        identificador = describir_input(input_el, idx + 1)
        probar_input(input_el, identificador)

    print("\n=== RESULTADOS DE PRUEBA DE CAMPOS <input type='text'> ===\n")
    for r in results:
        print(r)

    return results
