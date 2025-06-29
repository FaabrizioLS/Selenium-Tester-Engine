from selenium.webdriver.common.by import By

# ==============================================
# Función principal para probar campos <textarea>
# ==============================================
def run_input_textarea_tests(driver): # Recibimos un driver Selenium ya inicializado
    results = [] # Lista para almacenar resultados
    textareas = driver.find_elements(By.TAG_NAME, "textarea") # Capturamos todos los <textarea>

    # ===============================
    # Función para describir el campo
    # ===============================
    def describir_textarea(el, index):
        ph = el.get_attribute("placeholder")
        name = el.get_attribute("name")
        id_attr = el.get_attribute("id")
        if ph: return f'Textarea con placeholder "{ph}"'
        elif name: return f'Textarea con name="{name}"'
        elif id_attr: return f'Textarea con id="{id_attr}"'
        else: return f'Textarea[{index}] sin identificador'

    # ========================
    # Pruebas por cada campo
    # ========================
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

        test("Texto válido", texto_valido)
        test("Campo vacío", vacio)
        test("Solo espacios", solo_espacios)
        test("Texto largo", texto_largo)
        test("Saltos de línea", salto_linea)
        test("Inyección XSS", xss)
        test("Inyección SQL", sql)

    # =============================
    # Ejecutamos pruebas por campo
    # =============================
    for idx, textarea in enumerate(textareas):
        identificador = describir_textarea(textarea, idx + 1)
        probar_textarea(textarea, identificador)

    return results
