from selenium.webdriver.common.by import By

# ===============================
# Función principal para probar URLs
# ===============================
def run_input_url_tests(driver): # Recibe un driver Selenium ya inicializado
    results = [] # Lista para almacenar los resultados
    inputs = driver.find_elements(By.CSS_SELECTOR, 'input[type="url"]') # Seleccionamos todos los campos tipo URL

    # ========================
    # Identificación del campo
    # ========================
    def describir_input(el, index): # Generamos una descripción legible del input
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
    def probar_input(input_url, identificador):

        def test(nombre, funcion): # Ejecutamos una prueba y almacenamos el resultado
            try:
                mensaje, estado = funcion()
                results.append(f"[{estado}] {identificador} - {nombre}: {mensaje}")
            except Exception as e:
                results.append(f"[❌] {identificador} - {nombre}: Error durante la prueba: {str(e)}")

        # ========================
        # Pruebas específicas para URL
        # ========================

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

    # ======================
    # Ejecutamos por input
    # ======================
    for idx, input_el in enumerate(inputs):
        identificador = describir_input(input_el, idx + 1)
        probar_input(input_el, identificador)

    return results
