from selenium.webdriver.common.by import By

# ============================================
# Función principal para probar contraseñas
# ============================================
def run_input_password_tests(driver): # Recibe un driver Selenium ya inicializado
    results = [] # Lista para almacenar los resultados
    inputs = driver.find_elements(By.CSS_SELECTOR, 'input[type="password"]') # Seleccionamos todos los campos tipo contraseña

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

    # =======================
    # Pruebas por cada campo
    # =======================
    def probar_input(input_password, identificador):

        def test(nombre, funcion): # Ejecutamos una prueba y almacenamos el resultado
            try:
                mensaje, estado = funcion()
                results.append(f"[{estado}] {identificador} - {nombre}: {mensaje}")
            except Exception as e:
                results.append(f"[❌] {identificador} - {nombre}: Error durante la prueba: {str(e)}")

        # ==========================
        # Pruebas específicas para password
        # ==========================

        def contrasena_valida():
            input_password.clear()
            input_password.send_keys("Segura123!")
            valor = input_password.get_attribute("value")
            return ("Contraseña aceptada correctamente." if valor == "Segura123!"
                    else f"No se aceptó correctamente. Valor: '{valor}'",
                    "✔" if valor == "Segura123!" else "❌")

        def vacio():
            input_password.clear()
            valor = input_password.get_attribute("value")
            return ("Campo vacío permitido.", "⚠") if valor == "" else (f"No se vació correctamente: '{valor}'", "❌")

        def solo_espacios():
            input_password.clear()
            input_password.send_keys("     ")
            valor = input_password.get_attribute("value")
            return ("Campo acepta solo espacios.", "⚠") if valor.strip() == "" else (f"Valor tras limpiar: '{valor}'", "⚠")

        def caracteres_especiales():
            input_password.clear()
            input_password.send_keys("@#$%^&*()")
            valor = input_password.get_attribute("value")
            return (f"Caracteres especiales aceptados: '{valor}'", "✔")

        def xss():
            input_password.clear()
            payload = "<script>alert(1)</script>"
            input_password.send_keys(payload)
            valor = input_password.get_attribute("value")
            return ("XSS sin sanitizar." if payload in valor else "XSS bloqueado o modificado.",
                    "❗" if payload in valor else "✔")

        def sql():
            input_password.clear()
            payload = "' OR '1'='1"
            input_password.send_keys(payload)
            valor = input_password.get_attribute("value")
            return ("SQL Injection posible." if payload in valor else "SQL Injection bloqueado.",
                    "❗" if payload in valor else "✔")

        def longitud_larga():
            input_password.clear()
            texto = "A" * 1000
            input_password.send_keys(texto)
            valor = input_password.get_attribute("value")
            if len(valor) >= 1000: return "Campo aceptó texto largo.", "✔"
            elif 0 < len(valor) < 1000: return f"Texto recortado. Largo final: {len(valor)}", "⚠"
            else: return "Texto largo rechazado.", "❌"

        test("Contraseña válida", contrasena_valida)
        test("Campo vacío", vacio)
        test("Solo espacios", solo_espacios)
        test("Caracteres especiales", caracteres_especiales)
        test("Inyección XSS", xss)
        test("Inyección SQL", sql)
        test("Texto largo", longitud_larga)

    # ========================
    # Ejecutamos por input
    # ========================
    for idx, input_el in enumerate(inputs):
        identificador = describir_input(input_el, idx + 1)
        probar_input(input_el, identificador)

    return results
